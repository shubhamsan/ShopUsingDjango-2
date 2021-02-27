from decimal import Decimal

from  django . conf  import  settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from  paypal . standard . forms  import  PayPalPaymentsForm
from PayTm import Checksum
from .paytm import generate_checksum, verify_checksum

from orders.models import Order

PAYTM_SECRET_KEY = 'hMeivIIuJ2nqJ51f'
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    PAYTM_SECRET_KEY = 'hMeivIIuJ2nqJ51f'
    merchant_key = settings.PAYTM_SECRET_KEY
    host = request.get_host()
    amounts= '%.2f' % order.get_total_cost().quantize(
            Decimal('.01'))
  
    
    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(order_id)),
        ('CUST_ID', str(order.email)),
        ('TXN_AMOUNT',str(amounts) ),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/payment/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )
    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)
    paytm_params['CHECKSUMHASH'] = checksum
    return render(request, 'payment/process.html', context=paytm_params)



@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

@csrf_exempt
def handlerequest(request):
  pass



@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payment/canceled.html')

        return render(request, 'payment/callback.html', context=received_data)




