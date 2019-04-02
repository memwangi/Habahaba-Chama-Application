from django.shortcuts import render

def index(request):
    return render(request, 'chama/create_chama.html')
