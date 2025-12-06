from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from .models import Users
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def greet(request):
    return HttpResponse("Hello!! welcome to django")
def info(request):
    data={
        'name':["sharanya","harish","chandu"],
        'age':[23,21,24],
        'city':['hyderabad','warangal','warangal']
    }
    return JsonResponse(data)

def calculator(request):
    a=int(request.GET.get('a',10))
    b=int(request.GET.get('b',2))
    results={
        "addition":a+b,
        "subtraction":a-b,
        "multiplication":a*b,
        "division":a/b
    }
    return JsonResponse(results)

def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})


@csrf_exempt
def addStudent(request):
    # for data inserting
    if request.method=='POST':
        data=json.loads(request.body)
        student=Student.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
        )
        return JsonResponse({"status":"success","id":student.id},status=200)
    # for data getting(retrive)
    elif request.method=='GET':
        # result=list(Student.objects.values())
        # return JsonResponse({"status":"ok","data":result},status=200)

        # get all records
        # result=list(Student.objects.all().values())
        # return JsonResponse({"status":"ok","data":result},status=200)

        # get the exactly one record
        # results=Student.objects.filter(id=6).values().first()
        # return JsonResponse({"status":"ok","data":results},status=200) 

        # get age>=20
        data=json.loads(request.body)
        ref_age=data.get("age")
        results=list(Student.objects.filter(age__gte=ref_age).values())
        return JsonResponse({"status":"ok","data":results},status=200) 


    

    
    # for data update
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id") #getting id
        new_email=data.get("email")  #getting email
        existing_student=Student.objects.get(id=ref_id) #fetched the objects as per the id
        existing_student.email=new_email
        existing_student.save()
        updated_data=list(Student.objects.filter(id=ref_id).values())
        return JsonResponse({"status":"data updated successfully","updated_data":updated_data},status=200)
    
    # for delete data
    elif request.method=='DELETE':
        data=json.loads(request.body)
        ref_id=data.get("id")
        get_deleting_data=list(Student.objects.filter(id=ref_id).values())
        to_be_delete=Student.objects.get(id=ref_id)
        to_be_delete.delete()
        return JsonResponse({"req":"success","message":"Student record delete successfully","deleted data":get_deleting_data},status=200)



    return JsonResponse({"error":"use post method"},status=400)




# users
@csrf_exempt
def signUp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Create user
            user = Users.objects.create(
                username=data.get("username"),
                email=data.get("email"),
                password=make_password(data.get("password"))
            )

            # Serialize model into JSON-friendly dictionary
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }

            return JsonResponse({
                "status": "success",
                "message": "User created successfully",
                "data": user_data
            }, status=200)

        except Exception as e:
            # Return REAL error message to Postman
            return JsonResponse({"status": "failed", "error": str(e)}, status=500)

    return JsonResponse({"error": "Use POST method only"}, status=400)


# change the password

@csrf_exempt
def change_password(request):
    if request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        new_password=data.get("password")
        exisiting_user=Users.objects.get(id=ref_id)
        exisiting_user.password=make_password(new_password)
        exisiting_user.save()
        return JsonResponse({"status":"success","message":"change the password successfully","username":exisiting_user.username},status=200)
    

