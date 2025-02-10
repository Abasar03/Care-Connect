from django.shortcuts import render,redirect
from django.contrib import messages
from care_connect.views import get_db_connection
from django.http import JsonResponse
from datetime import datetime,timedelta

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
        
def admin_dashboard(request):
    if not request.session.get('is_admin_logged_in'):
        messages.error(request, "You must log in first.")
        return redirect('admin_login')

    return render(request, 'admin_dashboard.html')

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
    
    # Compute tomorrow's date in YYYY-MM-DD format
    tomorrow = (datetime.today().date() + timedelta(days=1)).isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM doctor WHERE specialization = %s", [department])
    doctors = [doctor[0] for doctor in cursor.fetchall()]
    
    available_times = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00", 
        "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00"
    ]
    
    # Use 'selected_date' instead of 'date' to avoid shadowing the datetime.date class
    if request.GET.get("doctor") and request.GET.get("date"):
        doctor = request.GET["doctor"]
        selected_date = request.GET["date"]

        cursor.execute(
            "SELECT doctor_id FROM doctor WHERE name = %s AND specialization = %s",
            [doctor, department]
        )
        doctor_record = cursor.fetchone()
        if doctor_record:
            doctor_id = doctor_record[0]
            cursor.execute(
                "SELECT time FROM appointment WHERE doctor_id = %s AND date = %s",
                [doctor_id, selected_date]
            )
            booked_times = [row[0] for row in cursor.fetchall()]
            available_times = [t for t in available_times if t not in booked_times]
            
    if request.method == 'POST': 
        doctor = request.POST.get('doctor')
        selected_date = request.POST.get('date')  # Renamed variable
        time_val = request.POST.get('time')
        status = request.POST.get('status')
        
        cursor.execute(
            "SELECT doctor_id FROM doctor WHERE name = %s and specialization = %s", 
            [doctor, department]
        )
        result = cursor.fetchone()
        doctor_id = result[0]
        
        cursor.execute(
            "INSERT INTO appointment (date, time, status, patient_id, doctor_id) VALUES (%s, %s, %s, %s, %s)",
            (selected_date, time_val, status, patient_id, doctor_id)
        )
        conn.commit()
        
        return redirect("total_appointments")
        
    return render(request, 'get_doctors.html', {
        'department': department, 
        'doctors': doctors, 
        'available_times': available_times,
        'tomorrow': tomorrow
    })

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

def patient_list(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    print(patients)
    return render(request, 'patient_list.html', {'patients': patients})

def doctor_list(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    print(doctors)
    return render(request, 'doctor_list.html', {'doctors': doctors})

def appointment_list(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT a.*,p.name as patient_name ,d.name as doctor_name FROM appointment a join patient p on a.patient_id = p.patient_id join doctor d on a.doctor_id = d.doctor_id;")
    appointments = cursor.fetchall()
    print(appointments)
    return render(request, 'appointment_list.html', {'appointments': appointments})

def report_list(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT r.*,p.name as patient_name,d.name as doctor_name from report r join patient p on r.patient_id =  p.patient_id join doctor d on r.doctor_id = d.doctor_id;")
    reports = cursor.fetchall()
    print(reports)
    return render(request, 'report_list.html', {'reports': reports})

from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

def delete_entity(request, entity_type, entity_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            if entity_type == 'doctor':
                # Delete all appointments related to this doctor
                cursor.execute("DELETE FROM appointment WHERE doctor_id = %s", [entity_id])
                
                # Delete all reports related to this doctor
                cursor.execute("DELETE FROM report WHERE doctor_id = %s", [entity_id])
                
                # Now delete the doctor
                cursor.execute("DELETE FROM doctor WHERE doctor_id = %s", [entity_id])
                
                messages.success(request, "Doctor successfully removed!")  # Success message


                return redirect('doctor_list')

            elif entity_type == 'patient':
                # Delete all appointments related to this patient
                cursor.execute("DELETE FROM appointment WHERE patient_id = %s", [entity_id])
                
                # Delete all reports related to this patient
                cursor.execute("DELETE FROM report WHERE patient_id = %s", [entity_id])
                
                # Now delete the patient
                cursor.execute("DELETE FROM patient WHERE patient_id = %s", [entity_id])

                messages.success(request, "Patient successfully removed!")  # Success message

                return redirect('patient_list')

            elif entity_type == 'appointment':
                # Delete the appointment
                cursor.execute("DELETE FROM appointment WHERE appointment_id = %s", [entity_id])

                messages.success(request, "Appointment successfully removed!")  # Success message

                return redirect('appointment_list')

            elif entity_type == 'report':
                # Delete the report
                cursor.execute("DELETE FROM report WHERE report_id = %s", [entity_id])

                messages.success(request, "Report successfully removed!")  # Success message

                return redirect('report_list')

            else:
                return HttpResponse("Invalid entity type", status=400)

    return HttpResponse("Invalid request", status=400)
