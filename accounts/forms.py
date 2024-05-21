from django import forms
from django.shortcuts import get_object_or_404

from .models import Order
from .models import Document

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title','body', 'keyword','num_word','typ_content','level_content', 'admin_uploade_file']
        def get_initial(self):
            initial = super().get_initial()
            order = get_object_or_404(Order, id=self.data['order_id'])
            initial['title'] = order.title
            initial['body'] = order.body
            initial['keyword'] = order.keyword
            initial['num_word'] = order.num_word
            initial['typ_content'] = order.typ_content
            initial['level_content'] = order.level_content
            return initial

        def save(self, commit=True):
            order = super().save(commit=False)
            if commit:
                order.save()
            return order


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['id', 'title', 'uploaded_file']
        # readonly_fields = ['date']  # اضافه کردن فیلد readonly
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance and self.instance.date:
    #         self.fields['date'].widget.attrs['readonly'] = True
        # def save(self, commit=True):
        #     Document = super().save(commit=False)
        #     if commit:
        #         Document.save()
        #     return Document


class WordFileUploadForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['admin_uploade_file']


class WordFileUploadForm_document(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['admin_uploade_file']