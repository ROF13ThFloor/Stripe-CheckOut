from math import prod
from operator import sub
from tkinter import EventType
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.views.generic.base  import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http.response import  JsonResponse , HttpResponse
import stripe
import json , pymongo

class CheckOutPage(TemplateView):
    template_name = 'CheckOut.html'


class SuccessPage(TemplateView):
    template_name = 'Success.html'


@csrf_exempt
def pub_keyrequets(request):
    if request.method == 'GET':
        pyb_keyrequest = {'pubkey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(pyb_keyrequest, safe=False)



@csrf_exempt
def create_checkout_session(request):


    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price = stripe.Price.create(
            unit_amount=20,
            currency="usd",
            recurring={"interval": "month"},
            product="prod_LMHGYavbG0yp39",
                        )
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': price.id ,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})



@csrf_exempt
def check_webhook(request):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Customers"]
    mycol = mydb["purchaseInfo"]





    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key    
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        print('payment was successfull ')
        Customer_email = event.data.object.customer_details.email
        Customer_id = event.data.object.customer
        Exp_date = event.data.object.expires_at
        Session_id = event.data.object.id
        mode = 'subscription'
        payment_status = event.data.object.payment_status
        sub_id = event.data.object.subscription
        prod_id = 'prod_LMHGYavbG0yp39'

        info = {
            "Customer_email" : Customer_email , 
            "Customer_id" : Customer_id , 
            "Exp_date"  :  Exp_date , 
            "Session_id" : Session_id , 
            "mode" : mode , 
            "payment_status"  : payment_status , 
            "sub_id" : sub_id , 
            "prod_id" : prod_id 

        }
        mycol.insert_one(info)
        print('new infor added -----------------------')
        
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)