import psycopg2
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password


def home(request):
    return render(request, 'home.html')

def departments(request):
    return render(request,'departments.html')

def doctors(request):
    return render(request,'doctors.html')

def contact_us(request):
    return render(request,'contact_us.html')

def index(request):
    return render(request, 'index.html')

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )


def doctor_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        specialization = request.POST['specialization']
        schedule = request.POST['schedule']
        contact_num = request.POST['contact_num']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("select dep_id from department where name=%s",(specialization,))
        result = cursor.fetchone()
        
        if not result:
            messages.error(request,"Department not found")
            return redirect('doctor_register')
        
        dep_id = result[0]
        
        cursor.execute(
            "INSERT INTO doctor (name, email, password, specialization, contact_num, schedule,dep_id) VALUES (%s, %s, %s, %s, %s, %s,%s)",
            (name, email, password, specialization, contact_num, schedule,dep_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        messages.success(request, "Doctor registered successfully.")
        return redirect('doctor_login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dep_id, name FROM department")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request, 'doctor_register.html', {'departments': departments})


def patient_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        age = request.POST.get('age')
        gender = request.POST['gender']
        contact_num = request.POST['contact_num']
        address = request.POST.get('address')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patient (name, age, gender, contact_num, address, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, age, gender, contact_num, address, email, password),
        )
        conn.commit()
        cursor.close()
        conn.close()

        messages.success(request, "Patient registered successfully.")
        return redirect('login')

    return render(request, 'patient_register.html')
    

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Doctor Login - Email: {email}, Password: {password}")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM doctor WHERE email=%s", [email])
            doctor = cursor.fetchone()
            print(f"Doctor data: {doctor}")

            if doctor:
                stored_password = doctor[6]  
                full_username=doctor[1]
                
                username = full_username.split(' ', 1)[0]
                
                print(f"Stored password: {stored_password}")

                if check_password(password,stored_password):
                    print(f"Password match for doctor: {email}")
                    return redirect(f'/doctor_dashboard/{username}/')

            messages.error(request, "Invalid email or password.")
        finally:
            cursor.close()
            conn.close()

    return render(request, 'doctor_login.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Patient Login - Email: {email}, Password: {password}")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM patient WHERE email=%s", [email])
            patient = cursor.fetchone()
            print(f"Patient data: {patient}")

            if patient:
                stored_password = patient[7]  
                full_username = patient[1]  

                username = full_username.split(' ', 1)[0]

                if check_password(password, stored_password):
                    print(f"Password match for patient: {email}")
                    return redirect(f'/patient_dashboard/{username}/')

            messages.error(request, "Invalid email or password.")
        finally:
            cursor.close()
            conn.close()

    return render(request, 'login.html')
