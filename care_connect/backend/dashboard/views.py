from django.shortcuts import render,redirect
from django.contrib import messages
from care_connect.views import get_db_connection
from django.http import JsonResponse
from datetime import datetime

def patient_dashboard(request, patient_id):
    # Query the patient profile using user_id
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM Patient WHERE patient_id = %s", [patient_id])
        patient_profile = cursor.fetchone()
        
        if patient_profile:
            full_username = patient_profile[1]  # Assuming patient's name is stored in index 1
            return render(request, 'patient_dashboard.html', {'user_id': patient_id, 'full_username': full_username})
        else:
            return redirect('home')
    finally:
        cursor.close()
        conn.close()


def doctor_dashboard(request, doctor_id):
    # Query the doctor profile using user_id
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Doctor WHERE doctor_id = %s", [doctor_id])
        doctor_profile = cursor.fetchone()
        
        if doctor_profile:
            full_username = doctor_profile[1]  # Assuming doctor's name is stored in index 1
            return render(request, 'doctor_dashboard.html', {'user_id': doctor_id, 'full_username': full_username})
        else:
            return redirect('home')
    finally:
        cursor.close()
        conn.close()
        
def admin_dashboard(request, username):
    return render(request, 'admin_dashboard.html', {'username': username})


def profile(request):
    user_id = request.session.get("user_id")
    user_type = request.session.get('user_type')
    conn = get_db_connection()
    cursor = conn.cursor()
    print(user_id)

    try:
        # Check if the user is a doctor
        if user_type == 'doctor':
            cursor.execute("SELECT * FROM doctor WHERE doctor_id = %s", [user_id])
            doctor_profile = cursor.fetchone()
            if doctor_profile:
                profile_data = {
                    'Doctor_id': doctor_profile[0],
                    'Name': doctor_profile[1],
                    'Specialization': doctor_profile[2],
                    'Contact_Number': doctor_profile[3],
                    'Schedule': doctor_profile[4],
                    }
                return render(request, 'doctor_profile.html', {'profile': profile_data})

        # Check if the user is a patient
        elif user_type == 'patient':
            cursor.execute("SELECT * FROM patient WHERE patient_id = %s", [user_id])
            patient_profile = cursor.fetchone()
            if patient_profile:
                profile_data = {
                    'Patient_id': patient_profile[0],
                    'Name': patient_profile[1],
                    'Age': patient_profile[2],
                    'Gender': patient_profile[3],
                    'Contact_Number': patient_profile[4],
                    'Address': patient_profile[5],
                    'Email': patient_profile[6],
                    }
                return render(request, 'patient_profile.html', {'profile': profile_data})

        messages.error(request, "Profile not found.")
        return redirect('home')

    finally:
        cursor.close()
        conn.close()


def make_appointments(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM department")
    departments = [row[0] for row in cursor.fetchall()]
    print("Departments:", departments)  # Debugging: check the list of departments
    return render(request, 'make_appointments.html', {'departments': departments})


def get_doctors(request, department):
    patient_id = request.session.get("user_id")    
    print("Selected department:", department)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM doctor WHERE specialization = %s", [department])
    doctors = [doctor[0] for doctor in cursor.fetchall()]
    
    available_times = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00", 
        "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00"
    ]
    
    if request.GET.get("doctor") and request.GET.get("date"):
        doctor = request.GET["doctor"]
        date = request.GET["date"]

        cursor.execute("SELECT doctor_id FROM doctor WHERE name = %s AND specialization = %s", [doctor, department])
        doctor = cursor.fetchone()
        doctor_id = doctor[0]

        cursor.execute("SELECT time FROM appointment WHERE doctor_id = %s AND date = %s", [doctor_id, date])
        booked_times = [row[0] for row in cursor.fetchall()]
        
        available_times = [t for t in available_times if t not in booked_times]
            
    if request.method == 'POST': 
        doctor = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')
        
        cursor.execute("SELECT doctor_id FROM doctor WHERE name= %s and specialization = %s", [doctor, department])
        result = cursor.fetchone()
        doctor_id = result[0]
        
        cursor.execute(
            "INSERT INTO appointment (date, time, status, patient_id, doctor_id) VALUES (%s, %s, %s, %s, %s)",
            (date, time, status, patient_id, doctor_id),
        )
        conn.commit()

        # **Redirect to total appointments page**
        return redirect("total_appointments")  # Make sure "total_appointments" is the correct name in urls.py

        
    return render(request, 'doctors_list.html', {'department': department, 'doctors': doctors, 'available_times': available_times})
    
def total_appointments(request):
    patient_id = request.session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT a.*, d.name AS doctor, specialization FROM appointment a JOIN doctor d  ON a.doctor_id = d.doctor_id where a.patient_id = %s;",[patient_id])
    appointments = cursor.fetchall()
    
    
    print(appointments)
    return render(request, 'total_appointments.html', {'appointments': appointments})

def my_appointments(request):
    doctor_id = request.session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT a.*, p.name AS patient, r.report_id
        FROM appointment a 
        JOIN patient p ON a.patient_id = p.patient_id
        LEFT JOIN report r ON a.appointment_id = r.appointment_id
        WHERE a.doctor_id = %s;
    """, [doctor_id])
    
    appointments = cursor.fetchall()
    print(appointments)
    
    return render(request, 'my_appointments.html', {'appointments': appointments})


def make_reports(request,appointment_id):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.*, 
            p.name AS patient_name, 
            p.patient_id AS patient_id, 
            d.name AS doctor_name, 
            d.doctor_id AS doctor_id
        FROM appointment a
        JOIN patient p ON a.patient_id = p.patient_id
        JOIN doctor d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_id = %s;
    """, [appointment_id])
    results=cursor.fetchall()
    print(results)
    patient = results[0][7]
    patient_id = results[0][8]
    doctor = results[0][9]
    doctor_id = results[0][10]
    date = results[0][1]
    print(doctor_id,doctor,patient,patient_id,date)
    
    if request.method == 'POST': 
        doctor = request.POST.get('doctor')
        patient = request.POST.get('patient')
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        date = request.POST.get('date')
        
        try:
            date = datetime.strptime(date, "%b. %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            print(f"Error: The date format '{date}' is invalid.")
        
        cursor.execute(
            "INSERT INTO report (doctor_id,patient_id,diagnosis,treatment,date,appointment_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (doctor_id,patient_id,diagnosis,treatment,date,appointment_id),
        )
        conn.commit()
        
        return redirect("my_appointments")

    return render(request, 'make_reports.html',{'doctor_name': doctor,'patient_name':patient,'date':date})

def view_reports(request,appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            r.*, 
            p.name AS patient_name,
            p.patient_id as patient_id,
            d.name AS doctor_name,
            d.doctor_id as doctor_id
        FROM report r
        JOIN patient p ON r.patient_id = p.patient_id
        JOIN doctor d ON r.doctor_id = d.doctor_id
        WHERE r.appointment_id = %s;
    """, [appointment_id])
    appointment=cursor.fetchall()
    print("appointment",appointment)

    if not appointment:  # If no report exists
        return render(request, 'view_reports.html', {'error_message': 'Report yet to be generated.'})
    
    appointment_details = {
        'appointment_id': appointment_id,
        'date': appointment[0][1],
        'diagnosis': appointment[0][2],
        'treatment': appointment[0][3],
        'patient_name': appointment[0][8],
        'doctor_name': appointment[0][10],
    }
    print(appointment_details)
    return render(request, 'view_reports.html',{'appointment':appointment_details}) 