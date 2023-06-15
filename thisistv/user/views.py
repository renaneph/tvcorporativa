from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    login as login_django,
    authenticate,
    logout as logout_django
)
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from .models import UserProfile, TYPE_USER_CHOICES
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.


@login_required(login_url='/login')
def users_register(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    context = {'type_user': user.type_user, 'form': request.POST}
    if user.type_user != 'A':
        raise PermissionDenied

    if request.method == "GET":
        return render(request, 'register.html', context)

    username = request.POST.get('login')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    type_user = request.POST.get('type-user')

    user = User.objects.filter(username=username).first()

    if user:
        messages.warning(request, 'Erro: Usuário já existe no sistema!')
        return render(request, 'register.html', context)

    if password == password2:
        new_user = User.objects.create_user(username=username, email=email, password=password)

        UserProfile.objects.create(djuser=user, type_user=type_user, djuser_id=new_user.pk)

        return redirect('/user/list-users')

    messages.warning(request, 'Erro: As senhas não são as mesmas!')
    return render(request, 'register.html', context)


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.filter(username=username).first()

    if user:

        if authenticate(username=username, password=password):
            login_django(request, user)

            return redirect('/dashboard/home')

        else:
            messages.warning(request, 'Erro: Usuário ou senha incorreta !')

    else:
        messages.warning(request, 'Erro: Usuário não existe na base de dados !')

    context = {'form': request.POST}
    return render(request, 'login.html', context)


def logout(request):

    logout_django(request)
    return redirect('/login')


@login_required(login_url='/login')
def changepassword(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    context = {'type_user': user.type_user, 'form': request.POST}

    if request.method == "GET":
        return render(request, 'change-password.html', context)

    newpassword = request.POST.get('newpassword')
    newpassword2 = request.POST.get('newpassword2')

    if newpassword != newpassword2:
        messages.warning(request, 'Erro: As senhas não são as mesmas!')
        return render(request, 'change-password.html', context)

    username = request.user
    currentpassword = request.POST.get('currentpassword')
    user_login = User.objects.get(username=username)
    check = check_password(currentpassword, user_login.password)

    if check:
        user_login.set_password(newpassword)
        user_login.save()
        messages.success(request, 'Senha Alterada com sucesso!')
    else:
        messages.warning(request, 'Erro: Senha atual incorreta !')

    return redirect('/user/change-password')


@login_required(login_url='/login')
def table_users(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    if user.type_user != 'A':
        raise PermissionDenied

    if request.method == "GET":
        user_list = User.objects.all()
        user_type = UserProfile.objects.all()
        data = {
            'user_list': user_list,
            'user_type': user_type,
            'type_user': user.type_user
        }
        return render(request, 'users.html', data)


@login_required(login_url='/login')
def deleteuser(request, id):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    if user.type_user != 'A':
        raise PermissionDenied

    if request.method == "POST":
        user = UserProfile.objects.get(djuser_id=id)
        djuser = user.djuser_id
        user.delete()
        User.objects.filter(id=djuser).delete()
        messages.success(request, 'O usuário foi deletado com sucesso!')
        return redirect('/user/list-users')


@login_required(login_url='/login')
def edituser(request, id):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    if user.type_user != 'A':
        raise PermissionDenied

    if request.method == "GET":
        user_active = UserProfile.objects.get(djuser_id=request.user.id)
        djuser = User.objects.get(id=id)
        user = UserProfile.objects.get(djuser_id=djuser.pk)
        list_users = []
        for chave, valor in TYPE_USER_CHOICES:
            if user.type_user != chave:
                list_users.append((chave, valor))
            else:
                name_typeuser = valor

        dict_djuser = {'login': djuser.username, 'email': djuser.email}
        data = {
            'djuser': dict_djuser,
            'type_user': user_active.type_user,
            'type_user_selected': user.type_user,
            'list_users': list_users,
            'name_typeuser': name_typeuser
        }
        return render(request, 'edit_user.html', data)

    user = UserProfile.objects.get(djuser_id=id)
    djuser = User.objects.filter(id=user.djuser_id)

    login = request.POST.get('login')
    email = request.POST.get('email')
    type_user = request.POST.get('type-user')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    active = request.POST.get('customRadio')
    password_hash = make_password(password)

    if password and password2:
        if password != password2:
            messages.warning(request, 'Erro: As senhas não são as mesmas!')
            return render(request, 'edit_user.html', {'user': user, 'djuser': djuser})
        else:
            djuser.update(username=login, email=email, is_active=active, password=password_hash)

    else:
        djuser.update(username=login, email=email, is_active=active)

    user.type_user = type_user
    user.save()
    messages.success(request, 'Usuário editado com sucesso!')
    return redirect('/user/list-users')
