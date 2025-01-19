from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def departments(request):
    return render(request,'departments.html')

def doctors(request):
    return render(request,'doctors.html')

def contact_us(request):
    return render(request,'contact_us.html')

def sign_in(request):
    return render(request,'sign_in.html')