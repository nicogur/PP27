from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .models import Product
from .forms import ProductForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView     
from django.db.models import Q
from django.views.generic import ListView
from .models import Product



class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 2

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

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        if "page" in query_params:   
            query_params.pop("page")
        context["query_params"] = query_params.urlencode()
        return context


        



class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

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
    



