from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Todo
#from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from .models import *

# Create your views here.

def registerPage(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)


            return redirect('login')


    context = {'form':form}
    return render(request, 'todos/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/todos/login/')
    
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/todos/list/')
            else:
                messages.info(request, 'Username OR password is incorrect')
                
        context = {}
        return render(request, 'todos/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')



#     template_name = 'todos/login.html'
#      = '__all__'
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy('todo_list') 

@login_required(login_url='login')

def list_todo_items(request):
    context = {'todo_list' : Todo.objects.all()}
    return render(request, 'todos/todo_list.html',context)

@login_required(login_url='login')
def insert_todo_item(request: HttpRequest):
    todo = Todo(content=request.POST['content'])
    todo.save()
    return redirect('/todos/list/')

@login_required(login_url='login')
def delete_todo_item(request,todo_id):
    todo_to_delete = Todo.objects.get(id=todo_id)
    todo_to_delete.delete()
    return redirect('/todos/list/')