import stripe
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from payment.tasks import payment_completed


from orders.models import Order

@csrf_exempt
def stripe_webhook(request: HttpRequest):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None


    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        try: 
            order = Order.objects.get(id=session.client_reference_id)
        except Order.DoesNotExist:
            return HttpResponse(status=404)

        order.paid = True
        order.stripe_id = session.payment_intent
        order.save()
        payment_completed.delay(order.id)    

    return HttpResponse(status=200)
