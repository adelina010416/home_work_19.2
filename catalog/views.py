from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from catalog.models import Product, Version
from catalog.forms import ProductForm, VersionForm


def contacts(request):
    return render(request, 'catalog/contacts.html')


# Create
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')


# Read
class ProductDetailView(DetailView):
    model = Product


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


# Update
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

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
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
