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

def doctor_login(request):
    return render(request,'doctor_login.html')



# Utility function to get database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )


# Registration View


def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        hashed_password = make_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        if role == 'doctor':
            dep_name = request.POST.get('department')
            print("HEYYY")
            print(dep_name)
            cursor.execute("SELECT dep_id FROM department WHERE name = %s", (dep_name,))
            dep_row = cursor.fetchone()
            print(dep_row)
            
            if dep_row:
                dep_id = dep_row[0]
                print(dep_id)
            else:
                messages.error(request, "Invalid department selected.")
                return render(request, 'register.html')
            
            specialization = request.POST.get('specialization')
            schedule = request.POST.get('schedule')
            contact_num = request.POST.get('contact_num')
            dep_id = request.POST.get('dep_id')
            cursor.execute(
                "INSERT INTO doctor (name, email, password, specialization, contact_num, schedule, dep_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (name, email, hashed_password, specialization, contact_num, schedule, dep_id)
            )
        elif role == 'patient':
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            contact_num = request.POST.get('contact_num')
            address = request.POST.get('address')
            cursor.execute(
                "INSERT INTO patient (name, age, gender, contact_num, address, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (name, age, gender, contact_num, address, email, hashed_password)
            )

        conn.commit()
        cursor.close()
        conn.close()
        messages.success(request, "Registration successful.")
        return redirect('login')

    else:
        # Fetching departments for the form
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT dep_id, name FROM department")
        departments = cursor.fetchall()
        cursor.close()
        conn.close()

        return render(request, 'register.html', {'departments': departments})
# Login View for Admin, Doctor, and Patient
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"{email}\n{password}")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check Doctor Table
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM doctor where email=%s", [email])
                doctor = cursor.fetchall()
                print(doctor)

                if doctor:
                    # Assuming password is the 7th field in the doctor table (adjust as needed)
                    stored_password = doctor[7]
                    print(f"Entered password is and stored pas(password,{stored_password}")
                
                    if check_password(password, stored_password):
                        print(f"Entered password is{stored_password}")

                        return redirect('doctor_dashboard')

                # Check Patient Table
                cursor.execute("SELECT * FROM patient WHERE email=%s", [email])
                patient = cursor.fetchone()
                print(patient)

                if patient:
                    # Assuming password is the 6th field in the patient table (adjust as needed)
                    stored_password = patient[7]
                    print(f"stored_password: {stored_password}")
                    if check_password(password, stored_password):
                        print(f"Entered password is and stored pas(password,{stored_password}")
                        return redirect('/dashboard/patient_dashboard')

                # If no matching user or invalid password
                messages.error(request, "Invalid email or password.")
        finally:
                # Ensure cursor and connection are closed
                cursor.close()
                conn.close()

    return render(request, 'login.html')