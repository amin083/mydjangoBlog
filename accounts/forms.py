from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title','body', 'keyword']

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            order.save()
        return order



