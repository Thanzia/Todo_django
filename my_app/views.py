from django.shortcuts import render,redirect
from django.views.generic import View
from my_app.forms import *
from my_app.models import User,TaskModel,OtpModel
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import random

# Create your views here.
# decorators -allow to do a new functionality to an existing object without modifying its structure
# the id given thru url is the id of taskmodel
# this id should be the taskid of the loginned user it is checked using deco
# by using deco we can utilize this in update,delete,read view instead of writing in all views

def is_user(fn):

	def wrapper(request,**kwargs):

		id = kwargs.get("pk")

		item = TaskModel.objects.get(id = id)  # we get taskmodel object which contain all infmn

		if item.user_id == request.user:

			return fn(request,**kwargs)
		
		return redirect("login")
	    
	return wrapper
	


# registration,login,addtask,read task,delete task,task update,logout,forgot password,welcome page

class UserRegistrationView(View):
	
	def get(self,request):

		form = UserRegistrationForm

		return render(request,"signup.html",{"form":form})
	
	def post(self,request):

		form = UserRegistrationForm(request.POST)

		if form.is_valid():

			print(form.cleaned_data)

			username = form.cleaned_data.get('username')

			password = form.cleaned_data.get('password')

			email = form.cleaned_data.get('email')

			User.objects.create_user(username=username,password=password,email=email)

			# User.objects.create_user(**form.cleaned_data)

		# form = UserRegistrationForm

		# return render(request,"signup.html",{"form":form})

		return redirect("login")


# LoginView -->> username,password
# methods ->> get,post

class LoginView(View):

	def get(self,request):

		form = LoginForm

		return render(request,"login.html",{"form":form})
	
	def post(self,request):

		form = LoginForm(request.POST)

		if form.is_valid():

			username = form.cleaned_data.get('username')

			password = form.cleaned_data.get('password')

			user_obj = authenticate(request,username=username,password=password)

			if user_obj:

				login(request,user_obj)
				
				return render(request,"index.html")
			
			else:

				form = LoginForm

				return render(request,"login.html",{"form":form})
			
# logoutView
# methods: get
class LogoutView(View):

	def get(self,request):

		logout(request)

		return redirect("login")

# task_add,add,delete,update(CRUD)

# to add a task
# lh:8000/task/create/
# methods: get,post
# taskname,duedate(yyyy-mm-dd),description,taskcategory


class AddTaskView(View):

	def get(self,request):

		form = TaskForm

		return render(request,"addtask.html",{"form":form})
	
	def post(self,request):

		form = TaskForm(request.POST)

		if form.is_valid():

			TaskModel.objects.create(user_id=request.user,**form.cleaned_data)

		form = TaskForm

		return render(request,"addtask.html",{"form":form})
	
# ReadView
# methods: get
# lh:8000/task/read/

@method_decorator(login_required,name="dispatch")
class TaskReadView(View):

	def get(self,request):

		# items = TaskModel.objects.all()  # collection of all objects in the table taskmodel

		items = TaskModel.objects.filter(user_id = request.user)   # to get the tasks of a loginned user alone

		# print(items)

		# print(request.user)
			
		return render(request,"tasklist.html",{"items":items})
		
		

	
	
# UpdateView
# methods:get,post
# lh:8000/task/update/<int:pk>
@method_decorator(decorator=is_user,name="dispatch")
class TaskUpdateView(View):

	def get(self,request,**kwargs):        # kwargs = {'pk':1}

		id = kwargs.get('pk')

		item = TaskModel.objects.get(id=id)

		form = TaskForm(instance=item)

		return render(request,"update.html",{"form":form})
	
	def post(self,request,**kwargs):

		id = kwargs.get('pk')

		item = TaskModel.objects.get(id=id)

		form = TaskForm(request.POST,instance=item)

		if form.is_valid():

			form.save()

		form = TaskForm

		return render(request,"update.html",{"form":form})
	
# deleteView
# methods: get
# lh:8000/task/delete/<int:pk>
@method_decorator(decorator=is_user,name="dispatch")
class TaskDeleteView(View):

	def get(self,request,**kwargs):

		id = kwargs.get('pk')

		TaskModel.objects.get(id=id).delete()

		return redirect("task_list")
	
# to read a specific task
# methods: get
# lh:8000/task/detail/<int:pk>

@method_decorator(decorator=is_user,name="dispatch")
class TaskDetailView(View):

	def get(self,request,**kwargs):

		id = kwargs.get("pk")

		item = TaskModel.objects.get(id=id)
		# print(item)

		return render(request,"detail.html",{"item":item})
	
# to edit completed_status
# methods: get
# lh:8000/task/edit/<int:pk>
class TaskEditView(View):

	def get(self,request,**kwargs):

		id = kwargs.get("pk")

		data = TaskModel.objects.get(id=id)

		data.completed_status = True

		data.save()

		return redirect("task_list")

# forgot passwordView
# methods:get,post
class ForgotPasswordView(View):

	def get(self,request):

		form = ForgotPasswordForm

		return render(request,"forgotpwd.html",{"form":form})
	
	def post(self,request):

		form = ForgotPasswordForm(request.POST)

		if form.is_valid():

			email = form.cleaned_data.get('email')

			user = User.objects.get(email=email)  # (email field in model User given in forgotpwdform = field get in the above step)

			otp = random.randint(1000,9999)

			OtpModel.objects.create(user_id=user,otp=otp)

			# wisu xnqp qllk mxls >> app password(key) 
			# send_email via smtp protocol
			send_mail(subject="Otp for password reset",message=str(otp),from_email="thanzia123@gmail.com",
			          recipient_list=[email])
			
			return redirect("otp_verify")
			
		return render(request,"forgotpwd.html",{"form":form})


# otp verify page
class OtpVerifyView(View):

	def get(self,request):

		form = OtpVerifyForm

		return render(request,"otpverify.html",{"form":form})
	
	def post(self,request):

		form = OtpVerifyForm(request.POST) 
		
		if form.is_valid():
			
			otp = form.cleaned_data.get('otp')
			
			item = OtpModel.objects.get(otp=otp)  # id otp user_id(form user fk)

			user_id = item.user_id

			user = User.objects.get(id=user_id.id)

			username = user.username
			
			if item:
				
				# name = User.objects.get('item')
				
				request.session['user'] = username
				
				return redirect("reset_pwd")
		
		return render(request,"otpverify.html",{"form":form})

class ResetPasswordView(View):

	def get(self,request):

		form = ResetpasswordForm

		return render(request,"resetpwd.html",{"form":form})

	def post(self,request):

		form = ResetpasswordForm(request.POST)

		if form.is_valid():

			password = form.cleaned_data.get('password')

			confirm_password = form.cleaned_data.get('confirm_password')

			if password == confirm_password:

				username = request.session.get('user')

				user = User.objects.get(username=username)

				user.set_password(password)

				user.save()

				return redirect("login")
		
		return render(request,"resetpwd.html",{"form":form})

# Filtering
# methods: get
# lh:8000/task/filter_category

class TaskFilterView(View):

	def get(self,request):

		category = request.GET.get('category')   # from html page get the data along url (query parameter)

		Task = TaskModel.objects.filter(user_id=request.user)

		tasks = Task.filter(task_category = category)

		return render(request,"filter.html",{"tasks":tasks})
	
class IndexView(View):

	def get(self,request):

		return render(request,"indexview.html")

# view for Contact
# methods:get,post

class ContactView(View):

	def get (self,request):

		form = ContactForm

		return render(request,"contact.html",{"form":form})

	def post(self,request):

		form = ContactForm(request.POST)

		return render(request,"contact.html",{"form":form})




