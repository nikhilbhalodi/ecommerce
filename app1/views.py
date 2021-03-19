from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView, View
from .models import Product, OrderProduct, Order
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from .forms import Subscribe
from ecommercedemo.settings import EMAIL_HOST_USER
from django.db.models import Q

from django.core.mail import send_mail
# Create your views here.

class ProductView(ListView):
    model = Product
    paginate_by = 6
    template_name = 'app1/home.html'

    def get_queryset(self):
        name = self.request.GET.get('q')
        object_list = self.model.objects.all()
        if name:
            object_list = object_list.filter(
                Q(name__icontains=name) | Q(category__icontains=name) | Q(des__icontains=name))
        return object_list

    def post(self, request, *args, **kwargs):
        sub = self.request.POST.get('email')
        subject = 'thanks'
        message = 'thank you for chossing our servies' 
        recipient_list = str(sub)
        send_mail(subject, 
            message, EMAIL_HOST_USER,[recipient_list], fail_silently = False)
        messages.info(self.request,"send successfully")
        return redirect('app1:home')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app1/product.html'

    def post(self, request, *args, **kwargs):
        sub = self.request.POST.get('email')
        subject = 'Thanks'
        message = 'Thank you for chossing our servies' 
        recipient_list = str(sub)
        send_mail(subject, 
            message, EMAIL_HOST_USER,[recipient_list], fail_silently = False)
        messages.info(self.request,"send successfully")
        return redirect('app1:product',slug=slug)
    
@login_required
def add_to_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    print("================product",product)
    print("===========>slug",slug)
    order_product,created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print("================order_qs",order_qs)
    print("=======>order_product",order_product)
    if order_qs.exists():
        order =order_qs[0]
        print("================order",order)
        if order.products.filter(product__slug=product.slug).exists():
            order_product.qty += 1
            order_product.save()
            messages.info(request,'Add Successfully')
            return redirect("app1:order-summary")
            
        else:
            
            order.products.add(order_product)
            messages.info(request,'Add Successfully')
            return redirect('app1:product',slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request,'Add Successfully')
        return redirect('app1:product',slug=slug)

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            order_product.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("app1:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("app1:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("app1:product", slug=slug)


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.qty > 1:
                order_product.qty -= 1
                order_product.save()
                messages.info(request, "This item quantity was remove.")
            else:
                order.products.remove(order_product)
                messages.info(request, "This item quantity was remove.")
            return redirect("app1:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("app1:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("app1:product", slug=slug)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'app1/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

def subscribe(request):
    sub = Subscribe()
    if request.method == 'POST':
        sub = Subscribe(request.POST)
        subject = 'thanks'
        message = 'thank you for chossing our servies' 
        recepient = str(sub['Email'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        messages.success(request,"mail is send successfully")
        return render(request, 'app1/home.html', {'recepient': recepient})
    return render(request, 'app1/home.html', {'form':sub})