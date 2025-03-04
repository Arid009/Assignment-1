from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm,LoginForm,CreateGroupForm,AssignRoleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
        
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active=False
            user.save()
            messages.success(request,'A confirmation mail sent. Please check your email')
            return redirect('sign-in')


    return render(request,'register.html',{'form':form})

def sign_in(req):
    form = LoginForm()
    if req.method == 'POST':
        form = LoginForm(data=req.POST)
        if form.is_valid():
            user = form.get_user()
            login(req,user)
            messages.success(req, "Login successfully")
            
            return redirect('dashboard')
        
    return render(req,'login.html',{'form':form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')

def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
@user_passes_test(is_admin,login_url='no-permission')
def create_group(req):
    form = CreateGroupForm()
    if req.method=='POST':
        form = CreateGroupForm(req.POST)
        if form.is_valid():
            group = form.save()
            messages.success(req, f"Group {group.name} has been created successfully")
            return redirect('create-group')
    
    return render(req, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})

@user_passes_test(is_admin,login_url='no-permission')
def delete_group(req,id):
    if req.method == 'POST':
        group = Group.objects.get(id=id)
        group.delete()
        messages.success(req, 'Group Deleted Successfully')
        return redirect('group-list')
    else:
        messages.error(req, 'Something went wrong')
        return redirect('group-list')

@user_passes_test(is_admin,login_url='no-permission')
def delete_user(req,id):
    if req.method == 'POST':
        user = User.objects.get(id=id)
        user.delete()
        messages.success(req, 'User Deleted Successfully')
        return redirect('all-part')
    else:
        messages.error(req, 'Something went wrong')
        return redirect('all-part')
        

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('all-part')
    
    return render(request, 'admin/assign_role.html', {"form": form})