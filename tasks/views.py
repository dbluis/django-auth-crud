from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm, "error": "El usuario ya existe"
                })
        return render(request, "signup.html", {
            "form": UserCreationForm, "error": "Las contraseñas no coinciden"
        })


def signout(request):
    logout(request)
    return redirect("index")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm, "error": "El usuario o contraseña no coinciden"
            })
        else:
            login(request, user)
            return redirect("tasks")


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks.html", {
        "tasks": tasks
    })


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {
            "form": TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "create_task.html", {
                "form": TaskForm, "error": "Complete con datos validos"
            })


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {
            "task": task, "form": form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "task_detail.html", {
                "task": task, "form": form, "error": "error actualizando tarea"
            })


@login_required
def task_completed(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def finish_tasks(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by("-datecompleted")
    return render(request, "tasks.html", {"tasks": tasks})
