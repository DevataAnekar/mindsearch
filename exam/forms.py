from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class CourseForm(forms.Form):
    course_name = forms.CharField(max_length=50)
    question_number = forms.IntegerField()
    total_marks = forms.IntegerField()
    video_path = forms.FileField()


class QuestionForm(forms.ModelForm):
    
    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class All_QuestionForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.All_Type_Question
        fields=['question','correct_ans','sample_ans']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 5, 'cols': 50})
        }
