from django import forms
from django_summernote.widgets import SummernoteWidget

from common.forms import BaseForm
from .models import Asset


class AssetCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Asset
        exclude = ('date_added', 'date_updated', 'created_by', 'last_modified_by')
        widgets = {
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', }}),
            # 'retirement_reason': SummernoteWidget(attrs={'summernote': {'width': '100%', }}),
        }


class AssetUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Asset
        exclude = ('date_added', 'date_updated', 'created_by', 'last_modified_by')
        widgets = {
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', }}),
            # 'retirement_reason': SummernoteWidget(attrs={'summernote': {'width': '100%', }}),
        }
