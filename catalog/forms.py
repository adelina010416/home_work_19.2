from django import forms
from catalog.models import Product, Version
from constants import forbidden_list


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('creation_date', 'last_change_date',)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_name = self.cleaned_data['name']
        cleaned_description = self.cleaned_data['description']

        for data in [cleaned_name, cleaned_description]:
            for word in forbidden_list:
                if word in data.lower():
                    raise forms.ValidationError('Ошибка, попытка загрузить запрещённый продукт.')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
