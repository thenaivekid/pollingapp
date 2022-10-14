from django.contrib import admin

from .models import Question,Choice
# Register your models here.
class MyAdminSite(admin.AdminSite):
    site_header= "Polls Admininstration"

admin_site = MyAdminSite(name="myadmin")

class ChoiceInline(admin.TabularInline):
    model= Choice
    extra=2
    
    
class QuestionAdmin(admin.ModelAdmin):
    list_display=("question_text","id","opened","pub_date","was_published_recently")
    fieldsets= [
        ("Question",  {'fields': ['question_text']}),
        ("Status",{'fields': ['opened']}),
        ("Published Date", {'fields':['pub_date']}),
    ] 
    inlines= [ChoiceInline]
    list_filter = ['pub_date','opened']
    search_fields = ['question_text']

class ChoiceAdmin(admin.ModelAdmin):
    list_display=("id","question","choice_text","vote")

admin_site.register(Question,QuestionAdmin)
admin_site.register(Choice,ChoiceAdmin)