from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg
from django.views.decorators.csrf import csrf_exempt

from .models import *


def register(request):

    username = request.POST.get("username", "")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"response": "Error: Username already exists."}, status=400)
    else:

        password = request.POST.get("password", "")
        email = request.POST.get("email", "")

        new_user = User(username=username, email=email, password=password)
        new_user.save()

        return JsonResponse({"response": "Successfully registered"}, status=200)

@csrf_exempt
def login(request):

    logged_in_user = request.session.get("username")

    if not logged_in_user:

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if User.objects.filter(username=username, password=password).exists():
            request.session["username"] = username
        else:
            return JsonResponse({"response": "Error: Incorrect username or password"}, status=400)

        return JsonResponse({"response": "Successfully logged in"}, status=200)
    else:
        return JsonResponse({"response": "Error: User already logged in"}, status=400)
    
@csrf_exempt
def logout(request):

    logged_in_user = request.session.get("username")

    if not logged_in_user:
        username = request.POST.get("username", "")
        request.session["username"] = username

        return JsonResponse({"response": "Error: Please login first"}, status=400)
    else:
        request.session.flush()

        return JsonResponse({"response": "Successfully Logged out"}, status=200)
    

def list(request):

    logged_in_user = request.session.get("username")

    if not logged_in_user:
        return JsonResponse({"response": "Error: Please login"}, status=400)
    else:

        ratings_list = []

        # gets all ModuleInstances, 
        module_instances = ModuleInstance.objects.all()

        for mi in module_instances:
            professors = Professor.objects.filter(taughtmodule__moduleInstance=mi)

            ratings_list.append({
                "module_ID": mi.module.ID,
                "module_name": mi.module.name,
                "year": mi.year,
                "semester": mi.semester,
                "professor_ids": [prof.ID for prof in professors],  # Unique Professor IDs
                "professor_names": [prof.name for prof in professors]  # Unique Professor Names
            })

        return JsonResponse({"response": ratings_list}, status=200)

def view(request):

    logged_in_user = request.session.get("username")

    if not logged_in_user:
        return JsonResponse({"response": "Error: Please login"}, status=400)
    else:
        professors = Professor.objects.annotate(avg_rating=Avg("taughtmodule__rating__rating"))

        professor_list = []
        for prof in professors:
            professor_list.append({
                "professor_ID": prof.ID,
                "professor_name": prof.name,
                "avg_rating": round(prof.avg_rating) if prof.avg_rating is not None else "No Ratings"
            })

        return JsonResponse({"response": professor_list}, status=200)

    
def average(request):

    logged_in_user = request.session.get("username")

    if not logged_in_user:
        return JsonResponse({"response": "Error: Please login"}, status=400)
    else:

        professor_id = request.GET.get("professor_id", "")
        module_id = request.GET.get("module_id", "")

        try:
            professor = Professor.objects.get(ID=professor_id)
            module = Module.objects.get(ID=module_id)
        except Professor.DoesNotExist:
            return JsonResponse({"response": f"Error: Professor with ID '{professor_id}' not found."}, status=404)
        except Module.DoesNotExist:
            return JsonResponse({"response": f"Error: Module with code '{module_id}' not found."}, status=404)
        

        avg_rating = Rating.objects.filter(
            taughtModule__professor__ID=professor_id,
            taughtModule__moduleInstance__module__ID=module_id
        ).aggregate(average=Avg("rating"))["average"]

        return JsonResponse({
            "professor_ID": professor.ID,
            "professor_name": professor.name,
            "module_ID": module.ID,
            "module_name": module.name,
            "avg_rating": round(avg_rating) if avg_rating is not None else None
            }, status=200)

@csrf_exempt
def rate(request):

    logged_in_user = request.session.get("username")

    print(logged_in_user)

    if not logged_in_user:
        return JsonResponse({"response": "Error: Please login"}, status=400)
    else:
        
        try:
            professor_id = request.POST.get("professor_id", "")
            module_id = request.POST.get("module_id", "")
            year = int(request.POST.get("year", ""))
            semester = int(request.POST.get("semester", ""))
            rating = int(request.POST.get("rating", ""))

            if rating < 1 or rating > 5:
                return JsonResponse({"response": "Error: Invalid rating. Please provide an integer between 1 and 5."}, status=400)


            logged_user = User.objects.get(username=logged_in_user)

            taught_module = TaughtModule.objects.get(
                professor__ID=professor_id,
                moduleInstance__module__ID=module_id,
                moduleInstance__year=year,
                moduleInstance__semester=semester
            )

            _, created = Rating.objects.update_or_create(
                taughtModule=taught_module,  
                user=logged_user,  
                defaults={"rating": rating}  
            )

            if created:
                return JsonResponse({"response": "Rating added successfully"}, status=200)
            else:
                return JsonResponse({"response": "Rating updated successfully"}, status=200)
                
        except (TaughtModule.DoesNotExist, ValueError):
            return JsonResponse({"response": "Error: Invalid arguments or does not exist."}, status=404)

        except User.DoesNotExist: # user deleted during session
            request.session.flush()
            return JsonResponse({"response": "Error: User not found"}, status=404)


