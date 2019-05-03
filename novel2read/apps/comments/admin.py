from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_comments_xtd.admin import XtdCommentsAdmin
from .models import CustomComment


class CustomCommentAdmin(XtdCommentsAdmin):
    list_display = ('thread_level', 'user_avatar', 'cid', 'name', 'content_type',
                    'object_pk', 'submit_date', 'followup', 'is_public',
                    'is_removed')
    list_display_links = ('cid', 'user_avatar', )
    fieldsets = (
        (None, {'fields': ('content_type', 'object_pk', 'site')}),
        (_('Content'), {'fields': ('user', 'user_name', 'user_avatar', 'user_email', 'user_url', 'comment', 'followup')}),
        (_('Metadata'), {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}),
    )


admin.site.register(CustomComment, CustomCommentAdmin)
