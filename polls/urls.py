from django.urls import path 
from . import views


app_name= 'polls'
urlpatterns =[
    path('',views.index,name="index"),
    path('allpolls/',views.allpolls, name="allpolls"),
    path('<int:question_id>/',views.detail,name="detail"),
    path('<int:question_id>/vote/',views.vote,name="vote"),
    path('<int:question_id>/result/',views.result,name="result"),
    path('search/',views.search,name="search"),
]