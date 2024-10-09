import hashlib
import random

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render
from django.db.models import Max
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from .models import *
# Create your views here.
def start(request):
    request.session['cart_id'] = Cart.objects.aggregate(Max('id'))
    response = redirect("/shop/")
    return response

def regview(request):
    if not (request.session.get("curruser") is None):
        return redirect(request.session["path"])
    return render(request, 'register.html')

def newuser(request):
    name = request.POST.get("username")
    email = request.POST.get("email")
    psw = hashlib.md5(request.POST.get("psw").encode(encoding='UTF-8', errors='strict'))
    pswrpt = hashlib.md5(request.POST.get("psw-repeat").encode(encoding='UTF-8', errors='strict'))
    if (psw.hexdigest() != pswrpt.hexdigest()):
        messages.info(request,"Пароли не совпадают")
        return redirect('regview')
    try:
        SiteUser.objects.create(UserName=name, EMail=email, Pass=psw.hexdigest())
        return HttpResponse(f"<h1>Пользователь {name} создан</h1>"
                        f"<a href='/shop/'>Назад</button>")
    except IntegrityError:
        messages.info(request, "Пользователь с данным именем существует")
        return redirect('regview')

def newitem(request):
    brand = request.POST.get("brand")
    type = request.POST.get("type")
    name = request.POST.get("name")
    price = request.POST.get("price")
    try:
        ProdModel.objects.create(brand=brand, type=type, name=name,price=price)
        return HttpResponse(f"<h1>Карточка товара создана</h1>"
                        f"<a href='/shop/'>Назад</button>")
    except:
        messages.info(request, "Ошибка")
        return redirect('nitemview')


def login(request):
    name = request.POST.get("username")
    psw = hashlib.md5(request.POST.get("psw").encode(encoding = 'UTF-8', errors = 'strict'))
    Users = SiteUser.objects.all()
    for User in Users:
        if name == User.UserName and psw.hexdigest() == User.Pass:
            request.session["curruser"] = User.UserName
            request.session["isAdmin"] = User.isAdmin
    return redirect(request.session["path"])

def unlogin(request):
    if request.session.get("curruser"):
        del request.session["curruser"]
    return redirect(request.session["path"])


def product_list(request):
    products = ProdModel.objects.all()
    return render(request, 'product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(ProdModel, id=product_id)
    cart_id = request.session.get('cart_id')
    print(cart_id)
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = get_object_or_404(Cart, id=cart_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect("/shop/")

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        cart_item.quantity = int(request.POST.get('quantity', 1))
        cart_item.save()
    return redirect("/cart/")



def cart_detail(request):
    request.session["path"] = request.path
    curruser = ""
    if not (request.session.get("curruser") is None):
        curruser = request.session.get("curruser")
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return render(request, 'checkout.html', {'cart': None, 'total_price': 0,"User": curruser})

    cart = get_object_or_404(Cart, id=cart_id)
    total_price = 0
    for item in cart.cartitem_set.all():
        total_price += int(float(item.total_price()))

    return render(request, 'checkout.html', {'cart': cart, 'total_price': total_price,"User": curruser})

def remove_from_cart(request, product_id):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, pk=cart_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('cart_detail')


def eshop(request):
    request.session['cart_id'] = Cart.objects.aggregate(Max('id'))['id__max']
    request.session["path"] = request.path
    Prods = ProdModel.objects.all()
    contextdict = {
        "Prods": Prods
    }
    if not (request.session.get("curruser") is None):
        contextdict["User"] = request.session.get("curruser")
        contextdict["isAdmin"] = request.session.get("isAdmin")
    return render(request,"prodlist.html",context=contextdict)

def conts(request):
    request.session["path"] = request.path
    contextdict = {}
    if not (request.session.get("curruser") is None):
        contextdict["User"] = request.session.get("curruser")
        contextdict["isAdmin"] = request.session.get("isAdmin")
    return render(request,'contacts.html',context=contextdict)

def about(request):
    request.session["path"] = request.path
    contextdict = {}
    if not (request.session.get("curruser") is None):
        contextdict["User"] = request.session.get("curruser")
        contextdict["isAdmin"] = request.session.get("isAdmin")
    return render(request, 'about.html', context=contextdict)

def cartview(request):
    request.session["path"] = request.path
    contextdict = {}
    if not (request.session.get("curruser") is None):
        contextdict["User"] = request.session.get("curruser")
        contextdict["isAdmin"] = request.session.get("isAdmin")
    return render(request, 'checkout.html', context=contextdict)

def make_order(request):
    orderfor = None
    if not (request.session.get("curruser") is None):
        orderfor = get_object_or_404(SiteUser, UserName=request.session.get("curruser"))
    else: orderfor = get_object_or_404(SiteUser, UserName="GUEST")
    cart_id = request.session.get('cart_id')
    ordernum = random.randint(1,1000000)
    for cart_item in get_list_or_404(CartItem, cart=cart_id):
        Orders.objects.create(OrderNum=ordernum, User=orderfor, Bought=cart_item.product,quantity=cart_item.quantity)
    Cart.objects.filter(id=cart_id).delete()
    return HttpResponse(f"<h1>Заказ №{ordernum} создан</h1>"
                        f"<a href='/shop/'>Назад</button>")

def nitemview(request):
    return render(request, 'additem.html')


