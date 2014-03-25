from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from aicte.forms import UserLoginForm

def user_login(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/portal/extension/')
                else:
                    return HttpResponse('you are blocked')
            else:
                return HttpResponse('Invalid username or password')
        else:
            form = UserLoginForm()
            context = {
                'form': form
            }
            context.update(csrf(request))
            return render_to_response('aicte/templates/user_login.html', context)
    else:
        return HttpResponseRedirect('/portal/extension')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/portal/extension')
