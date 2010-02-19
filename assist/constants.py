#coding: utf-8

# адреса различных сервисов ASSIST
TEST_MODE1_URL = "https://test.assist.ru/shops/purchase.cfm"
TEST_MODE2_URL = "https://test.assist.ru/shops/cardpayment.cfm"
TEST_GET_RESULTS_URL = "https://test.assist.ru/results/results.cfm"
REAL_MODE1_URL = "https://secure.assist.ru/shops/purchase.cfm"
REAL_MODE2_URL = "https://secure.assist.ru/shops/cardpayment.cfm"
REAL_GET_RESULTS_URL = "https://secure.assist.ru/results/results.cfm"
CHARGE_URL = "https://secure.assist.ru/postauths/postauth.cfm"
REFUND_URL = "https://secure.assist.ru/rvr/rvr.cfm"

# форматы ответа на запрос
ASSIST_FORMAT_CSV = 1
ASSIST_FORMAT_WDDX = 2
ASSIST_FORMAT_XML = 3
ASSIST_FORMAT_SOAP = 4

# причины возврата средств или отмены авторизации
ASSIST_RVR_SHOP = 1
ASSIST_RVR_CUSTOMER = 2
ASSIST_RVR_FRAUD = 3

# языки
ASSIST_LANGUAGE_RU = 0
ASSIST_LANGUAGE_EN = 1

# Названия полей, которые приходят в CSV, не совпадают с теми, что описаны в
# приложении 5.4, поэтому явно прописываем соответствие
FIELDS_MAPPING = {
    'Order Number': 'OrderNumber',
    'Result Code': 'Response_Code',
    'Recommendation': 'Recommendation',
    'Message': 'Message',
    'Comment': 'Comment',
    'Order Date': 'Date',
    'Order Total': 'Total',
    'Currency Code': 'Currency',
    'Card Type': 'CardType',
    'Card Number': 'CardNumber',
    'Lastname': 'LastName',
    'Firstname': 'FirstName',
    'Middlename': 'MiddleName',
    'Address': 'Address',
    'E-mail': 'Email',
    'Country Code': 'Country',
    'Currency rate': 'Rate',
    'Approval Code': 'ApprovalCode',
    'Mean Subtype': 'CardSubType',
    'CVC2 Exist': 'CVC2',
    'Cardholder': 'CardHolder',
    'IP-address': 'IPAddress',
    'Protocol Type': 'ProtocolTypeName',
    'Payment No.': 'BillNumber',
    'Bank issuer': 'BankName',
    'Order State': 'Status',
    'Processing System Response Code': 'Error_Code',
    'Processing System Response Code Description': 'Error_Comment',
    'Paket date': 'PacketDate',
#    'Digital Signature': '_Signature',
    'Processing System Name': 'ProcessingName',
    'Payment Type': 'PatmentType',
}