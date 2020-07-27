from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate, LoginPerson
from math import ceil
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# forms
from .forms import LoginForm, SignInForm, ContactForm
# Create your views here.


# Paytm details
MERCHANT_KEY = '44DnaXde4a0fYpdC'
MERCHANT_ID = 'InURMN50387203211187'


def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # calculating no of slides
    # nslides = n//4 + ceil(n/4 - n//4)
    # params = {'no_of-sildes': noOfSlides,
    #           'range': range(1, noOfSlides), 'product': products}
    pvals = Product.objects.values('category', 'id')
    cats = {item['category'] for item in pvals}
    allProds = []
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + ceil(n/4 - n//4)
        allProds.append([prod, range(1, nslides), nslides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, 'shop/about.html')


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    messages.success(request, 'Successfully Logged in')
                    login(request, user)
                    return redirect('/shop')
                else:
                    raise ObjectDoesNotExist
            except ObjectDoesNotExist:
                messages.error(request, 'Invalid Username or Password!')
    form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})


def logoutUser(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect('/shop')


def signinUser(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
        # try block to check if the user did not exist so raise error and make new user
            try:
                user = LoginPerson.objects.get(email=email)
            # is user does not exist
            except ObjectDoesNotExist:
                user = form.save()
                # User Object
                newUser = User.objects.create_user(
                    username=f'{user.first_name}{user.person_id}',
                    password=user.password,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name)
                newUser.save()
                # saving objects

                login(request, newUser)
                messages.success(
                    request, "ThankYou to become a part of MyCart")

                return redirect('/shop/')
            # if user already exist
            else:
                messages.error(request, 'User Already exist')
                return render(request, 'shop/signin.html', {'form': form})

    form = SignInForm()
    return render(request, 'shop/signin.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, 'Thank You For Giving Your Feedback To Us')
    form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        # if user did't ennter input correctly
        if(orderId == '' or email == ''):
            # return empty JSON file
            return HttpResponse('{"status":"fielderrror"}')
        try:
            try:
                order = Order.objects.get(order_id=orderId, email=email)
            # raise ObjectDoesNotExist if entered order is not found in Orders
            except ObjectDoesNotExist:
                # if the order is not found then return empty JSON file
                return HttpResponse('{"status": "noitems"}')
            # if the id is in Orders then check for updates
            else:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                # if we dont use default= str then it will raise an error that timestamp is not JSON serializable
                # we are sending updates which is an js obejct of update desc and time of desc and order.items_json
                # is containing a list of items
                response = json.dumps(
                    {'status': 'success', 'updates': updates, 'items': order.items_json}, default=str)

                # returning reposne as json file
                return HttpResponse(response)
        # if any unexpected error occur
        except Exception:
            return HttpResponse('{"status": "error"}')
    return render(request, 'shop/tracker.html')


def searchMatch(query, item):
    query = query.lower()
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslides = n//4 + ceil(n/4 - n//4)
        if len(prod) != 0:
            allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds': allProds, "msg": ''}
    if len(allProds) == 0 or len(query) < 4:
        params = {'search': query}
    return render(request, "shop/search.html", params)


def productView(request, myid):
    product = Product.objects.get(id=myid)
    params = {'product': product}
    return render(request, 'shop/productview.html', params)


@login_required(login_url='/shop/login/')
def myorders(request):
    user = request.user
    orders = Order.objects.filter(email=user.email)
    orders_dict = {}
    # adding products id in set because may be some other person uses same email for order and then
    # there will be more than one order with same email id
    print("json")
    for order in orders:
        items_json = json.loads(order.items_json)
        print(items_json)
        for item in items_json:
            if item in orders_dict.keys():
                orders_dict[item] += int(items_json[item][0])
            else:
                orders_dict[item] = int(items_json[item][0])

    user_orders = []
    print(orders_dict)
    for order in orders_dict:
        order_id = int(order.replace('pr', ''))
        order_obj = Product.objects.get(id=order_id)
        order_dict = {'product': order_obj, 'qty': orders_dict[order]}
        user_orders.append(order_dict)

    params = {'orders': user_orders}
    return render(request, 'shop/myorders.html', params)


@login_required(login_url='/shop/login')
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        amount = request.POST.get('amount')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        items_json = request.POST.get('itemsjson', '')
        order = Order(items_json=items_json, amount=amount, name=name, email=email, phone=phone,
                      address=address, city=city, state=state, zip_code=zip_code)
        order.save()
        # id = order.order_id
        # thank = True
        # success msg to be displayed on Home Page of Shop
        # messages.success(
        #     request, f'Thanks You. Your Parcel id is {id} you can keep track of your Parcel.')
        # # making an update order
        # order_update = OrderUpdate(order_id=id, update_desc="Order Placed")
        # order_update.save()
        # return render(request, 'shop/checkout.html', {'thank': thank})
        param_dict = {
            'MID': MERCHANT_ID,
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(order.amount),
            'CUST_ID': order.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            # webstaging is used for testing purposes
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        print("return redirect/paytm")
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    else:
        return render(request, 'shop/checkout.html')


# here PAYTM will send you POST request
@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("Order successful")
        else:
            print("Order was not successful because " +
                  response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
