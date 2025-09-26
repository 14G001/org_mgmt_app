from django.views import View
from django.shortcuts import redirect

class HomeView(View):
    def get(self, request):
        return redirect('/ensenaxargentina_example/')