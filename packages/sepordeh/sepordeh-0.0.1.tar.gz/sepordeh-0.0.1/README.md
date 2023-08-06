# Sepordeh

Python library for using www.sepordeh.com payemnt gateway

[webservice documentation](https://sepordeh.com/webservice)

کتابخانه پایتون جهت اتصال به درگاه پرداخت www.sepordeh.com

[مستندات وبسرویس](https://sepordeh.com/webservice)

## Installation

```bash
pip install sepordeh
```

## Usage

ایجاد فاکتور

add invoice

```python
from sepordeh.payment import add_invoice

# returns invoice_id
add_invoice(merchant='' , amount='', callback='', description='', orderId='', phone='')
```

آدرس پرداخت

payment url

```python
from sepordeh.payment import payment_url

# returns url
payment_url(invoice_id='')

```

تایید پرداخت فاکتور

verify invoice

```python
from sepordeh.payment import verify_invoice

# returns card , invoice_id
verify_invoice(merchant='' , authority='')

```
