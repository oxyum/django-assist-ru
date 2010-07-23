#coding: utf-8

# адреса ASSIST
TEST_SERVER = 'https://test.assist.ru'
REAL_SERVER = 'https://secure.assist.ru'

MODE1_PATH = '/shops/purchase.cfm'
MODE2_PATH = '/shops/cardpayment.cfm'
GET_RESULTS_PATH = '/results/results.cfm'
CHARGE_PATH = "/postauths/postauth.cfm"
REFUND_PATH = "/rvr/rvr.cfm"

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

# расшифровки различных кодов и статусов
RESPONSE_CODE_CHOICES = (
    ('AS000', u'АВТОРИЗАЦИЯ УСПЕШНО ЗАВЕРШЕНА'),
    ('AS100', u'ОТКАЗ В АВТОРИЗАЦИИ'),
    ('AS101', u'ОТКАЗ В АВТОРИЗАЦИИ. Ошибочный номер карты'),
    ('AS102', u'ОТКАЗ В АВТОРИЗАЦИИ. Недостаточно средств'),
    ('AS104', u'ОТКАЗ В АВТОРИЗАЦИИ. Неверный срок действия карты'),
    ('AS105', u'ОТКАЗ В АВТОРИЗАЦИИ. Превышен лимит'),
    ('AS106', u'ОТКАЗ В АВТОРИЗАЦИИ. Неверный PIN'),
    ('AS107', u'ОТКАЗ В АВТОРИЗАЦИИ. Ошибка приема данных'),
    ('AS108', u'ОТКАЗ В АВТОРИЗАЦИИ. Подозрение на мошенничество'),
    ('AS109', u'ОТКАЗ В АВТОРИЗАЦИИ. Превышен лимит операций ASSIST'),
    ('AS110', u'Требуется авторизация по 3D-Secure'),
    ('AS200', u'ПОВТОРИТЕ АВТОРИЗАЦИЮ'),
    ('AS300', u'АВТОРИЗАЦИЯ В ПРОЦЕССЕ. ЖДИТЕ'),
    ('AS400', u'ПЛАТЕЖА С ТАКИМИ ПАРАМЕТРАМИ НЕ СУЩЕСТВУЕТ'),
    ('AS998', u'ОШИБКА СИСТЕМЫ. Свяжитесь с ASSIST'),
)

STATUS_CHOICES = (
    ('Authorized', u'Платеж прошел успешно'),
    ('Not authorized', u'Платеж не прошел'),
    ('Preauthorized', u'Авторизация при двустадийном механизме прошла успешно'),
    ('Not preauthorized', u'Авторизация при двустадийном механизме не прошла'),
    ('Captured', u'Финансовое подтверждение прошло успешно'),
    ('Not captured', u'Финансовое подтверждение не прошло'),
    ('Voided', u'Он-лайн отмена авторизации прошла успешно'),
    ('Not Voided', u'Он-лайн отмена авторизации не прошла'),
    ('Refunded', u'Возврат средств прошел успешно'),
    ('Not Refunded', u'Возврат средств не прошел'),
    ('Reversaled', u'Отмена авторизации прошла успешно'),
    ('Not Reversaled', u'Отмена авторизации не прошла'),
    ('in process', u'В процессе'),
)

PAYMENT_TRANSACTION_TYPE_CHOICES = (
    (1, u'Оплата кредитной картой'),
    (2, u'Предварительная авторизация кредитной карты (авторизация при двустадийном режиме работы)'),
    (3, u'Поставторизация кредитной карты (финансовое подтверждение)'),
    (4, u'Возврат средств по оплате кредитной картой (refund)'),
    (6, u'Chargeback средств по оплате кредитной картой'),
    (7, u'Он-лайн отмена авторизации по кредитной карте (void)'),
    (9, u'Reversal'),
    (10, u'Перевод средств WebMoney'),
    (20, u'Оплата средствами PayCash'),
    (24, u'Оплата средствами QIWI (в т. ч. Мобильный платеж Beeline)'),
)


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
