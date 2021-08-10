import json

import razorpay
from django.http.response import JsonResponse
from django.views import  View
from django.views.decorators.csrf import csrf_exempt

from core.settings import RAZORPAY_KEY, RAZORPAY_SECRET, RAZORPAY_WEBHOOK_SECRET
from payment.models import Payment, Transaction

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))
class RazorHookView(View):
    def get(self):
        return  JsonResponse({
            'error':True,
            'message':"Invalid  Request"
        })
    @csrf_exempt
    def post(self,request):
        webhookbody = request.body.decode('utf-8')
        body = json.loads(webhookbody)
        signature = request.headers['X-Razorpay-Signature']
        try:
            payment_id = body['payload']['payment']['entity']['id']
            razorpay_order_id = body['payload']['payment']['entity']['order_id']
            razorpay_amount = body['payload']['payment']['entity']['amount']
            payment_method = body['payload']['payment']['entity']['method']
            verify = client.utility.verify_webhook_signature(body, signature, RAZORPAY_WEBHOOK_SECRET)
            if body['event'] == 'refund.processed':
                print('refund initiated')
                _x = body['payload']['refund']
                print(_x['entity']['id'])
                order = Payment.objects.get(rzp_order_id=razorpay_order_id)

                order.order.payment_status = 'refunded'
                order.order.save()
                trans = Transaction()
                trans.order = order.order
                trans.payment = order
                trans.raw_data = body
                trans.payment_token = _x['entity']['id']
                trans.r_pay_id = _x['entity']['payment_id']





            elif body['event'] == 'payment.captured':
                print('payment captured')
                _x = body['payload']['payment']
                print(_x['entity']['order_id'])
                order = Payment.objects.get(rzp_order_id=razorpay_order_id)
                order.order.is_payment_successfull = True
                order.order.status ="Confirmed"
                order.order.save()
                trans = Transaction()
                trans.order = order.order
                trans.payment = order
                trans.rzp_order_id = razorpay_order_id
                trans.amount = razorpay_amount
                trans.method = _x['entity']['method']
                if _x['entity']['method'] == 'card':
                    trans.card_holder_name = _x['entity']['card']['name']
                    trans.card_issuer = _x['entity']['card']['issuer']
                    trans.card_holder_network = _x['entity']['card']['issuer']['network']
                    trans.card_last_4 = _x['entity']['card']['issuer']['last4']
                trans.bank = _x['entity']['bank']
                trans.wallet = _x['entity']['wallet']
                trans.vpa = _x['entity']['vpa']
                trans.email = _x['entity']['email']
                trans.phone = _x['entity']['contact']
                trans.fee = _x['entity']['fee']
                trans.payment_token = _x['entity']['id']
                trans.raw_data = body
                trans.r_order_id = _x['entity']['order_id']
                trans.r_pay_id = _x['entity']['id']
                trans.hook_signature = signature
                trans.save()
            elif body['event'] == 'payout.created':
                print('payout created')


            elif body['event'] == 'payout.failed':
                print('payment failed')
                # _x = payload['payload']['payment']
                # print(_x['entity']['order_id'])
                # order = Order.objects.get(razorpay_order_id=_x['entity']['order_id'])
                # order.payment_status = 'failure'
                # order.save()
                # trans = Transaction()
                # trans.order = order
                # trans.response = payload
                # trans.r_order_id = _x['entity']['order_id']
                # trans.r_pay_id = _x['entity']['id']
                # trans.hook_signature = signature
                # trans.save()
            else:
                raise ValueError
        except Exception as e:
            print(e)
            print('----------------')
            return JsonResponse(
                {
                    'status':'Fail'
                }
            )
        return  JsonResponse({
            'status':'OK'
        })