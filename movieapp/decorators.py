from django.core.exceptions import PermissionDenied
import functools



def user_can_edit_movie(view_func):
    @functools.wraps(view_func)
    def ret_func(*args,**kwargs):
        # request = kwargs['request']
        # print("------ request user",request.user.name)
        return view_func
    return ret_func
