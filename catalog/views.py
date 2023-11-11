from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from catalog.models import Product, Version, Category
from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def contacts(request):
    return render(request, 'catalog/contacts.html')


def categories(request):
    key = 'category_list'
    category_list = cache.get(key)
    if category_list is None:
        category_list = Category.objects.all()
        cache.set(key, category_list)

    context = {'object_list': category_list}
    return render(request, 'catalog/category_list.html', context)



def category_products(request, pk):
    category = Category.objects.get(pk=pk)
    context = {'object_list': Product.objects.filter(category=pk),
               'category': category.name}
    return render(request, 'catalog/product_list.html', context)


# Create
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        if form.is_valid():
            product = form.save()
            product.owner = self.request.user
            product.save()
        return super().form_valid(form)


# Read
class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = False
        context['is_moderator'] = False
        if self.object.owner == self.request.user:
            context['is_owner'] = True
        if self.request.user.has_perms(['catalog.set_is_published',
                                        'catalog.change_description',
                                        'catalog.change_category']):
            context['is_moderator'] = True
        return context


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        for item in context['product_list']:
            active_version = Version.objects.filter(product=item, is_current=True).last()
            if active_version:
                item.active_version_number = active_version.version_number
            else:
                item.active_version_number = None
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset


# Update
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def test_func(self):
        is_owner = Product.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
        return is_owner

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object, )
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])


# Delete
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        is_owner = Product.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
        return is_owner


class ModeratorProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ModeratorProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        is_moderator = self.request.user.has_perms(['catalog.set_is_published',
                                                    'catalog.change_description',
                                                    'catalog.change_category'])
        return is_moderator

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object, )
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])
