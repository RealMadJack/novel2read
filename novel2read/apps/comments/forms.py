from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from django_comments_xtd.forms import XtdCommentForm
from django_comments_xtd.models import TmpXtdComment

User = get_user_model()


class BasicCommentForm(XtdCommentForm):
    user_avatar = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': _('avatar')})
    )

    def get_comment_create_data(self, **kwargs):
        data = super(BasicCommentForm, self).get_comment_create_data(**kwargs)
        try:
            user = User.objects.get(email=data['user_email'])
            data.update({
                'user_name': user.username,
                'user_avatar': user.profile.avatar,
            })
        except User.DoesNotExist:
            data.update({
                'user_name': data.get('user_name', 'Guest'),
                'user_avatar': 'users/default.png',
            })
        return data
