from payment.models import Payment
from django.urls import reverse
from graphene_django.utils.testing import GraphQLTestCase
from cart.models import Cart, CartLine
from order.models import Address, Design, Order
from product.models import Product
from django.test import TestCase
from utils.test_setup import TestSetup
from django.contrib.auth import get_user_model
import json

User = get_user_model()
# Create your tests here.


class PaymentTestCase(TestSetup, GraphQLTestCase):
    def setUp(self):
        self.create_test_user()

    def make_order_for_payment(self):
        print("==============================================================")
        p1 = self.create_test_product()
        u = User.objects.get(phone="9744567054")
        cart, _ = Cart.objects.get_or_create(user=u)
        cartline = CartLine.objects.create(product_id=p1.pk, cart_id=cart.pk)
        Design.objects.create(cart_id=cart.pk, cart_line=cartline.pk, image=self.get_image(), video=self.get_image(),
                              user=u)
        self.create_test_user_two()
        self.assertTrue(self.client.login(
            phone="9744567054", password="anoop@123"))
        query = """
            mutation checkout($cartId: String!,$billingAddress:String!,$shippingAddress:String!){
              checkout(billingAddress:$billingAddress,shippingAddress:$shippingAddress,cartId:$cartId){
                payment{
                  rzpOrderId
                }
                order{
                  orderId
                  totalOrderValue
                }
              }
            }
        """
        x = self.query(query, variables={'billingAddress': self.create_test_address(user=u),
                                         'shippingAddress': self.create_test_address(user=u), 'cartId': str(cart.pk)})
        # print(x.json())
        # print("==============================================================")

        return x.json()

    def test_webhooks_with_netbanking(self):
        cart_data = self.make_order_for_payment()

        data = {
            "entity": "event",
            "account_id": "acc_BFQ7uQEaa7j2z7",
            "event": "payment.captured",
            "contains": [
                "payment"
            ],
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_DESlfW9H8K9uqM",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "netbanking",
                        "amount_refunded": 0,
                        "amount_transferred": 0,
                        "refund_status": None,
                        "captured": True,
                        "description": None,
                        "card_id": None,
                        "bank": "HDFC",
                        "wallet": None,
                        "vpa": None,
                        "email": "gaurav.kumar@example.com",
                        "contact": "919876543210",
                        "notes": [],
                        "fee": 2,
                        "tax": 0,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                            "bank_transaction_id": "0125836177"
                        },
                        "created_at": 1567674599
                    }
                }
            },
            "created_at": 1567674606
        }
        x = self.client.post(reverse('razorpayhook'), data,
                             content_type='application/json')
        headers = {'X-Razorpay-Signature': "jvjhvgwejdvbjlhwaebvfjhvaeswjflb",
                   'content_type': 'application/json'}
        # x = requests.post('http://967f5ebdb442.ngrok.io/hook/api/payment/',data=json.dumps(data),headers=headers)

        assert x.json() == {'status': 'OK'}

    def test_payment_with_card(self):
        cart_data = self.make_order_for_payment()
        data = {
            "entity": "event",
            "account_id": "acc_BFQ7uQEaa7j2z7",
            "event": "payment.captured",
            "contains": [
                "payment"
            ],
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_DESp9bgForNoUd",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "card",
                        "amount_refunded": 0,
                        "amount_transferred": 0,
                        "refund_status": None,
                        "captured": True,
                        "description": None,
                        "card_id": "card_DESp9fNnu0RoNc",
                        "card": {
                            "id": "card_DESp9fNnu0RoNc",
                            "entity": "card",
                            "name": "Gaurav Kumar",
                            "last4": "1111",
                            "network": "Visa",
                            "type": "debit",
                            "issuer": None,
                            "international": False,
                            "emi": False,
                            "sub_type": "business"
                        },
                        "bank": None,
                        "wallet": None,
                        "vpa": None,
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919876543210",
                        "notes": [],
                        "fee": 2,
                        "tax": 0,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                            "auth_code": "828553"
                        },
                        "created_at": 1567674797
                    }
                }
            },
            "created_at": 1567674804
        }
        x = self.client.post(reverse('razorpayhook'), data,
                             content_type='application/json')
        assert x.json() == {'status': 'OK'}

    def test_payment_with_wallet(self):
        cart_data = self.make_order_for_payment()
        data = {
            "entity": "event",
            "account_id": "acc_BFQ7uQEaa7j2z7",
            "event": "payment.captured",
            "contains": [
                      "payment"
            ],
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_DEStK8twGApHtW",
                              "entity": "payment",
                              "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                              "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "wallet",
                        "amount_refunded": 0,
                        "amount_transferred": 0,
                        "refund_status": None,
                        "captured": True,
                        "description": None,
                        "card_id": None,
                        "bank": None,
                        "wallet": "payzapp",
                        "vpa": None,
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919876543210",
                        "notes": [],
                        "fee": 2,
                        "tax": 0,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                                  "transaction_id": None
                              },
                        "created_at": 1567675034
                    }
                }
            },
            "created_at": 1567675037
        }
        x = self.client.post(reverse('razorpayhook'), data,
                             content_type='application/json')
        assert x.json() == {'status': 'OK'}

    def test_payment_with_upi(self):
        cart_data = self.make_order_for_payment()
        data = {
            "entity": "event",
            "account_id": "acc_BFQ7uQEaa7j2z7",
            "event": "payment.captured",
            "contains": [
                "payment"
            ],
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_DESyzxuld02Zul",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "upi",
                        "amount_refunded": 0,
                        "amount_transferred": 0,
                        "refund_status": None,
                        "captured": True,
                        "description": None,
                        "card_id": None,
                        "bank": None,
                        "wallet": None,
                        "vpa": "gaurav.kumar@upi",
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919876543210",
                        "notes": [],
                        "fee": 2,
                        "tax": 0,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                            "rrn": "0125836177"
                        },
                        "created_at": 1567675356
                    }
                }
            },
            "created_at": 1567675356
        }
        x = self.client.post(reverse('razorpayhook'), data,
                             content_type='application/json')
        assert x.json() == {'status': 'OK'}

    def test_payment_failed(self):
        cart_data = self.make_order_for_payment()
        data = {
            "entity": "event",
            "account_id": "acc_E6ztBHzyaVFgBV",
            "event": "payment.failed",
            "contains": [
                "payment"
            ],
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_Epiw458kREjwE8",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "status": "failed",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": "inv_EpivkS3Vb7AnUD",
                        "international": False,
                        "method": "card",
                        "amount_refunded": 0,
                        "refund_status": None,
                        "captured": False,
                        "description": None,
                        "card_id": "card_EpihqypuNkmSJX",
                        "card": {
                            "id": "card_DESp9fNnu0RoNc",
                            "entity": "card",
                            "name": "Gaurav Kumar",
                            "last4": "1111",
                            "network": "Visa",
                            "type": "debit",
                            "issuer": None,
                            "international": False,
                            "emi": False,
                            "sub_type": "business"
                        },
                        "bank": None,
                        "wallet": None,
                        "vpa": None,
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919876543210",
                        "notes": [],
                        "fee": None,
                        "tax": None,
                        "error_code": "BAD_REQUEST_ERROR",
                        "error_description": "Payment failed",
                        "error_source": "gateway",
                        "error_step": "payment_authorization",
                        "error_reason": "payment_failed",
                        "acquirer_data": {
                            "auth_code": None
                        },
                        "created_at": 1589347206
                    }
                }
            },
            "created_at": 1589347208
        }
        x = self.client.post(reverse('razorpayhook'), data,
                             content_type='application/json')
        assert x.json() == {'status': 'Fail'}

    def test_refund_request(self):
        cart_data = self.make_order_for_payment()
        data = {
            "entity": "event",
            "account_id": "acc_BFQ7uQEaa7j2z7",
            "event": "payment.captured",
            "contains": [
                "payment"
            ],
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_DESyzxuld02Zul",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "upi",
                        "amount_refunded": 0,
                        "amount_transferred": 0,
                        "refund_status": None,
                        "captured": True,
                        "description": None,
                        "card_id": None,
                        "bank": None,
                        "wallet": None,
                        "vpa": "gaurav.kumar@upi",
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919876543210",
                        "notes": [],
                        "fee": 2,
                        "tax": 0,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                            "rrn": "0125836177"
                        },
                        "created_at": 1567675356
                    }
                }
            },
            "created_at": 1567675356
        }
        x = self.client.post(reverse('razorpayhook'), data,
                             content_type='application/json')
        refund = {
            "entity": "event",
            "account_id": "acc_E7OQJcEANmBHTC",
            "event": "refund.processed",
            "contains": [
                "refund",
                "payment"
            ],
            "payload": {
                "refund": {
                    "entity": {
                        "id": "rfnd_FS8TWyPrCsa0OB",
                        "entity": "refund",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "payment_id": "pay_FPoJKWQQ8lK13n",
                        "notes": {
                            "comment": "Customer Notes for Webhooks."
                        },
                        "receipt": None,
                        "acquirer_data": {
                            "arn": None
                        },
                        "created_at": 1597734071,
                        "batch_id": None,
                        "status": "processed",
                        "speed_processed": "normal",
                        "speed_requested": "optimum"
                    }
                },
                "payment": {
                    "entity": {
                        "id": "pay_FPoJKWQQ8lK13n",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "netbanking",
                        "amount_refunded": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "amount_transferred": 0,
                        "refund_status": "partial",
                        "captured": True,
                        "description": None,
                        "card_id": None,
                        "bank": "HDFC",
                        "wallet": None,
                        "vpa": None,
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919999999999",
                        "notes": [],
                        "fee": 11800,
                        "tax": 1800,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                            "bank_transaction_id": "4827433"
                        },
                        "created_at": 1597226379
                    }
                }
            },
            "created_at": 1597734071
        }
        x = self.client.post(reverse('razorpayhook'), refund,
                             content_type='application/json')
        payment = Payment.objects.filter(
            rzp_order_id=cart_data['data']['checkout']['payment']['rzpOrderId'])[0]
        # print(payment.order.status)
        assert payment.order.status == 'cancelled'
        assert x.json() == {'status': 'OK'}
        # print(x.json())

    def test_partial_refund_request(self):
        cart_data = self.make_order_for_payment()
        data = {
            "entity": "event",
            "account_id": "acc_BFQ7uQEaa7j2z7",
            "event": "payment.captured",
            "contains": [
                "payment"
            ],
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_DESyzxuld02Zul",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "upi",
                        "amount_refunded": 0,
                        "amount_transferred": 0,
                        "refund_status": None,
                        "captured": True,
                        "description": None,
                        "card_id": None,
                        "bank": None,
                        "wallet": None,
                        "vpa": "gaurav.kumar@upi",
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919876543210",
                        "notes": [],
                        "fee": 2,
                        "tax": 0,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                            "rrn": "0125836177"
                        },
                        "created_at": 1567675356
                    }
                }
            },
            "created_at": 1567675356
        }
        x = self.client.post(reverse('razorpayhook'), data,
                             content_type='application/json')
        refund = {
            "entity": "event",
            "account_id": "acc_E7OQJcEANmBHTC",
            "event": "refund.processed",
            "contains": [
                "refund",
                "payment"
            ],
            "payload": {
                "refund": {
                    "entity": {
                        "id": "rfnd_FS8TWyPrCsa0OB",
                        "entity": "refund",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100)-500,
                        "currency": "INR",
                        "payment_id": "pay_FPoJKWQQ8lK13n",
                        "notes": {
                            "comment": "Customer Notes for Webhooks."
                        },
                        "receipt": None,
                        "acquirer_data": {
                            "arn": None
                        },
                        "created_at": 1597734071,
                        "batch_id": None,
                        "status": "processed",
                        "speed_processed": "normal",
                        "speed_requested": "optimum"
                    }
                },
                "payment": {
                    "entity": {
                        "id": "pay_FPoJKWQQ8lK13n",
                        "entity": "payment",
                        "amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "currency": "INR",
                        "base_amount": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "status": "captured",
                        "order_id": cart_data['data']['checkout']['payment']['rzpOrderId'],
                        "invoice_id": None,
                        "international": False,
                        "method": "netbanking",
                        "amount_refunded": (float(cart_data['data']['checkout']['order']['totalOrderValue'])*100),
                        "amount_transferred": 0,
                        "refund_status": "partial",
                        "captured": True,
                        "description": None,
                        "card_id": None,
                        "bank": "HDFC",
                        "wallet": None,
                        "vpa": None,
                        "email": "gaurav.kumar@example.com",
                        "contact": "+919999999999",
                        "notes": [],
                        "fee": 11800,
                        "tax": 1800,
                        "error_code": None,
                        "error_description": None,
                        "error_source": None,
                        "error_step": None,
                        "error_reason": None,
                        "acquirer_data": {
                            "bank_transaction_id": "4827433"
                        },
                        "created_at": 1597226379
                    }
                }
            },
            "created_at": 1597734071
        }
        x = self.client.post(reverse('razorpayhook'), refund,
                             content_type='application/json')
        payment = Payment.objects.filter(
            rzp_order_id=cart_data['data']['checkout']['payment']['rzpOrderId'])[0]
        # print(payment.order.status)
        assert payment.order.status == 'processing'
        assert x.json() == {'status': 'OK'}
        # print(x.json())
