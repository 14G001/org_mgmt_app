from django.views import View
from django.shortcuts import redirect

class IndexView(View):
    def get(self, request):
        return redirect('/campus_example/')