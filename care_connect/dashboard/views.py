from django.shortcuts import render

def patient_dashboard(request, username):
    return render(request, 'patient_dashboard.html', {'username': username})

def doctor_dashboard(request, username):
    return render(request, 'doctor_dashboard.html', {'username': username})

def admin_dashboard(request, username):
    return render(request, 'admin_dashboard.html', {'username': username})
