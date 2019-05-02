from django import forms
from django.utils.translation import ugettext_lazy as _

from django_comments_xtd.forms import XtdCommentForm
from django_comments_xtd.models import TmpXtdComment


class BookSearchForm(forms.Form):
    search_field = forms.CharField(
        label='Search for book title:', max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Any book info...',
            'class': 'form-control',
        })
    )


class BookCommentsForm(XtdCommentForm):
    avatar = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': _('avatar')})
    )

    def get_comment_create_data(self, *args, **kwargs):
        data = super(BookCommentsForm, self).get_comment_create_data(*args, **kwargs)
        print(self.user)
        print(data)
        return data
