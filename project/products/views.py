# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden, HttpResponseNotAllowed
# from .models import Product
# from .forms import ProductForm
# from django.views.generic import ListView, DetailView, CreateView, UpdateView     
# from django.db.models import Q
# from django.views.generic import ListView
# from .models import Product
# from .mixins import QueryParamsMixin
# from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .models import Product
from .forms import ProductForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView     # *



# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'products/product_list.html', {'products': products})

#  ListView - objectebis listios chveneba 
from django.db.models import Q
from django.views.generic import ListView
from .models import Product
from .mixins import QueryParamsMixin
from django.conf import settings

class ProductListView(ListView, QueryParamsMixin):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if query:
            queryset = queryset.filter(Q(name__icontains=query))

        if category:
            queryset = queryset.filter(category__name=category)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # orderingi
        order_by = self.request.GET.get('order_by')  #price, name, id 
        if order_by in ['name', '-name', 'price', '-price', 'id', '-id']:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('id')
        return queryset



class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

# ---------------------------------------------------------------------------------------------------------------------------
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# CreateView - axali objectis sheqmna
class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




class AdminUpdateProductView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/admin_update_product.html'
    context_object_name = 'product'

    # 
    def post(self, request, *args, **kwargs):
        method = request.POST.get('_method', '').upper()
        if method != 'PUT':
            return HttpResponseNotAllowed(['PUT'])  
        return super().post(request, *args, **kwargs)
    
    
    def test_func(self):
        return self.request.user.is_superuser
    
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden('only admin can change the product')
        return super().handle_no_permission()
    
    def get_success_url(self):   
        return reverse_lazy('product_detail', kwargs = {'pk': self.object.pk} )
    

