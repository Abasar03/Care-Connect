import psycopg2
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def departments(request):
    return render(request,'departments.html')

def doctors(request):
    return render(request,'doctors.html')

def contact_us(request):
    return render(request,'contact_us.html')

def login(request):
    return render(request,'login.html')

def doctor_login(request):
    return render(request,'doctor_login.html')

def register(request):
    return render(request,'register.html')


# Utility function to get database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['care connect'],
        user=settings.DATABASES['default']['postgres'],
        password=settings.DATABASES['default']['LewondoskI@09'],
        host=settings.DATABASES['default']['localhost'],
        port=settings.DATABASES['default']['5432']
    )

# Registration View
def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        if role == 'doctor':
            specialization = request.POST.get('specialization')
            schedule = request.POST.get('schedule')
            contact_num = request.POST.get('contact_num')
            dep_id = request.POST.get('dep_id')
            cursor.execute(
                "INSERT INTO doctor (name, specialization, contact_num, schedule, email, password, dep_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (name, specialization, contact_num, schedule, email, password, dep_id)
            )
        elif role == 'patient':
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            contact_num = request.POST.get('contact_num')
            address = request.POST.get('address')
            dep_id = request.POST.get('dep_id')
            cursor.execute(
                "INSERT INTO patient (name, age, gender, contact_num, address, email, password, dep_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, age, gender, contact_num, address, email, password, dep_id)
            )

        conn.commit()
        cursor.close()
        conn.close()
        messages.success(request, "Registration successful.")
        return redirect('login')

    return render(request, 'register.html')

# Login View for Admin, Doctor, and Patient
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check for Admin Login
        if email == 'admin@example.com' and password == 'adminpass':
            return redirect('admin_dashboard')

        # Check for Doctor Login
        cursor.execute("SELECT * FROM doctor WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            return redirect('doctor_dashboard')

        # Check for Patient Login
        cursor.execute("SELECT * FROM patient WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            return redirect('patient_dashboard')

        cursor.close()
        conn.close()
        messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')
