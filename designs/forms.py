from django import forms
from .models import Design

class DesignForm(forms.ModelForm):
    customer = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Customer'
        })
    )
    ident = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Ident'
        })
    )
    style = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Style'
        })
    )
    length = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Length'
        })
    )
    width = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Width'
        })
    )
    depth = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Depth'
        })
    )
    test = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Test'
        })
    )
    flute = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Flute'
        })
    )
    paper = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Paper'
        })
    )
    samples_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        })
    )
    num_samples_requested = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Number of Samples Requested'
        })
    )
    ard_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        })
    )
    pdf_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        })
    )
    eps_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        })
    )
    dxf_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        })
    )
    cape_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        })
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full',
            'placeholder': 'Notes'
        })
    )
    
    
    class Meta:
        model = Design
        fields = (
        'customer','ident','style','length','width','depth',
        'test','flute','paper','samples_required','num_samples_requested',
        'ard_required','pdf_required','eps_required','dxf_required',
        'cape_required','notes',
                )
