from django.shortcuts import render, redirect,get_object_or_404
from .models import User ,requestData
from django import template
from django.db.models import Q

from django.contrib.auth import authenticate, login
#from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
'''
def run(request):
    return render(request, "admin_page.html")
'''
def run(request):
    return render(request, "login.html")

def delete_Queue(request):
    if request.method== "POST":
        Quid = request.POST.get('Quid')
        st = requestData.objects.filter(uid=Quid)
        if st :
            st.delete()
            success_message = f"Queue has been cleared successfully! you can apply now with uid {Quid}"
            return render(request, 'admin_page.html', {'success_message':success_message})
        try:   
            error_message =f"there is no apllication with this uid {Quid}"
            return render(request, 'admin_page.html', {'error_message':  error_message})
        except IntegrityError:
            error_message = "An error occurred while deleting the user. Please try again."
       
        return redirect('admin_page')
    else:
        return redirect('admin_page')       

def deleteUser(request):
    if request.method == "POST":
        uid = request.POST.get('tuid')
        users = User.objects.filter(uid=uid)
        var=uid
        if users.exists():
            users.update(status="inactive")
            #users.delete()
            success_message = f"User deleted successfully! {var}"
            return render(request, 'admin_page.html', {'success_message':success_message})
        try:   
            error_message ="UID does not exists. Please use a different UID."
            return render(request, 'admin_page.html', {'error_message':  error_message})
        except IntegrityError:
            error_message = "An error occurred while deleting the user. Please try again."       
        return redirect('admin_page')
    else:
        return redirect('admin_page')

def editUser(request):
    if request.method == 'POST':
        euid = request.POST.get('euid')
        epass=request.POST.get('npass')
        users = User.objects.filter(uid=euid)
        if users.exists():
            users.update(upassword=epass)
            success_message = f"password changed successfully for the Id ! {euid}  new password is  {epass}"
            return render(request, 'admin_page.html', {'success_message':success_message})
        try:   
            error_message ="UID does not exists. Please use a different UID."
            return render(request, 'admin_page.html', {'error_message':  error_message})
        except IntegrityError:
            error_message = "An error occurred while updating password of the user. Please try again."      
        return redirect('admin_page')
    else:
        return redirect('admin_page')        

def addUser(request):
    if request.method == 'POST':
        
        vuid = request.POST['tuid']
        vuname = request.POST['tuname']
        vuemail = request.POST['tumail']
        vpassword= request.POST['tpassword']
        vrole=request.POST['trole']
        vdept=request.POST['tdept']
        vstatus=request.POST['tstatus']
        '''us = User(uid=vuid, uname=vuname, uemail=vuemail, role=vpassword)
        us.save()'''        
        if User.objects.filter(uid=vuid).exists():
            error_message = "UID already exists. Please use a different UID."
            return render(request, 'admin_page.html', {'error_message': error_message})        
        try:
            if (vuid and vuname and vuemail and vpassword and vrole):
                if vrole=="student":
                    vdept="cse"
                print(vuid,vuname, vuemail,vpassword,vrole ,vdept)
                user = User(uid=vuid, uname=vuname, uemail=vuemail, upassword=vpassword, status=vstatus,department=vdept,role=vrole )
                user.save()
                success_message = "User added successfully!"
                return render(request, 'admin_page.html', {'success_message': success_message})
            else:
                error_message = "An error occurred while adding the user. Please try again."
                return render(request, 'admin_page.html', {'error_message': error_message})
        except IntegrityError:
            error_message = "An error occurred while adding the user. Please try again."
       
        return redirect('admin_page')
    else:
        return redirect('admin_page')

def admin_page(request):
    return render(request, 'admin_page.html')
def check(request):
    return render(request, 'check.html')
def add(request):
    return render(request, 'add.html')
def view(request):
    return render(request, 'view.html')
def delete(request):
    return render(request, 'delete.html')
def delete_Q(request):
    return render(request, 'delete_Q.html')
def edit(request):
    return render(request,'edit.html')
def login(request):
    return render(request,'login.html')
def viewUser(request):
    if request.method=='POST':
        adminPass = request.POST['adminPass']
        
        pas='kamal'
        if pas==adminPass:
            users = User.objects.all()
            return render(request, 'admin_page.html', {'viewOk': True, 'users': users})
        else:
            error_message = "Oops!! some thing went wrong !!wrong password"
            return render(request, 'admin_page.html', {'error_message': error_message})
     
def loginUser(request):
    if request.method == 'POST':
        vuid = request.POST.get('luid')
        vpassword = request.POST.get('lpasswd')        
        try:
            user = User.objects.get(uid=vuid)           
            if vpassword == user.upassword:
                if user.status == "inactive":
                    context = f"ID with {vuid} does not have access."
                    return render(request, "login.html", {'error': context})               
                # determine user department and thenn prepare context accordingly
                if user.department=="cse":
                    l1={"Username":user,"Status":user.status,"UserId":user.uid}
                    context = {'message1': l1.items(),'message2': vuid}
                    return render(request, "student.html",context) 
                u_dept = user.department
                all_users = requestData.objects.all()
                data = []
                
                if u_dept == "examination":
                    text = "Welcome to Examination Department, "
                    c_name="examD"
                    for i in all_users:
                        curr = {'uid': i.uid, 'status': i.examD}
                        data.append(curr)
                
                elif u_dept == "library":
                    text = "Welcome to Library Department, "
                    c_name="libD"
                    for i in all_users:
                        curr = {'uid': i.uid, 'status': i.libD}
                        data.append(curr)
                
                elif u_dept == "hostel":
                    text = "Welcome to Hostel Department, "
                    c_name="hostelD"
                    for i in all_users:
                        curr = {'uid': i.uid, 'status': i.hostelD}
                        data.append(curr)
                
                elif u_dept == "lab":
                    text = "Welcome to Lab Department, "
                    c_name="labD"
                    for i in all_users:
                        curr = {'uid': i.uid, 'status': i.labD}
                        data.append(curr)
                
                elif u_dept == "security":
                    text = "Welcome to Security Department, "
                    c_name="secD"
                    for i in all_users:
                        curr = {'uid': i.uid, 'status': i.secD}
                        data.append(curr)
                
                elif u_dept == "hod":
                    text = "Welcome to HOD Department, "
                    c_name="hoD"
                    for i in all_users:
                        curr = {'uid': i.uid, 'status': i.hoD}
                        data.append(curr)
                context = {
                    'text': text,
                    't1': user.uname,
                    'viewOk': True,
                    'dept': data,
                    'messages':u_dept,
                    'c_name': c_name
                }  
                return render(request, "display_dept.html", context)             
            else:
                return render(request, "login.html", {'error': 'Invalid Password'})
        except User.DoesNotExist:
            return render(request, "login.html", {'error': 'Invalid UID'})
    return render(request, "login.html")

def studentData(request):
    if request.method == 'POST':
        input_data = request.POST.get('check')
        vuid = request.POST.get('message2')
        if input_data=="apply":
            row_exists = requestData.objects.filter(uid=vuid).exists()
            if row_exists:
                message3 = f"you are trying to applying for NOC, But you have already applied for NOC with the id :  {vuid}"   
            else:
                #secD hoD hostelD libD examD labD
                user =requestData(uid=vuid,secD="pending",hoD="pending", hostelD="pending", libD="pending",labD="pending", examD="pending")
                user.save()
                message3 = f"successfully NOC is applied for UID {vuid} ."
            context = {'message3': message3,}
            return render(request, 'display_std.html', context)
        if input_data=="track":
            row_exists = requestData.objects.filter(uid=vuid).exists()
            if row_exists:
                message3 = f"UID  {vuid}. this is your status Dear,"
                data=requestData.objects.get(uid=vuid)
                message2={
                    "Head of the Department": data.hoD,
                    "Examination Department":data.examD,
                    "Hostel Department     ":data.hostelD,
                    "Laboratory Department ":data.labD,
                    "Library Department    ":data.libD,
                    "Security Department   ":data.secD
                }
                message2=message2.items()
                context = {'message3': message3,'message2':message2}
                print(data.labD)
                if all(status == "accepted" for status in [data.hoD, data.examD, data.hostelD, data.labD, data.secD, data.libD]):  
                    print("done")
                    pmessage="done bayya"
                    context = {'message3': message3,'message2':message2,'pmessage':pmessage}
                else:
                    context = {'message3': message3,'message2':message2}
            else:               
                message3 = f"with the UID: {vuid}, There is no application."
                context = {'message3': message3}
            return render(request, 'display_std.html', context)
def deptupdate(request):
    text = None
    viewOk = True
    dept = requestData.objects.all()
    if request.method == 'POST':
        search_query = request.POST.get('search')
        status_filter = request.POST.get('status_filter')
        dept1=request.POST.get('messages')
            #print(dept1,search_query,status_filter)
            #secD hoD hostelD libD examD labD
        if dept1=="library":
            dept1="libD"
        if dept1=="hostel":
            dept1="hostelD"
        if dept1=="examination":
            dept1="examD"
        if dept1=="security":
            dept1="secD"
        if dept1=="lab":
            dept1="labD"
        if dept1=="hod":
            dept1="hoD" 
        if search_query:
            dept = requestData.objects.filter(uid=search_query).values(dept1).first()
            if dept:
                message ={
                        'dept': dept[dept1],
                        'uid':search_query,
                        'viewok':"hi",
                        }
            else:
                message1="There is no student with this id"
                message={
                    'viewok':"error",
                    'message1':message1,
                }
            return render(request, 'display_dept2.html', message)
        if status_filter:
            if dept1=='libD':
                dept = requestData.objects.filter(libD=status_filter).values('uid',dept1)
            if dept1=='labD':
                dept = requestData.objects.filter(labD=status_filter).values('uid',dept1)
            if dept1=='examD':
                dept = requestData.objects.filter(examD=status_filter).values('uid',dept1)
            if dept1=='secureD':
                dept = requestData.objects.filter(secureD=status_filter).values('uid',dept1)
            if dept1=='hoD':
                dept = requestData.objects.filter(hoD=status_filter).values('uid',dept1)
            if dept1=='hostelD':
                dept = requestData.objects.filter(hostelD=status_filter).values('uid',dept1)
            if dept:
                message={
                    'filter':"hi",
                    'dept':dept,
                }
            else:
                message1="There are no students with this filter "
                message={
                    'viewok':"error",
                    'message1':message1,
                }   
            return render(request, 'display_dept2.html', message)
        
        duid = request.POST.get('duid')
        if 'accept' in request.POST:
            c_name = dept1 #request.POST.get('c_name')
            print(c_name)
            if c_name=="examD":
                requestData.objects.filter(uid=duid).update(examD='accepted')
            elif c_name=="labD":
                requestData.objects.filter(uid=duid).update(labD='accepted')
            elif c_name=="libD":
                requestData.objects.filter(uid=duid).update(libD='accepted')
            elif c_name=="hostelD":
                requestData.objects.filter(uid=duid).update(hostelD='accepted')
            elif c_name=="hoD":
                requestData.objects.filter(uid=duid).update(hoD='accepted')
            elif c_name=="secD":
                requestData.objects.filter(uid=duid).update(secD='accepted')
            else:
                print("going out")
        
            text = f"Accepted UID: {duid}"
        elif 'reject' in request.POST:
            c_name = dept1 #request.POST.get('c_name')

            if c_name=="examD":
                requestData.objects.filter(uid=duid).update(examD='rejected')
            if c_name=="labD":
                requestData.objects.filter(uid=duid).update(labD='rejected')
            if c_name=="libD":
                requestData.objects.filter(uid=duid).update(libD='rejected')
            if c_name=="hostelD":
                requestData.objects.filter(uid=duid).update(hostelD='rejected')
            if c_name=="hoD":
                requestData.objects.filter(uid=duid).update(hoD='rejected')
            if c_name=="secD":
                requestData.objects.filter(uid=duid).update(secD='rejected')
            text = f"Rejected UID: {duid}"

        data=[]
        for i in dept:
            curr = {'uid': i.uid, 'status': i.hoD}
            data.append(curr)        
    context = {
        'text': text,
        #'t1': message1,
        #'message2': message2,
        'dept1':dept1,
        'viewOk': viewOk,
        'dept': data,
    }
    return render(request, 'display_dept.html', context)