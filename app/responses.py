from django.http import JsonResponse, Http404

def json_result(status=200, **kwargs):
    return JsonResponse(kwargs, status=status)
def resource_not_exists():
    return Http404("Resource not found.")
def error(status, result_message, **kwargs):
    kwargs['result'] = result_message
    return json_result(status, **kwargs)
def ok(**kwargs):
    return json_result(**kwargs)