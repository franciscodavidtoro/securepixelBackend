
# Register your models here.
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Tema

admin.site.register(Tema, MarkdownxModelAdmin)  