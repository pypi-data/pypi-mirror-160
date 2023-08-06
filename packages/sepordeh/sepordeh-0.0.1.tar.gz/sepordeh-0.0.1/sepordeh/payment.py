import requests
import json

# add invoice
def add_invoice(merchant='' , amount=10000, callback='', description='', orderId='', phone=''):
    url = 'https://sepordeh.com/merchant/invoices/add'
    body = {
        "merchant":merchant,
        "amount": amount,
        "callback": callback,
        "description": description,
        "orderId": orderId,
        "phone": phone
    }
    res = requests.post(url, data=json.dumps(body), headers={"Content-Type": "application/json"})
    if res.status_code == 200:
        status = res.json().get('status')
        if status == 200:
            return res.json().get('information').get('invoice_id')
    return null


# payment url
def payment_url(invoice_id=''):
    return f'https://sepordeh.com/merchant/invoices/pay/automatic:true/id:{invoice_id}'


# verify invoice
def verify_invoice(merchant='' , authority=''):
    url = 'https://sepordeh.com/merchant/invoices/verify'
    body = {
        "merchant":merchant,
        "authority": authority
    }
    res = requests.post(url, data=json.dumps(body), headers={"Content-Type": "application/json"})
    if res.status_code == 200:
        status = res.json().get('status')
        if status == 200:
            return res.json().get('information')
    return null
