from django.shortcuts import render

def patient_dashboard(request, username):
    full_username = request.GET.get('full_username', username)
    return render(request, 'patient_dashboard.html', {'username': username, 'full_username': full_username})

def doctor_dashboard(request, username):
    full_username = request.GET.get('full_username', username)
    return render(request, 'doctor_dashboard.html', {'username': username, 'full_username': full_username})

def admin_dashboard(request, username):
    return render(request, 'admin_dashboard.html', {'username': username})
