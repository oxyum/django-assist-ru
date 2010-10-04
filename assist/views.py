# -*- coding: utf-8; -*-

import logging
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
from xml.etree import ElementTree as ET

from django.core.mail import mail_admins
from django.db.transaction import commit_on_success
from django.http import HttpResponse

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt
from django.views.decorators.http import require_POST

from assist.conf import SHOP_IDP, SENDRESULT_SECRET
from assist.forms import AssistSendResultForm
from assist.models import AssistAuthResult
from assist.signals import payment_accepted

@require_POST
@csrf_exempt
@commit_on_success
def result(request):
    logger = logging.getLogger('assist.views.result')

    def xml_response(firstcode, secondcode, billnumber=None, packetdate=None):
        response = ET.Element('pushpaymentresult', firstcode=str(firstcode), secondcode=str(secondcode))
     
        if firstcode == 0:
            xml_order = ET.SubElement(response, 'order') 
     
            xml_billnumber = ET.SubElement(xml_order, 'billnumber')
            xml_billnumber.text = str(billnumber)
         
            xml_packetdate = ET.SubElement(xml_order, 'packetdate')
            xml_packetdate.text = str(packetdate)
     
        logger.info('Response to ASSIST: firstcode %d, secondcode %d.', firstcode, secondcode)
        return HttpResponse(ET.tostring(response, 'cp1251'), mimetype='text/xml')

    logger.info('Request from ASSIST SendResult service.')

    firstcode = 1
    secondcode = 0

    form = AssistSendResultForm(request.POST)

    if form.is_valid():
        try:
            if int(form.cleaned_data['Shop_IDP']) != int(SHOP_IDP):
                logger.warning('Incorrect Shop_IDP "%d". Our Shop_IDP is "%d"',
                               form.cleaned_data['Shop_IDP'],
                               int(SHOP_IDP))
                firstcode = 5
                secondcode = 100
                return xml_response(firstcode, secondcode)
      
            gen_hash = md5(''.join([form.data['Shop_IDP'],
                                    form.data['OrderNumber'],
                                    form.data['Total'],
                                    form.data['Currency'],
                                    SENDRESULT_SECRET])).hexdigest().upper()
      
            if gen_hash != form.cleaned_data['CheckValue']:
                logger.warning('MD5 Checksum mismatch for order "%s". Received "%s", generated "%s".',
                               form.cleaned_data['OrderNumber'],
                               form.cleaned_data['CheckValue'],
                               gen_hash)
                firstcode = 5
                secondcode = 158
                return xml_response(firstcode, secondcode)
            logger.debug('Request from ASSIST SendResult service is OK.')

            
            data = {
                'OrderNumber': form.data['OrderNumber'],
                'Response_Code': form.data['Response_Code'],
                'Recommendation': form.data['Recommendation'],
                'Message': form.data['Message'],
                'Comment': form.data['Comment'],
                'Date': form.cleaned_data['Date'],
                'Total': form.data['Total'],
                'Currency': form.data['Currency'],
                'CardType': form.data['CardType'],
                'CardNumber': form.data['CardNumber'],
                'LastName': form.data['LastName'],
                'FirstName': form.data['FirstName'],
                'MiddleName': form.data['MiddleName'],
                'Address': form.data['Address'],
                'Email': form.data['Email'],
                'Country': form.data['Country'] if form.data['Country'] != 'UNKNOWN' else '',
                'Rate': '0.0000',
                'ApprovalCode': form.data['ApprovalCode'] if form.data['ApprovalCode'] != 'UNKNOWN' else '',
                'CardSubType': form.data['CardSubType'] if form.data['CardSubType'] != 'UNKNOWN' else '',
                'CVC2': form.data['CVC2'],
                'CardHolder': form.data['CardHolder'],
                'IPAddress': form.data['IPAddress'],
                'ProtocolTypeName': form.data['ProtocolTypeName'],
                'BillNumber': form.data['BillNumber'],
                'BankName': form.data['BankName'] if form.data['BankName'] != 'UNKNOWN' else '',
                'Status': form.data['Status'],
                'Error_Code': form.data['Error_Code'],
                'Error_Comment': form.data['Error_Comment'],
                'ProcessingName': form.data['ProcessingName'],
                'PacketDate': form.cleaned_data['PacketDate'],
                'PatmentType': form.data['PaymentTransactionType_id'],
            }

            authresult = AssistAuthResult(**data)
            try:
                old_instance = AssistAuthResult.objects.get(BillNumber=authresult.BillNumber)
                authresult._log_changes(old_instance)
                pk = old_instance.pk
            except AssistAuthResult.DoesNotExist:
                pk = None
            authresult.pk = pk
            authresult.save()

            if authresult.Status == 'Authorized':
                payment_accepted.send(sender=authresult.__class__, payment=authresult)

            firstcode = 0
        except Exception, e:
            logger.exception('Unknown error:')
    else:
        logger.warning('Some errors in form validation: %s', form.errors)

    return xml_response(firstcode, secondcode)
