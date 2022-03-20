from django.shortcuts import render

# Create your views here.
from django.views.generic.base  import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http.response import  JsonResponse
import stripe


class CheckOutPage(TemplateView):
    template_name = 'CheckOut.html'



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
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})