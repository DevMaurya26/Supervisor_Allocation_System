from django.shortcuts import render , redirect
from django.http import FileResponse,HttpResponse, HttpResponseRedirect
from Logics.fileReader import saveAtServer
from Logics.allocation import allocations
from django.contrib.auth.decorators import login_required
from .middelware import is_admin
from .models import Allocation_File, Change_reqs
from django.contrib.auth.models import User

save = saveAtServer()
final_file_name = ''
# Create your views here.
def index(request):
    return render(request, 'main/index.html')

@is_admin
def create(request):
    flag1 = False
    flag2 = False
    exam_name = request.POST.get('exam_name')
    user_instance = User.objects.get(pk=request.user.id)
    user_files = Allocation_File.objects.filter(user_id=user_instance)

    data ={
        'Done' : 'Done Uploading ✅',
        'error' : 'Please Upload the CSV files first 📂',
        'err_flag' : True,
        'user_files' : user_files,
        'user_instance' : user_instance,
    }
    if request.method == 'POST':
        # print(request.FILES)
        if 'prepared_file' in request.FILES:
            uploaded_file = request.FILES['prepared_file']
            flag3 = save.read_prepared_csv(uploaded_file)
            if flag3:
                final_file_name = uploaded_file.name
                with open('./CSVfiles/generated_files/0files.txt', 'a') as f:
                    f.write(final_file_name+'\n')
                data['err_flag'] = False
                obj = Allocation_File(user_id=user_instance,file_name=final_file_name,exam_name=exam_name)
                obj.save()
            return render(request, 'main/create.html',data)

        if 'date_csv' in request.FILES:
            uploaded_file = request.FILES['date_csv']
            flag1 = save.read_date_csv(uploaded_file)

        if 'name_csv' in request.FILES:
            uploaded_file = request.FILES['name_csv']
            flag2 = save.read_name_csv(uploaded_file)

        print(flag1,"------",flag2)
        if flag1 and flag2:
            final_file_name = allocations.do_allocations(request.user.id,exam_name)
            with open('./CSVfiles/generated_files/0files.txt', 'a') as f:
                f.write(final_file_name+'\n')

            data['err_flag'] = False
    
    db = Allocation_File.objects.filter(user_id=request.user.id)
    print(db)

    return render(request, 'main/create.html',data)



@login_required(login_url='login')
def generated(request):
    data =[]
    latest_file_name=''
    not_registered_clg=False
    if request.user.is_staff:
        return redirect('create')

    user_instance = User.objects.get(pk=request.user.id)
    UserName = request.user.email or user_instance.username
    institute_name = user_instance.last_name

    try:

        admin_id_institute = User.objects.get(last_name=institute_name,is_staff=1)
        print(admin_id_institute)

        latest_file_name = Allocation_File.objects.filter(user_id=admin_id_institute.id)
        print(latest_file_name)

        try:
            data = allocations.find_allocation_for(UserName,latest_file_name.last())
            global final_file_name
            final_file_name = latest_file_name.last()
        except Exception as e:
            print('Unable to find Data..', e)
        
    except Exception as e:
        not_registered_clg = True
        print('College is not registered..!',e)

    finally:
        return render(request, 'main/table_data.html',{'data':data,'file_name':latest_file_name,'college_404':not_registered_clg})



@login_required(login_url='login')
def download(request, file_name):
    response = FileResponse(open(f'./CSVfiles/generated_files/{file_name}', 'rb'))

    response['Content-Disposition'] = f'attachment; filename="Block_Allocation: {file_name[:10]}.csv"'

    return response

@login_required(login_url='login')
def change_req(request,data):
    data = data.split(' ')
    
    user_instance = User.objects.get(pk=request.user.id) 
    #user instance need inorder to use as foregion key
    date = data[0][1:]
    time = data[1]+data[2]
    Name = data[3]
    Block_Number = data[-1].split(']')[0]
    final_file_name
    
    details = str(date)+' '+str(time)+' - block no.: '+str(Block_Number)
    Obj_Change_req_db = Change_reqs(requestor_id=user_instance,reqtor_name=request.user.first_name,file_name=str(final_file_name),previous_details=details,college=request.user.last_name)

    Obj_Change_req_db.save()
    # return render(request,'main/change_form.html',{'data':data})
    return HttpResponse(status=204)

@login_required(login_url='login')
def user_change_req(request):
    user_instance = User.objects.get(pk=request.user.id) 
    if not request.user.is_staff:
        data = Change_reqs.objects.filter(requestor_id=request.user.id)
        return render(request, 'main/change_form.html',{'data':data})

    #if admin login then show all of the data where institute name is same..!
    print(user_instance.last_name)
    data = Change_reqs.objects.filter(college=user_instance.last_name)
    print(data)
    return render(request, 'main/change_form.html',{'data':data})
    
@is_admin    
def admin_aprove_reject(request,decision,req_id):
    print(decision,req_id)
    Change_reqs.objects.filter(id=req_id).update(status=decision)
    return redirect('your_change_req') #to render same page 

@is_admin
def staff(request,institute):
    staff_list = User.objects.filter(last_name=institute,is_staff=0)
    # print([name.first_name for name in staff_list])
    return render(request,'main/staff.html',{'staff_list' : staff_list})

@is_admin
def remove_staff(request,user_id):
    try:

        obj = User.objects.get(id = user_id)
        obj.delete()
        user_instance = User.objects.get(pk=request.user.id) 
        return redirect('staff_list',user_instance.last_name)
    
    except User.DoesNotExist:
        print("User is not Exists..!🤔")
    
    except Exception as e:
        print("Error in staff removing >> ",e)

    # return HttpResponse(210)
 # 210 successfuly removed
