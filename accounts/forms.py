from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title','body', 'keyword','num_word','typ_content','level_content']

class UploadFileForm(forms.Form):
    file = forms.FileField()
    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            order.save()
        return order



