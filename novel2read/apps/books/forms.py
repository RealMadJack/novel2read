from django import forms


class BookSearchForm(forms.Form):
    search_field = forms.CharField(
        label='Search for book title:', max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Any book info...',
            'class': 'form-control',
        })
    )
