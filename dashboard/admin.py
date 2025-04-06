from django.contrib import admin
from .models import Category, Tag, Project
# Register your models here.
from django import forms


# class TagAdminForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ['id', 'name']
#     name = forms.CharField(max_length=20, required=True)
#
# class CategoryAdmin(admin.ModelAdmin):
#     search_fields = ['name', ]
#     list_display = ['id', 'name']
#
#
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']
#     search_fields = ['name', ]
#     form = TagAdminForm


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Project)