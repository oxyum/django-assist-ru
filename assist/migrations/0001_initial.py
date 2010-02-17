#coding: utf-8

from south.db import db
from django.db import models
from assist.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AssistAuthResult'
        db.create_table('assist_assistauthresult', (
            ('id', orm['assist.AssistAuthResult:id']),
            ('OrderNumber', orm['assist.AssistAuthResult:OrderNumber']),
            ('Response_Code', orm['assist.AssistAuthResult:Response_Code']),
            ('Recommendation', orm['assist.AssistAuthResult:Recommendation']),
            ('Message', orm['assist.AssistAuthResult:Message']),
            ('Comment', orm['assist.AssistAuthResult:Comment']),
            ('Date', orm['assist.AssistAuthResult:Date']),
            ('Total', orm['assist.AssistAuthResult:Total']),
            ('Currency', orm['assist.AssistAuthResult:Currency']),
            ('CardType', orm['assist.AssistAuthResult:CardType']),
            ('CardNumber', orm['assist.AssistAuthResult:CardNumber']),
            ('LastName', orm['assist.AssistAuthResult:LastName']),
            ('FirstName', orm['assist.AssistAuthResult:FirstName']),
            ('MiddleName', orm['assist.AssistAuthResult:MiddleName']),
            ('Address', orm['assist.AssistAuthResult:Address']),
            ('Email', orm['assist.AssistAuthResult:Email']),
            ('Country', orm['assist.AssistAuthResult:Country']),
            ('Rate', orm['assist.AssistAuthResult:Rate']),
            ('ApprovalCode', orm['assist.AssistAuthResult:ApprovalCode']),
            ('CardSubType', orm['assist.AssistAuthResult:CardSubType']),
            ('CVC2', orm['assist.AssistAuthResult:CVC2']),
            ('CardHolder', orm['assist.AssistAuthResult:CardHolder']),
            ('IPAddress', orm['assist.AssistAuthResult:IPAddress']),
            ('ProtocolTypeName', orm['assist.AssistAuthResult:ProtocolTypeName']),
            ('BillNumber', orm['assist.AssistAuthResult:BillNumber']),
            ('BankName', orm['assist.AssistAuthResult:BankName']),
            ('Status', orm['assist.AssistAuthResult:Status']),
            ('Error_Code', orm['assist.AssistAuthResult:Error_Code']),
            ('Error_Comment', orm['assist.AssistAuthResult:Error_Comment']),
            ('ProcessingName', orm['assist.AssistAuthResult:ProcessingName']),
            ('PacketDate', orm['assist.AssistAuthResult:PacketDate']),
            ('PatmentType', orm['assist.AssistAuthResult:PatmentType']),
        ))
        db.send_create_signal('assist', ['AssistAuthResult'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AssistAuthResult'
        db.delete_table('assist_assistauthresult')
        
    
    
    models = {
        'assist.assistauthresult': {
            'Address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'ApprovalCode': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'BankName': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'BillNumber': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'CVC2': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'CardHolder': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'CardNumber': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'CardSubType': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'CardType': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'Comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'Country': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'Currency': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'Date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'Email': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'Error_Code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'Error_Comment': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'FirstName': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'IPAddress': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'LastName': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'Message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'MiddleName': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'OrderNumber': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'PacketDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'PatmentType': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ProcessingName': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'ProtocolTypeName': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'Rate': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'Recommendation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'Response_Code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'Status': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'Total': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['assist']
