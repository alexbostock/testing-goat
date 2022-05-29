from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR_MESSAGE = 'List item must not be empty'

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR_MESSAGE}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
