from django.db import models
from django. contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from k12exchange.settings import FILES_DIR

fs = FileSystemStorage(location=FILES_DIR)


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	email = models.EmailField()
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	USER_TYPE=(
		("Teacher","Teacher"),("Student","Student"),("Parent","Parent"))
	user_type = models.CharField(max_length=10, choices=USER_TYPE)
	school = models.CharField(max_length=50)
	GRADE_TYPE = (
		("kindergarten","kindergarten"),("elementary_school","elementary_school"),\
		 ("middle_school","middle_school"),("high_school","high_school"))
	grade = models.CharField(max_length=20, choices=GRADE_TYPE)
	SCHOOL_TYPE = (
		("private","private"),("public","public"),("charter","charter"))
	school_type = models.CharField(max_length=10, choices=SCHOOL_TYPE)
	GEO_TYPE = (
		("urban","urban"),("suburb","suburb"),("rural","rural"))
	geography = models.CharField(max_length=10, choices=GEO_TYPE)
	city = models.CharField(max_length=15)
	state = models.CharField(max_length=15)
	picture = models.ImageField(upload_to="profile_images", blank = True, null=True)
	introduction = models.TextField(blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user = u)[0])

class Material(models.Model):
	name = models.CharField(max_length=100)
	uploader = models.ForeignKey('UserProfile', blank=True, null=True)
	author = models.CharField(max_length=30)
	CATE_CHOICES = (
		("Presentation","Presentation"),("In-Class_Work","In-Class_Work"),\
		("Homework","Homework"),("Game","Game"),("Test","Test"))
	category = models.CharField(max_length=15, choices=CATE_CHOICES)
	TYPE_CHOICES = (("original","original"),("updated","updated"))
	upload_type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True)
	doc = models.FileField(storage=fs, blank = True, null=True)
	upload_date = models.DateTimeField(default=datetime.now)
	create_date = models.DateTimeField(default=datetime.now)
   	description = models.TextField()
	GRADE_TYPE = (
		("kindergarten","kindergarten"),("elementary_school","elementary_school"),\
		 ("middle_school","middle_school"),("high_school","high_school"))
	grade = models.CharField(max_length=20, choices=GRADE_TYPE)
	year = models.IntegerField(default=1, validators=[MinValueValidator(1)])
   	subject = models.CharField(max_length=20)
   	class_size = models.IntegerField(default=30, validators=[MinValueValidator(0)])
   	tags = models.CharField(max_length=100)
   	liked_by = models.ManyToManyField('UserProfile', null=True, related_name="liked_by")

class Rating(models.Model):
	rater = models.ForeignKey('UserProfile', related_name='rater', blank=True, null=True)
	rated = models.ForeignKey('UserProfile', related_name='rated', blank=True, null=True)
	material = models.ForeignKey('Material', blank=True, null=True)
	rate = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1),MaxValueValidator(5)])
	comment = models.TextField(blank=True, null=True)
	time = models.DateTimeField(default=datetime.now)

class Search(models.Model):
	user = models.ForeignKey("UserProfile", null=True, blank = True) 
	term = models.CharField(max_length=50, null = True, blank = True)
	CATE_CHOICES=(("Presentation","Presentation"),("In-Class_Work","In-Class_Work"),\
		("Homework","Homework"),("Game","Game"),("Test","Test"))
	category = models.CharField(max_length=15, choices=CATE_CHOICES, null=True)
	# class_size = models.IntegerField(default=30, validators=[MinValueValidator(0)])
	# subject = models.CharField(max_length=20)
	# grade = models.CharField(max_length=20, choices=GRADE_TYPE)
	# GRADE_TYPE = (
	#  	("kindergarten","kindergarten"),("elementary_school","elementary_school"),\
	#	 ("middle_school","middle_school"),("high_school","high_school"))
	# year = models.IntegerField(default=1, validators=[MinValueValidator(1)])
	time = models.DateTimeField(default=datetime.now)

class Download(models.Model):
	user = models.ForeignKey("UserProfile", null=True, blank = True)
	material = models.ForeignKey('Material', blank=True, null=True)
	time = models.DateTimeField(default=datetime.now)

class Message(models.Model):
	sender = models.ForeignKey("UserProfile", related_name='sender', null=True, blank = True)
	receiver = models.ForeignKey("UserProfile", related_name='receiver', null=True, blank = True)
	text = models.TextField(blank=True, null=True)
	time = models.DateTimeField(default = datetime.now)