from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
import datetime
from datetime import timedelta

# import emotion_recognition
import check_sentiment
import check_Match_the_pair
import check_answer

#for showing signup/login button for student

def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def mcq1(request):
    if request.method == 'GET':
        return render(request,'student/mcq1.html')
    else:

        mark_description = ''

        QF = [request.POST['qf1'], request.POST['qf2'], request.POST['qf3'], request.POST['qf4'], request.POST['qf5'], request.POST['qf6'], request.POST['qf7'], request.POST['qf8'], request.POST['qf9'], request.POST['qf10'] ,
        request.POST['qf11'], request.POST['qf12'], request.POST['qf13'], request.POST['qf14'], request.POST['qf15'], request.POST['qf16'], request.POST['qf17'], request.POST['qf18'], request.POST['qf19'], request.POST['qf20'], 
        request.POST['qf21'], request.POST['qf22'], request.POST['qf23'], request.POST['qf24'], request.POST['qf25'], request.POST['qf26'], request.POST['qf27'], request.POST['qf28'], request.POST['qf29'], request.POST['qf30'], 
        request.POST['qf31'], request.POST['qf32'], request.POST['qf33'], request.POST['qf34'], request.POST['qf35'], request.POST['qf36'], request.POST['qf37'], request.POST['qf38'], request.POST['qf39'], request.POST['qf40'],
        request.POST['qf41'], request.POST['qf42'], request.POST['qf43'], request.POST['qf44'], request.POST['qf45'], request.POST['qf46'], request.POST['qf47'], request.POST['qf48'], request.POST['qf49'], request.POST['qf50'], request.POST['qf51']  ]

        for q in QF:
            mark_description += q

        QF = list(map(int, QF))
        print(QF)
        
        QI = [request.POST['qi1'], request.POST['qi2'], request.POST['qi3'], request.POST['qi4'], request.POST['qi5'], request.POST['qi6'], request.POST['qi7'], request.POST['qi8'], request.POST['qi9'], request.POST['qi10'],
        request.POST['qi11'], request.POST['qi12'], request.POST['qi13'], request.POST['qi14'], request.POST['qi15'], request.POST['qi16'], request.POST['qi17'], request.POST['qi18'], request.POST['qi19'], request.POST['qi20'],
        request.POST['qi21'], request.POST['qi22'], request.POST['qi23'], request.POST['qi24'], request.POST['qi25'], request.POST['qi26'], request.POST['qi27'], request.POST['qi28'], request.POST['qi29'], request.POST['qi30'],
        request.POST['qi31'], request.POST['qi32'], request.POST['qi33'], request.POST['qi34'], request.POST['qi35'], request.POST['qi36'], request.POST['qi37'], request.POST['qi38'], request.POST['qi39'], request.POST['qi40'],
        request.POST['qi41'], request.POST['qi42'], request.POST['qi43'], request.POST['qi44'], request.POST['qi45'], request.POST['qi46'], request.POST['qi47'], request.POST['qi48'], request.POST['qi49'], request.POST['qi50'], request.POST['qi51']  ]
        for q in QI:
            mark_description += q

        QI = list(map(int, QI))
        print(QI)

        Depression_que  = [6,11,24,26,31,50,21,41,46]
        depression_freq = []
        depression_intensity = []
        for d in Depression_que:
            depression_freq.append(QF[d-1])
            depression_intensity.append(QI[d-1])


        Anxiety_que     = [37,42,17,22,12,15,47,27]
        Anxiety_freq = []
        Anxiety_intensity = []
        for d in Anxiety_que:
            Anxiety_freq.append(QF[d-1])
            Anxiety_intensity.append(QI[d-1])

        depression_freq_mark = sum(depression_freq)
        depression_intensity_mark = sum(depression_intensity)
        Anxiety_freq_mark = sum(Anxiety_freq)
        Anxiety_intensity_mark = sum(Anxiety_intensity)


        num = 100000000
        marks = num + depression_freq_mark*1000000 + depression_intensity_mark*10000 + Anxiety_freq_mark*100 + Anxiety_intensity_mark
        print("You Score is : ",marks)

        courses=QMODEL.Course.objects.all()
        student = models.Student.objects.get(user_id=request.user.id)
        results= QMODEL.Result.objects.all().filter(student=student)
        attempted_exams = []

        try:
            for r in results:
                attempted_exams.append(r.exam_id)
            highest_attempted_exam = max(attempted_exams)
        except:
            highest_attempted_exam = 0


        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.pre_post_Result()
        result.student=student
        result.exam=1
        result.marks=marks
        result.marks_descriptios=mark_description
        result.save()

        return HttpResponseRedirect('student-exam')
        # return render(request,'student/student_exam.html',{'courses':courses,'highest_attempted_exam':highest_attempted_exam+1})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def mcq2(request):
    if request.method == 'GET':
        return render(request,'student/mcq2.html')
    else:

        mark_description = ''

        QF = [request.POST['qf1'], request.POST['qf2'], request.POST['qf3'], request.POST['qf4'], request.POST['qf5'], request.POST['qf6'], request.POST['qf7'], request.POST['qf8'], request.POST['qf9'], request.POST['qf10'] ,
        request.POST['qf11'], request.POST['qf12'], request.POST['qf13'], request.POST['qf14'], request.POST['qf15'], request.POST['qf16'], request.POST['qf17'], request.POST['qf18'], request.POST['qf19'], request.POST['qf20'], 
        request.POST['qf21'], request.POST['qf22'], request.POST['qf23'], request.POST['qf24'], request.POST['qf25'], request.POST['qf26'], request.POST['qf27'], request.POST['qf28'], request.POST['qf29'], request.POST['qf30'], 
        request.POST['qf31'], request.POST['qf32'], request.POST['qf33'], request.POST['qf34'], request.POST['qf35'], request.POST['qf36'], request.POST['qf37'], request.POST['qf38'], request.POST['qf39'], request.POST['qf40'],
        request.POST['qf41'], request.POST['qf42'], request.POST['qf43'], request.POST['qf44'], request.POST['qf45'], request.POST['qf46'], request.POST['qf47'], request.POST['qf48'], request.POST['qf49'], request.POST['qf50'], request.POST['qf51']  ]

        for q in QF:
            mark_description += q

        QF = list(map(int, QF))
        print(QF)
        
        QI = [request.POST['qi1'], request.POST['qi2'], request.POST['qi3'], request.POST['qi4'], request.POST['qi5'], request.POST['qi6'], request.POST['qi7'], request.POST['qi8'], request.POST['qi9'], request.POST['qi10'],
        request.POST['qi11'], request.POST['qi12'], request.POST['qi13'], request.POST['qi14'], request.POST['qi15'], request.POST['qi16'], request.POST['qi17'], request.POST['qi18'], request.POST['qi19'], request.POST['qi20'],
        request.POST['qi21'], request.POST['qi22'], request.POST['qi23'], request.POST['qi24'], request.POST['qi25'], request.POST['qi26'], request.POST['qi27'], request.POST['qi28'], request.POST['qi29'], request.POST['qi30'],
        request.POST['qi31'], request.POST['qi32'], request.POST['qi33'], request.POST['qi34'], request.POST['qi35'], request.POST['qi36'], request.POST['qi37'], request.POST['qi38'], request.POST['qi39'], request.POST['qi40'],
        request.POST['qi41'], request.POST['qi42'], request.POST['qi43'], request.POST['qi44'], request.POST['qi45'], request.POST['qi46'], request.POST['qi47'], request.POST['qi48'], request.POST['qi49'], request.POST['qi50'], request.POST['qi51']  ]
        for q in QI:
            mark_description += q

        QI = list(map(int, QI))
        print(QI)

        Depression_que  = [6,11,24,26,31,50,21,41,46]
        depression_freq = []
        depression_intensity = []
        for d in Depression_que:
            depression_freq.append(QF[d-1])
            depression_intensity.append(QI[d-1])


        Anxiety_que     = [37,42,17,22,12,15,47,27]
        Anxiety_freq = []
        Anxiety_intensity = []
        for d in Anxiety_que:
            Anxiety_freq.append(QF[d-1])
            Anxiety_intensity.append(QI[d-1])

        depression_freq_mark = sum(depression_freq)
        depression_intensity_mark = sum(depression_intensity)
        Anxiety_freq_mark = sum(Anxiety_freq)
        Anxiety_intensity_mark = sum(Anxiety_intensity)

        num = 100000000
        marks = num + depression_freq_mark*1000000 + depression_intensity_mark*10000 + Anxiety_freq_mark*100 + Anxiety_intensity_mark
        print("You Score is : ",marks)

        courses=QMODEL.Course.objects.all()
        student = models.Student.objects.get(user_id=request.user.id)
        results= QMODEL.Result.objects.all().filter(student=student)
        attempted_exams = []

        try:
            for r in results:
                attempted_exams.append(r.exam_id)
            highest_attempted_exam = max(attempted_exams)
        except:
            highest_attempted_exam = 0

        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.pre_post_Result()
        result.student=student
        result.exam=2
        result.marks=marks
        result.marks_descriptios=mark_description
        result.save()
        return HttpResponseRedirect('student-exam')
        # return render(request,'student/student_exam.html',{'courses':courses,'highest_attempted_exam':highest_attempted_exam+1})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):

    courses=QMODEL.Course.objects.all()
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(student=student)
    attempted_exams = []

    try:
        for r in results:
            attempted_exams.append(r.exam_id)
        highest_attempted_exam = max(attempted_exams)
    except:
        highest_attempted_exam = 0

    dict={    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.All_Type_Question.objects.all().count(),
    'attempts':highest_attempted_exam,
    'unattempts':15 - highest_attempted_exam,
    'x' : ["Sessions Attempted",'Sessions Unattempted'],
    'y' : [highest_attempted_exam,15 - highest_attempted_exam]

    }


    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):

    student = models.Student.objects.get(user_id=request.user.id)
    pre_post_Result= QMODEL.pre_post_Result.objects.all().filter(student=student)

    print(pre_post_Result)
    print(len(pre_post_Result))

    courses=QMODEL.Course.objects.all()
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(student=student)
    attempted_exams = []
    pretest_marks = -1
    posttest_marks = -1
    msg = "Attend Pre Test First"
    if(len(pre_post_Result) == 0):
        # Give pre test
        print("Give Pre test")
        highest_attempted_exam = -1


    elif(len(pre_post_Result) == 2):
        # Give pre test
        print("Post test result")
        posttest_marks = pre_post_Result[1].marks 
        pretest_marks = pre_post_Result[0].marks 
        try:
            for r in results:
                attempted_exams.append(r.exam_id)
            highest_attempted_exam = max(attempted_exams)
        except:
            highest_attempted_exam = 0

    else:

        # marks = num + depression_freq_mark*1000000 + depression_intensity_mark*10000 + Anxiety_freq_mark*100 + Anxiety_intensity_mark

        marks = pre_post_Result[0].marks 
        print(marks)
        depression_freq_mark        = ((marks%100000000 - marks%1000000)/1000000)/ 36 * 20
        depression_intensity_mark   = ((marks%1000000 - marks%10000)/10000)/ 36 * 20
        Anxiety_freq_mark           = ((marks%10000 - marks%100)/100)/ 32 * 20
        Anxiety_intensity_mark      = (marks%100)/ 32 * 20

        print("--------=============---------")
        print("PreTest Marks : ")
        print("depression_freq_mark : ", depression_freq_mark)
        print("depression_intensity_mark : ", depression_intensity_mark)
        print("Anxiety_freq_mark : ", Anxiety_freq_mark)
        print("Anxiety_intensity_mark : ", Anxiety_intensity_mark)

        if depression_freq_mark <= 5 and depression_intensity_mark <= 5 and Anxiety_freq_mark <= 6 and Anxiety_intensity_mark <= 6:
            print("Result : No Signs")
            print("Message : Mental health is good no need to attend the sessions.")
            msg = "Mental health is good. No need to attend the sessions."
            highest_attempted_exam = -2
            print("No need to give pretest")

        
        elif depression_freq_mark >= 15 and depression_intensity_mark >= 14 and Anxiety_freq_mark >= 16 and Anxiety_intensity_mark >= 15:
            print("Result : Severe")
            print("Message : Please consult to Psychiatrist for further action due to severe symptoms of depression or anxiety.")
            msg = "Please consult to Psychiatrist for further action due to severe symptoms of depression or anxiety. No need to attend the sessions"
            highest_attempted_exam = -2
            print("No need to give pretest")

        else:
            print("Mild/ Moderate")
            print("Message : Please attend the further sessions to reduce the mild or moderate symptoms of depression or anxiety")
            msg = "Please attend the further sessions to reduce the mild symptoms of depression or anxiety"
            try:
                for r in results:
                    attempted_exams.append(r.exam_id)
                highest_attempted_exam = max(attempted_exams)
            except:
                highest_attempted_exam = 0


    return render(request,'student/student_exam.html',{'courses':courses,'highest_attempted_exam':highest_attempted_exam+1,'pretest_marks':pretest_marks,'posttest_marks':posttest_marks,'msg':msg})




@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.All_Type_Question.objects.all().filter(course=course).count()
    student = models.Student.objects.get(user_id=request.user.id)
    questions=QMODEL.All_Type_Question.objects.all().filter(course=course)
    total_marks=0
    highest_attempted_exam = 0
# 

    time_after_which_next_session_can_attempt = 0

    # results= QMODEL.Result.objects.get(exam=course)

    # results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    results= QMODEL.Result.objects.all().filter(student=student)

    # results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    # 

    attempted_exams = []

    for r in results:
        attempted_exams.append(r.exam_id)

    # print(attempted_exams)
    try:
        highest_attempted_exam = max(attempted_exams)
        print("Highest attempted exam : ", highest_attempted_exam)

        if pk <= highest_attempted_exam:
            print("You can attempt exam")
        else:
            if pk - highest_attempted_exam == 1:
                print("Need to check time")
                highest_attempted_exam_1st_attempt_time = results[attempted_exams.index(highest_attempted_exam)].date.replace(tzinfo=None) + timedelta(hours=5.50)
                current_time = datetime.datetime.now()
                hr = abs(current_time - highest_attempted_exam_1st_attempt_time).total_seconds() / 3600.0
                print("Hours : ", hr)
                if hr > time_after_which_next_session_can_attempt:
                    print("You can attempt exam")
                else:
                    print("Need to wait for time")
                    print("Last attempt session Time : ",highest_attempted_exam_1st_attempt_time)

                    print("You can attempt this session after : ", highest_attempted_exam_1st_attempt_time + timedelta(hours=time_after_which_next_session_can_attempt))

                    dd = (highest_attempted_exam_1st_attempt_time + timedelta(hours=time_after_which_next_session_can_attempt)).date()
                    tt = (highest_attempted_exam_1st_attempt_time + timedelta(hours=time_after_which_next_session_can_attempt)).time()
                    print(dd.year)
                    print(dd.strftime("%A"))
                    print(dd.strftime("%d"))

                    to_display = "You can attend this session on or after " + str(tt.strftime("%I")) + ":" + str(tt.strftime("%M")) + " " + str(tt.strftime("%p")) + " on or after " +  str(dd.strftime("%d")) + "/"  + str(dd.strftime("%m")) + "/" +  str(dd.year) + " {" + str(dd.strftime("%A")) + "}"

                    print(to_display)

                    return render(request,'student/student_no_exam.html',{'to_display':to_display})
            
            else:
                    to_display2 = "You have attended " + str(highest_attempted_exam) + " sessions till now." + "Please attend your session number " + str(highest_attempted_exam + 1) + " to enable next session"

                    return render(request,'student/student_no_exam.html',{'to_display2':to_display2})


        return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'highest_attempted_exam':highest_attempted_exam})

    except:
        if pk == 1:
            return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'highest_attempted_exam':0})
        else:
            to_display2 = "Please attend your session number 1 to enable next session"
            return render(request,'student/student_no_exam.html',{'to_display2':to_display2})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.All_Type_Question.objects.all().filter(course=course)  
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        emmo = ['Neutral','Happy','Surprise']

        emotion = emmo[random.randint(0, 2)]

        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        student = models.Student.objects.get(user_id=request.user.id)
        results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
        total_marks=0
        questions=QMODEL.All_Type_Question.objects.all().filter(course=course)
        print("_________________________________________")
        print(course_id)
        print(request.user.id)
        print("============")
        dont_submit = 0
        for i in range(len(questions)):
            selected_ans = request.COOKIES.get(str(i+1))
            print("Answer : ",i)
            print(selected_ans)
            # print(len(selected_ans))
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print()
            if dont_submit == 0:
                que=QMODEL.All_Type_Question.objects.get(id=questions[i].id)
                Q_result = QMODEL.Result_all_question()
                Q_result.student = student
                Q_result.exam = course
                Q_result.question = que
                Q_result.given_ans = selected_ans
                Q_result.attempt = len(results) + 1
                Q_result.face_emotion = emotion
                print("++++++++++++")
                print(questions[i].id)
                print("++++++++++++")


                # Sentiment Analysis
                if questions[i].id == 2 or questions[i].id == 5 or questions[i].id == 6 or questions[i].id == 12 or questions[i].id == 14 or questions[i].id == 16 or questions[i].id == 25 or questions[i].id == 26 or questions[i].id == 29 or questions[i].id == 33 or questions[i].id == 34 or questions[i].id == 41 or questions[i].id >=43:
                    Q_result.comment = check_sentiment.get(selected_ans)
                
                # Check answer
                if questions[i].id == 1:
                        Q_result.comment = "-"

                if questions[i].id == 3:
                        Q_result.comment = check_answer.get("Anger",selected_ans)

                if questions[i].id == 4:
                        Q_result.comment = check_answer.get("Anger, angry, Guilt, Helplessness, Worry",selected_ans)

                if questions[i].id == 7:
                        Q_result.comment = check_answer.get("Disha",selected_ans)

                if questions[i].id == 8:
                        Q_result.comment = check_answer.get("All of the above",selected_ans)

                if questions[i].id == 9:
                        Q_result.comment = check_answer.get("All of the above",selected_ans)

                if questions[i].id == 10:
                        Q_result.comment = check_Match_the_pair.get("a1b3c2",selected_ans)

                if questions[i].id == 11:
                        Q_result.comment = check_Match_the_pair.get("a2b3c1",selected_ans)

                if questions[i].id == 13:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("c") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("C. Major role",selected_ans)

                if questions[i].id == 15:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("c") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("C. I am no good to be selected in such a reputed company. It’s shame for me!",selected_ans)

                if questions[i].id == 17:
                        Q_result.comment = check_answer.get("True",selected_ans)

                if questions[i].id == 18:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("a") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("A. I should be always perfect",selected_ans)

                if questions[i].id == 19:
                        Q_result.comment = check_Match_the_pair.get("1b2c3a",selected_ans)

                if questions[i].id == 20:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("c") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("C. Belief about world",selected_ans)

                if questions[i].id == 21:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("b") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("B. I am very dumb at presentations",selected_ans)

                if questions[i].id == 22:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("a") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("A. I can not live without her.",selected_ans)

                if questions[i].id == 23:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("b") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("B. People are at their bad acts.",selected_ans)

                if questions[i].id == 24:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("c") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("C. One should keep dwelling about possibility of fearsome happening in reality",selected_ans)

                if questions[i].id == 27:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("a") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("A. Result oriented",selected_ans)

                if questions[i].id == 28:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("a") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("A. Blame game",selected_ans)

                if questions[i].id == 30:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("b") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("B.  what will happen in future?",selected_ans)

                if questions[i].id == 31:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("d") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("D. All of the above",selected_ans)

                if questions[i].id == 32:
                    if len(selected_ans) < 3:
                        if selected_ans.lower().find("b") != -1:
                            Q_result.comment = "Correct"
                        else:
                            Q_result.comment = "Incorrect"
                    else:
                        Q_result.comment = check_answer.get("B. It's all over.5",selected_ans)

                if questions[i].id == 35:
                        Q_result.comment = check_answer.get("That only proves this time I did not behave like I expected. That does not prove that  I am a fool or rather what exactly is definition of fool? I will not label myself.",selected_ans)

                if questions[i].id == 36:
                        Q_result.comment = check_answer.get("I do not understand specific part of mathematics that does  not prove that I am dumb at everything. I have other abilities and even for the sake of discussion, I say that I have no abilities, that only proves my limitations on which I can improve upon.",selected_ans)

                if questions[i].id == 37:
                        Q_result.comment = check_answer.get("This only proves that I have behaved not like my own expectations once, there is always a chance to improve",selected_ans)

                if questions[i].id == 38:
                        Q_result.comment = check_answer.get("Again one failure equals to everything is not the fact. Even if there are many failures, that proves I had failed so and so times but I am not a failure in totality.",selected_ans)

                if questions[i].id == 39:
                        Q_result.comment = check_answer.get("I can always improvise on my decision. And if not I can always change my thinking to make myself less disturbed.",selected_ans)

                if questions[i].id == 40:
                        Q_result.comment = check_answer.get("From my past efforts I will learn and change my method. I am useless is only my interpretation",selected_ans)

                if questions[i].id == 42:
                        Q_result.comment = check_answer.get("Demonstrative answer Sataki can politely ask professor, where he can improve therby clarifying his doubts. If he still feels that the  answer from professor does not satisfy him, he can accept it with some displeasure avoiding   blaming anyone. His goal is not to prove anyone wrong or right but to  improve his grades in the long run.",selected_ans)


                Q_result.save()

        if dont_submit == 0:
            student = models.Student.objects.get(user_id=request.user.id)
            result = QMODEL.Result()
            result.marks=total_marks
            result.exam=course
            result.student=student
            result.save()
        if dont_submit == 1:
            print("Dont Submit exam")
        else:
            print("Submit EXAMINATION")
        return HttpResponseRedirect('student-exam')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    print("============")
    print(len(results))
    print("============")

    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(student=student)
    attempted_exams = []

    try:
        for r in results:
            attempted_exams.append(r.exam_id)
        highest_attempted_exam = max(attempted_exams)
    except:
        highest_attempted_exam = 0

    return render(request,'student/student_marks.html',{'courses':courses,'highest_attempted_exam':highest_attempted_exam+1})

  