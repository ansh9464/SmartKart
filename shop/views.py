from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Product , contact , Orders, OrderUpdate
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
MERCHANT_KEY = 'efdRJm1HFp%yX6RI'
import json
# Create your views here.
def index(request):
    #product_list = Product.objects.all()
    #print(product_list)
    #n=len(product_list)


    all_prods=[]
    category_prods=Product.objects.values('category')
    #print(category_prods)
    categories={item['category'] for item in category_prods}
    print(categories)
    for cat in categories:
        product_list = Product.objects.filter(category=cat)
        #print(product_list)
        n=len(product_list)
        no_of_slides=n//4+ceil((n/4)-(n//4))
        all_prods.append([product_list , range(1,no_of_slides), no_of_slides])



    #all_prods=[[product_list,range(1,no_of_slides),no_of_slides],
     #           [product_list,range(1,no_of_slides),no_of_slides]]
    #list = {'no_of_slides':no_of_slides,'product_list': product_list,'range':range(1,no_of_slides)}



    list={'allprods':all_prods}
    print(all_prods)
    return render(request, 'shop/index.html', list)

def about(request):
    return render(request,'shop/about.html')

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        print(name,email,phone,desc)
        contactus = contact(name=name,email=email,phone=phone,desc=desc)
        contactus.save()
        thank = True
        return render(request, 'shop/contactus.html',{'thank':thank})
    return render(request,'shop/contactus.html')

def productview(request , id):
    #fetching the products by id
    product_list = Product.objects.filter(id=id)
    print(product_list)

    return render(request,'shop/productview.html',{'product':product_list[0]})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status':'success','updates':updates,'items_json':order[0].items_json} ,default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

def searchMatch(query,item):
    if query in item.product_name.lower() or query in item.discription.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    all_prods = []
    category_prods = Product.objects.values('category')
    categories = {item['category'] for item in category_prods}
    for cat in categories:
        product_list_item = Product.objects.filter(category=cat)
        product_list = [item for item in product_list_item if searchMatch(query.lower(),item)]
        n = len(product_list)
        no_of_slides = n // 4 + ceil((n / 4) - (n // 4))
        if len(product_list)!=0 :
            all_prods.append([product_list, range(1, no_of_slides), no_of_slides])

    list = {'allprods': all_prods,'msg':''}
    if len(all_prods) == 0 or len(query)<3:
        list = {'msg':'Please enter the valid search keyword'}
    return render(request, 'shop/search.html', list)

def checkout(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        item_json = request.POST.get('itemjson','')
        price =request.POST.get('total','')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        new_order = Orders(name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone, items_json=item_json,price=price)
        new_order.save()
        update = OrderUpdate(order_id=new_order.order_id,update_desc="We have received your order")
        update.save()
        thank = True
        id = new_order.order_id
        #return render(request, 'shop/checkout.html', {'thank':thank,'id': id})
        param_dict = {

            'MID': 'Sqdvab24023252007793',
            'ORDER_ID': str(new_order.order_id),
            'TXN_AMOUNT': str(price),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        print(param_dict)
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html',{'param_dict':param_dict})
    return render(request,'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    #paytm will send request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
