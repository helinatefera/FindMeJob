from django.http import HttpResponse
from django.shortcuts import redirect


   
def allowed_user(allowed_roles=[]):
    def decoretor(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.group.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not allowed')
                
            
        return wrapper_func
    return decoretor
def admin_only(view_func):
    def wrapper_function(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='employee':
            return redirect('allJob')
        if group =='aompany':
            return view_func(request,*args,**kwargs)
            
    return wrapper_function
