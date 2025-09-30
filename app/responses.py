from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden

def json_result(status=200, **kwargs):
    return JsonResponse(kwargs, status=status)
def resource_not_exists():
    return HttpResponseNotFound("El recurso no existe.")
def access_denied():
    return HttpResponseForbidden("Acceso denegado")
def not_authorized():
    return error(403, "Not authorized")
def error(status, result_message, **kwargs):
    kwargs['result'] = result_message
    return json_result(status, **kwargs)
def ok(**kwargs):
    return json_result(**kwargs)