from django import forms
from models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    user_type = forms.ChoiceField(label="I am a",choices=[("","----"),("Teacher","Teacher"),("Student","Student"),("Parent","Parent")])
    school = forms.CharField(label="Name of School (Parents: enter the school your kids attend)")
    grade = forms.ChoiceField(label="School Level", choices=[("","----"),("kindergarten","kindergarten"),("elementary_school","elementary_school"),\
		 ("middle_school","middle_school"),("high_school","high_school")])
    school_type = forms.ChoiceField(label="School Type", choices=[("","----"),("private","private"),("public","public"),("charter","charter")])
    geography = forms.ChoiceField(choices=[("","----"),("urban","urban"),("suburb","suburb"),("rural","rural")], required=False)
    city = forms.CharField()
    state = forms.CharField()
    profile_picture = forms.ImageField()
    introduction = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name","last_name","password1",\
            "password2","email","user_type","school","grade","school_type","geography",\
            "city","state","introduction", "profile_picture")

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserCreateForm, self).save(commit=True)
        user_profile = UserProfile(user=user, email=self.cleaned_data["email"], \
            first_name=self.cleaned_data["first_name"], last_name=self.cleaned_data["last_name"], \
            user_type=self.cleaned_data["user_type"], school=self.cleaned_data["school"],\
            grade=self.cleaned_data["grade"], school_type=self.cleaned_data["school_type"],\
            geography=self.cleaned_data["geography"],city=self.cleaned_data["city"],
            state=self.cleaned_data["state"],introduction=self.cleaned_data["introduction"],\
            picture = self.cleaned_data["profile_picture"])
        user_profile.save()
        return user, user_profile


class UserModifyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["school","grade","school_type","geography","city",\
            "state","introduction"]

class AddMaterialForm(forms.ModelForm):
    author = forms.CharField(label="Author (If you, write your own name.)", required=False)
    create_date = forms.DateTimeField(label="Date of Creation (eg.2015-04-10 02:46:07)")
    tags = forms.CharField(label="Tags (eg. math, linear algebra, matrix, Cramer's rule)")
    grade = forms.ChoiceField(label="School Level", choices=[("","----"),("kindergarten","kindergarten"),("elementary_school","elementary_school"),\
		 ("middle_school","middle_school"),("high_school","high_school")])
    category = forms.ChoiceField(choices=[("","----"),("Presentation","Presentation"),("In-Class_Work","In-Class_Work"),\
		("Homework","Homework"),("Game","Game"),("Test","Test")])
    doc = forms.FileField(label="File (Please upload editable files if possible.)")
    class Meta:
        model = Material
        fields = ['name','author','category','upload_type','create_date','subject','description','tags',\
        'grade','year','class_size','doc']

class SearchForm(forms.ModelForm):
	term = forms.CharField(label="Key Words")
	class Meta:
		model = Search
		fields = ["term","category"]

class RateForm(forms.ModelForm):
    rate = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Rating
        fields = ["rate", "comment"]

class MessageForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Message
        fields = ["text"]