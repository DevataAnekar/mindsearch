from django.db import models

from student.models import Student
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   video_path = models.CharField(max_length=50,null=True)
   def __str__(self):
        return self.course_name


class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class All_Type_Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    question=models.CharField(max_length=1500)
    correct_ans=models.CharField(max_length=600)
    sample_ans=models.CharField(max_length=600)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class pre_post_Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam =  models.PositiveIntegerField() # 1=pre test / 2=post test
    marks = models.PositiveIntegerField()
    marks_descriptios = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)

class Result_question(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    actual_ans=models.CharField(max_length=500)
    given_ans=models.CharField(max_length=500)
    attempt = models.CharField(max_length=10)


class Result_all_question(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    question = models.ForeignKey(All_Type_Question,on_delete=models.CASCADE)
    given_ans=models.CharField(max_length=500)
    attempt = models.CharField(max_length=10)
    face_emotion = models.CharField(max_length=500)
    comment = models.CharField(max_length=500)
