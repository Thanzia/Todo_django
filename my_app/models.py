from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# 1.user table
# username,password,email
# import from contrib.auth.models


# 2..taskmodel
class TaskModel(models.Model):

	task_name = models.CharField(max_length=100)

	created_date = models.DateField(auto_now_add=True)

	due_date = models.DateField()   # yyyy-mm-dd

	description = models.TextField(null=True,blank=True) # make it optional

	category = [
		('work','work'),
		('personal','personal'),  # tuples 2 values one to enter table and 
		('urgent','urgent')
	]

	task_category = models.CharField(max_length=100,choices=category)

	completed_status = models.BooleanField(default=False)

	user_id = models.ForeignKey(User,on_delete=models.CASCADE)  
	# one to many relation by default  (User -->> TaskModel)

	def __str__(self):
		return self.task_name     # to see the taskname in html page
	
class OtpModel(models.Model):

	user_id = models.ForeignKey(User,on_delete=models.CASCADE)
	# one user can do forgot password many times (one to many relation)

	otp = models.CharField(max_length=100)

	created_at = models.DateField(auto_now_add=True)



