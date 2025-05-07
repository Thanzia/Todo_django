from django import forms
from my_app.models import User,TaskModel

class UserRegistrationForm(forms.ModelForm):

	class Meta:

		model = User

		fields = ['username','password','email']

		widgets = {
			"username":forms.TextInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter username"}),
			"password":forms.PasswordInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter password"}),
			"email":forms.EmailInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter email"})
		}

class LoginForm(forms.Form):

	username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter username"}))

	password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter password"}))

class TaskForm(forms.ModelForm):

	class Meta:

		model = TaskModel

		exclude = ['created_date','completed_status','user_id']

		widgets = {

			"task_name":forms.TextInput(attrs={"class":"form-control w-75 mx-auto"}),
			"due_date":forms.DateInput(attrs={"class":"form-control w-75 mx-auto"}),
			"description":forms.Textarea(attrs={"class":"form-control w-75 mx-auto"}),
			"task_category":forms.Select(attrs={"class":"form-select w-75 mx-auto"}),

		}

class ForgotPasswordForm(forms.Form):

	email = forms.CharField(max_length=100)

class OtpVerifyForm(forms.Form):

	otp = forms.CharField(max_length=100)

class ResetpasswordForm(forms.Form):

	password = forms.CharField(max_length=50)

	confirm_password = forms.CharField(max_length=50)

class ContactForm(forms.Form):

	user_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter username"}))

	email = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter email"}))

	subject = forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter subject"}))

	message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control w-75 mx-auto","placeholder":"enter your message here"}))