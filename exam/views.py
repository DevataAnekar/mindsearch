from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User

from . import forms,models

import datetime
from datetime import timedelta

import xlwt
from django.http import HttpResponse

# writing to existing workbook using xlwt 
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd

import os


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'exam/update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.status=True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request,'exam/salary_form.html',{'teacherSalary':teacherSalary})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher_salary.html',{'teachers':teachers})




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_download_student_marks(request):
    students= SMODEL.Student.objects.all()



    return render(request,'exam/admin_download_student_marks.html',{'students':students})


@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'exam/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'exam/admin_course.html')


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'exam/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'exam/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})



# def export_write_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="Student1.xls"'

#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Student') # this will make a sheet named Users Data

#     st_info_header = ["User ID","User name","First name","Last name","Mobile number"]

#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     for col_num in range(len(st_info_header)):
#         ws.write(row_num, col_num, st_info_header[col_num], font_style) # at 0 row 0 column 
#     # wb.save(response)

#     student = models.Student.objects.all().values_list('mobile', 'user_id')
#     print(student)
#     for st in student:
#         row_num += 1
#         stt = []
#         # print(st[0])
#         # print(st[1])
#         rows = User.objects.all().values_list('username', 'first_name', 'last_name').filter(id=st[1])
#         for r in rows:
#             # print(r)
#             stt = [st[1], r[0],  r[1],  r[2], st[0]]

#         for col_num in range(len(stt)):
#             print(col_num)
#             stt[col_num]
#             ws.write(row_num, col_num, stt[col_num], font_style) # at 0 row 0 column 

#     wb.save(response)

#     return response



session_name = ["1. Why we get disturbed? {Brain storming}",
"2. Introduction to Self talk",
"3. Self talk examples and characteristics",
"4. Appropriate Inappropriate emotions",
"5. Appropriate Inappropriate emotions",
"6. Introduction to ABC model: Beliefs",
"7. 3 core beliefs plus beliefs of anxiety & depression",
"8. Expectation demand",
"9. Feedback Evaluation",
"10. Fact Opinion",
"11. Disputation: Cognitive",
"12. Replacing Irrational(IB) beliefs with rational beliefs(RB)",
"13. Disputation tips Emotional",
"14. Disputation tips Behavioral",
"15. Further Action plan"]



def export_write_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    student = models.Student.objects.all().values_list('mobile', 'user_id','id')

    for st in student:
        row_num = 0

        row_num += 1
        stt = []
        # print(st[0])
        # print(st[1])
        rows = User.objects.all().values_list('username', 'first_name', 'last_name').filter(id=st[1])
        for r in rows:
            # print(r)
            stt = [st[2], r[0],  r[1],  r[2], st[0]]

        ws = wb.add_sheet("User_ID_"+ str(st[2])) # this will make a sheet named Users Data

        st_info_header = ["User ID","User name","First name","Last name","Mobile number"]


        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(st_info_header)):
            ws.write(row_num, col_num, st_info_header[col_num], font_style) # at 0 row 0 column 

        row_num += 1

        for col_num in range(len(stt)):
            stt[col_num]
            ws.write(row_num, col_num, stt[col_num], font_style) # at 0 row 0 column 
# 

        st_info_header2 = ["Exam", "attempt", "Question no.", "Answer", "Marks"]

        row_num += 1
        row_num += 1

        font_style.font.bold = True

        font_style = xlwt.XFStyle()
        for col_num in range(len(st_info_header2)):
            ws.write(row_num, col_num, st_info_header2[col_num], font_style) # at 0 row 0 column 
        row_num += 1

        PPR = models.pre_post_Result.objects.all().values_list('exam', 'marks', 'marks_descriptios','student_id')
        PPR2 = []
        for ppr in PPR:
            if ppr[3] == st[2]:
                if ppr[0] == 1:
                    PPR2 = ['PreTest',1,'Frequency & Intensity',ppr[2],ppr[1]]

        for col_num in range(len(PPR2)):
            ws.write(row_num, col_num, PPR2[col_num], font_style) # at 0 row 0 column 
        row_num += 1
# 


        QA = models.Result_all_question.objects.all().values_list('exam_id', 'attempt', 'question_id', 'given_ans', 'student_id')
        qa2 = []
        for qa in QA:
            if qa[4] == st[2]:
                qa2 = [ "Session " + session_name[qa[0]-1], qa[1], qa[2], qa[3]]
                # print(qa2)
                for col_num in range(len(qa2)):
                    ws.write(row_num, col_num, qa2[col_num], font_style) # at 0 row 0 column 
                row_num += 1

# 

        PPR2 = []
        for ppr in PPR:
            if ppr[3] == st[2]:
                if ppr[0] == 2:
                    PPR2 = ['Post Test',1,'Frequency & Intensity',ppr[2],ppr[1]]

        for col_num in range(len(PPR2)):
            ws.write(row_num, col_num, PPR2[col_num], font_style) # at 0 row 0 column 

    wb.save(response)

    return response
