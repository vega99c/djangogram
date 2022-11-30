from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('', views.main, name='main'),
    #회원가입 페이지 등록
    path('signup/', views.signup, name='signup')
]
