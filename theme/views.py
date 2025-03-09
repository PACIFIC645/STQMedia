from django.shortcuts import render

def theme_home(request):
    return render(request, 'theme/index.html')
