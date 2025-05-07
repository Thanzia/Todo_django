"""
URL configuration for Todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
	path('',IndexView.as_view(),name="indexview"),
	path('todo/signup',UserRegistrationView.as_view(),name="signup"),
	path('login/',LoginView.as_view(),name="login"),
	path('logout/',LogoutView.as_view(),name="logout"),
	path('todo/forgotpwd/',ForgotPasswordView.as_view(),name="forgot"),
	path('task/create/',AddTaskView.as_view(),name="create"),
	path('task/list/',TaskReadView.as_view(),name="task_list"),
	path('task/update/<int:pk>',TaskUpdateView.as_view(),name="update"),
	path('task/delete/<int:pk>',TaskDeleteView.as_view(),name="delete"),
    path('task/detail/<int:pk>',TaskDetailView.as_view(),name="detail"),
	path('task/edit/<int:pk>',TaskEditView.as_view(),name="edit"),
	path('todo/otp_verify/',OtpVerifyView.as_view(),name="otp_verify"),
	path('todo/reset_pwd/',ResetPasswordView.as_view(),name="reset_pwd"),
	path('todo/filter/',TaskFilterView.as_view(),name="filter"),
	path('todo/contact/',ContactView.as_view(),name="contact"),
	
]
