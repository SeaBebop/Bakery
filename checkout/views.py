from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import redirect
from django_project.settings import FRONTEND_CHECKOUT_SUCCESS_URL,FRONTEND_CHECKOUT_FAILED_URL
from post.serializer import CartSerializer
import stripe 
from environs import Env
from post.models import Cart,Product
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
from django_project import settings
from django.contrib.sessions.models import Session
import json 
# Create your views here.
env = Env()
env.read_env()
stripe.api_key = env("DOCKER_STRIPE")
endpoint_secret = env('DOCKER_ENDPOINT_SK')

class Webhook(APIView):
    def post(self,request):
        payload = request.body
        print('This is payload',payload)
        print('')
        
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)
        # Handle the checkout.session.completed event
        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            #print('this is triggered', session)

            # Save an order in your database, marked as 'awaiting payment'
            create_order(session)

            # Check if the order is already paid (for example, from a card payment)
            #
            # A delayed notification payment will have an `unpaid` status, as
            # you're still waiting for funds to be transferred from the customer's
            # account.
            if session.payment_status == "paid":
            # Fulfill the purchase
                fulfill_order(session)

        elif event['type'] == 'checkout.session.async_payment_succeeded':
            session = event['data']['object']

            # Fulfill the purchase
            fulfill_order(session)

        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']

            # Send an email to the customer asking them to retry their order
            email_customer_about_failed_payment(session)
                

        # Passed signature verification
        return HttpResponse(status=200)

def fulfill_order(session):
  # TODO: fill me in
  #Will use this to delete the cart info
  checkoutID = session['id']
  customerInfo = stripe.checkout.Session.retrieve(checkoutID)
  customerInfo = customerInfo['metadata']['userInfo']
  print('This is customerInfo', customerInfo)

  #print('this is session', session['metadata']['userInfo'])


def create_order(session):
  # TODO: fill me in
  print("Creating order")

def email_customer_about_failed_payment(session):
  # TODO: fill me in
  print("Emailing customer")

class CreateCheckoutSession(APIView):
    

    def get(self,request,*args,**kwargs):
        charge = stripe.Charge.list(customer='cus_O8yLbjwStIAW8w',payment_intent='pi_3NNzeXH83CFbAyZP0hhKCg7z')
        return Response(charge)
              
    def post(self,request,*args,**kwargs): 
        #Setting up a cart of products
        counter = 0
        line_items = []
        cart = None
        item = None
        customerID = None
        userData = None
        loggedIn = False
        passInInfo = None
        itemDict = None
        
        #Trying to decode on the backend more for security purposes
        #Created a solution for redirecting with a post
        #print(self.request.session.session_key)<-this doesn't work

        #So I passed on hidden inputs of the user data which contains:
        #Who they are, if they are logged in, their stripe customer ID
        #With this data I make checkout 

        if request.data['userID'] != '':
            loggedIn = True
            userData = jwt.decode(str(request.data['userID']),key=settings.SECRET_KEY,algorithms=["HS256"])
            customerID = userData['customer']
        
        
        if request.data['userID'] != '':
            cart = Cart.objects.filter(user=userData['user_id']).values_list('orders__item',flat=True)
            item = Cart.objects.filter(user=userData['user_id']).values_list('orders__quantity',flat=True)

            customerID = customerID
        if request.data['userID'] == '' and request.data['sessionKey'] != '': 
            #print('this triggered')
            cart = Cart.objects.filter(session_key=request.data['sessionKey']).values_list('orders__item',flat=True)
            item = Cart.objects.filter(session_key=request.data['sessionKey']).values_list('orders__quantity',flat=True)
            customerID = Session.objects.get(pk=request.data['sessionKey'])
            customerID = customerID.get_decoded()
            customerID = customerID[str(request.data['sessionKey'])]
      
            
        for cart_items in cart:
            
            line_items.append(
                {
                 'price_data' : {
                      'currency': 'usd',
                      #Strip interestingly set up prices as ints, so 7.00 is 7.00* 100= 700 
                        'unit_amount':  int(Product.objects.filter(id=cart_items).values_list('price',flat=True)[0] * 100),
                'product_data': {
                    'name': Product.objects.filter(id=cart_items).values_list('name',flat=True)[0],
                },
                },
                'quantity': item[counter],
                    })
            counter+=1

        #Creating a dict of product data to pass on data to the payment intent
        #This idea failed, lead there was a 500 character limit
        #counter = 0
        #print('this is line items',line_items)
        """        
            for product in line_items:
            tmp = {str(counter) : product['product_data']}
            itemDict.update(tmp)
            counter+=1"""
        #print('This is dict of items',itemDict)

        #itemDict = dict(zip(cart,item))

        #Instead of doing what is above I realized
        #Using user customerID i can get PaymentIntent->CheckoutData->LineItems
        #Perfect for purchase history
        #Using Charge I should get the reciept for the user
        try:
            if loggedIn:
                passInInfo = userData['user_id']
            else:
                passInInfo = request.data['sessionKey']
            #print(passInInfo)
            checkout_session = stripe.checkout.Session.create(
                #So I know who they are for webhook purposes
                metadata={
                    "userInfo":passInInfo
                },
                        
                        
                        line_items=line_items,
                        customer = customerID,
                        mode='payment',
                        #So I can document more info on what the products are 
                    
                        success_url=FRONTEND_CHECKOUT_SUCCESS_URL,
                        cancel_url=FRONTEND_CHECKOUT_FAILED_URL,
                    )


            
            
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)      
        return Response('')
           
      