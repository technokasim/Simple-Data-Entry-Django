import io, csv
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout , authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login 
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def home(request):
    context = {}
    data = Work_entry.objects.all()
    context['data'] =  data
    return render(request , 'home.html', context)




def login_request(request):
  if request.user.is_authenticated:
     return redirect("addData")  
  else:
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print('don')
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}")
                return redirect('addData')
            else:
                print('no yar')
                messages.info(request, "No User Found!")
        # else:
            #  messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    form.fields['username'].widget.attrs['class'] = "input"
    
    form.fields['password'].widget.attrs['class'] = "input"
    # form.help_text = None
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("home")




@login_required(login_url='login')
def addData(request):
    context = {}
    template = "add-data.html"
    prompt = {
        'order': 'Order of the CSV should be first_name, last_name, email, ip, message'
    }
    data = Work_entry.objects.all()
    context['data'] =  data

    if request.method == "GET":
        return render(request , template, context)
    

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csvfile')


    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Work_entry.objects.update_or_create(
            position =column[0],
            address =column[1],
            time =column[2]  
        )
    print(context)
    return render(request, template, context)




def is_ajax(self):
    return self.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def ajax_add(request):
    if request.is_ajax():
        name = request.POST.get('txtname') # getting data from first_name input 
        address = request.POST.get('txtdepartment')  # getting data from last_name input
        time = request.POST.get('txtphone')
        q_items = Work_entry.objects.create(position = name, address =address , time = time )
        q_items.save()
        print(q_items)
        response = {
           'msg':'Added successfully!' # response message
        }
        return JsonResponse(response) # return response as JSON
    else:
        print('kkkwork')
        response = {
           'msg':'error' # response message
        }
        return JsonResponse(response) # return response as JSON



def ajax_update(request):
    if request.is_ajax():
        id = request.POST.get('string') # getting data from first_name input 
        name = request.POST.get('txtname') # getting data from first_name input 
        address = request.POST.get('txtdepartment')  # getting data from last_name input
        time = request.POST.get('txtphone') 
        q_items = Work_entry.objects.filter(id = id).update(position = name, address =address , time =time)
        print(q_items)
        response = {
           'msg':'Updated successfully!' # response message
        }
        return JsonResponse(response) # return response as JSON
    else:
        print('kkkwork')
        response = {
           'msg':'error' # response message
        }
        return JsonResponse(response) # return response as JSON




def ajax_delete(request):
    if request.is_ajax():
            id = request.GET.get('string', None)
            Work_entry.objects.filter(id=id).delete()
            response = {
                    'msg':'Deleted successfully!' # response message
                        }
            return JsonResponse(response)


