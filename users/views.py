from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

User = get_user_model()

@login_required
def create_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Create a new user and assign `created_by`
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.created_by = request.user
        new_user.save()

        return redirect("user_list")  # Change to your actual redirect URL

    return render(request, "users/create_user.html")


@login_required
def user_list(request):
    if request.user.groups.filter(name="Operator").exists():
        users = User.objects.filter(created_by=request.user)  # Show only their created users
    else:
        users = User.objects.all()  # Admins see all users
    return render(request, "users/user_list.html", {"users": users})