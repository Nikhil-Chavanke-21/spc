# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm
#
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
#
#from files.models import File
# from django.http import HttpResponse
# from django.utils.encoding import iri_to_uri
#
@csrf_exempt
def register(request):
	if request.method =='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			#username = form.cleaned_data.get('username')
			messages.success(request, "Your account has been created! You can now login")
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

# class HttpResponseTemporaryRedirect(HttpResponse):
#     status_code = 307

#     def __init__(self, redirect_to):
#         HttpResponse.__init__(self)
#         self['Location'] = iri_to_uri(redirect_to)

class DLoginView(LoginView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

@login_required
def my_cloud(request):
	context={
		'files': request.user.file_set.all()
	}
	return render(request, 'users/my_cloud.html',context)

@login_required
def scheme(request):
	return render(request, 'users/scheme.html')