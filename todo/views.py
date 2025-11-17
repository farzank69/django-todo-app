from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import date
from .models import Task
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import TaskForm
from django.contrib.auth.views import LoginView
# views.py
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_email(request):
    if request.method == "POST":
        subject = request.POST.get("subject", "No Subject")
        message = request.POST.get("message", "")
        recipient = request.POST.get("recipient")

        if not recipient:
            return JsonResponse({"error": "Recipient email is required"}, status=400)

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email="your_email@gmail.com",   # Must match EMAIL_HOST_USER in settings.py
                recipient_list=[recipient],
                fail_silently=False,
            )
            return JsonResponse({"success": "Email sent successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # 👇 If GET request, just render the form
    return render(request, "todo/send_email.html")

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('completed', 'due_date')

        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False) #won't save yet.
                task.user = request.user
                task.save()
                messages.success(request, "Task added successfully!")
                return redirect('home')
        else:
            form = TaskForm()
        return render(request, 'home.html', {'tasks':tasks, 'form': form, 'today': date.today()})
    
    else:
        return redirect('login')

def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id = task.id)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'update_task.html', {'form': form, 'task': task})

@login_required
def mark_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.completed = True
        task.save()
    return redirect('home')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
    return redirect('home')

