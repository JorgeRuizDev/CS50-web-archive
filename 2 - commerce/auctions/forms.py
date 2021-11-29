from django.forms import forms
from django.forms import ModelForm
from django import forms
from .models import Bid, Category, Item, Comment

from .util import get_max_bid


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = [
            'ammount'
        ]

    def __init__(self, *args, **kwargs):
        self.item_id = kwargs.pop("item_id")
        super(NewBidForm, self).__init__(*args, **kwargs)

    bidder = None
    item = None

    def clean_ammount(self):
        ammount = self.cleaned_data['ammount']

        if ammount <= get_max_bid(self.item_id):
            raise forms.ValidationError(message="Bid ammount is lower than the maximun bid.")
        else:
            return ammount


class NewCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean(self):
        print(self.cleaned_data)
        if Category.objects.filter(name=self.cleaned_data.get("name")):
            raise forms.ValidationError(message="Category already exists")
        if len(self.cleaned_data.get("name")) is 0:
            raise forms.ValidationError(message="field is empty")

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(NewCategoryForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['name'].required = False

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_name',
                  'image',
                  'min_bid',
                  'categories',
                  ]

    # Extra fields:
    item_description = forms.CharField(widget=forms.Textarea, max_length=4000)
    owner = None
    is_active = True
    date = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        item_name = self.cleaned_data['item_name']

        if (len(item_name) < 3):
            raise forms.ValidationError(message="Item name must contain at least three characters")

        item_description = self.cleaned_data['item_description']

        min_bid = self.cleaned_data['min_bid']

        if min_bid < 1.0:
            raise forms.ValidationError(message="Min bid must be at least USD 1")

class NewCommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = [
            'item',
            'comment'
        ]
    comment = forms.CharField(widget=forms.Textarea, max_length=4000)

    def clean(self):

        if not self.cleaned_data.get("item"):
            raise forms.ValidationError(message="The item does not exist")

        item_id = self.cleaned_data.get("item").id

        if not Item.objects.filter(id=item_id):
            raise forms.ValidationError(message="The item does not exist")

        if len(self.cleaned_data.get("comment")) <= 0:
            raise forms.ValidationError(message="there is no comment")

