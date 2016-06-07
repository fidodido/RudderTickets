from django.shortcuts import render
from appauth.forms import AuthForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

#this errors must be in global config
ERR_NOT_VALID = 'Sorry, Not valid account'
ERR_INACTIVE = 'Sorry, this account is inactive'
NO_PROJECTS = 'Sorry, this account dont have projects active'

SUCCESS_REDIRECT = 'tickets_index'

LOGOUT_REDIRECT = 'signin'


def signin(request):

    success_redirect = 'index'
    template = 'appauth/signin.html'

    if request.method == 'POST':

        form = AuthForm(request.POST)
        errors = []
        context = {
            'form': form,
            'errors': errors
        }

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            # si el usuario existe.
            if user is not None:

                # si el usuario esta activo.
                if user.is_active:

                    login(request, user)
                    return redirect(SUCCESS_REDIRECT)
                    
                else:
                    errors.append(ERR_INACTIVE)
                    return render(request, template, context)
            else:
                errors.append(ERR_NOT_VALID)
                return render(request, template, context)
        else:
            return render(request, template, context)

    form = AuthForm()
    return render(request, template)


def signout(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT)


#@login_required
def user_profile(request, user_id):

    template = 'appauth/user_profile.html'

    user = User.objects.get(pk=user_id)

    return render(request, template, {'user': user})