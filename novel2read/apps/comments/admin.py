from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_comments_xtd.admin import XtdCommentsAdmin
from .models import BasicComment


class BasicCommentAdmin(XtdCommentsAdmin):
    list_display = ('thread_level', 'user_avatar', 'cid', 'name', 'content_type',
                    'object_pk', 'submit_date', 'followup', 'is_public',
                    'is_removed')
    list_display_links = ('cid', )
    fieldsets = (
        (None, {'fields': ('content_type', 'object_pk', 'site')}),
        (_('Content'), {'fields': ('title', 'user', 'user_name', 'user_avatar', 'user_email', 'user_url', 'comment', 'followup')}),
        (_('Metadata'), {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}),
    )


admin.site.register(BasicComment, BasicCommentAdmin)
