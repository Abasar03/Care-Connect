from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from care_connect.views import get_db_connection
from datetime import datetime,timedelta

def patient_dashboard(request, patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM Patient WHERE patient_id = %s", [patient_id])
        patient_profile = cursor.fetchone()
        
        if patient_profile:
            full_username = patient_profile[1] 
            return render(request, 'patient_dashboard.html', {'user_id': patient_id, 'full_username': full_username})
        else:
            return redirect('home')
    finally:
        cursor.close()
        conn.close()


def doctor_dashboard(request, doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Doctor WHERE doctor_id = %s", [doctor_id])
        doctor_profile = cursor.fetchone()
        
        if doctor_profile:
            full_username = doctor_profile[1]  
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
                    'Email': doctor_profile[5],
                    }
                return render(request, 'doctor_profile.html', {'profile': profile_data})

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
    print("Departments:", departments) 
    return render(request, 'make_appointments.html', {'departments': departments})


def get_doctors(request, department):
    patient_id = request.session.get("user_id")
    print("Selected department:", department)
    
    tomorrow = (datetime.today().date() + timedelta(days=1)).isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM doctor WHERE specialization = %s", [department])
    doctors = [doctor[0] for doctor in cursor.fetchall()]
    
    available_times = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00", 
        "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00"
    ]
    
    selected_doctor = request.GET.get("doctor") or request.POST.get('doctor')
    selected_date = request.GET.get("date") or request.POST.get('date')
    
    if selected_doctor and selected_date:
        print("doctor and selected date", selected_doctor, selected_date)

        cursor.execute(
            "SELECT doctor_id FROM doctor WHERE name = %s AND specialization = %s",
            [selected_doctor, department]
        )
        doctor_record = cursor.fetchone()
        if doctor_record:
            doctor_id = doctor_record[0]
            print("doctor id", doctor_id)
            cursor.execute(
                "SELECT time FROM appointment WHERE doctor_id = %s AND date = %s",
                [doctor_id, selected_date]
            )
            booked_times = [row[0] for row in cursor.fetchall()]
            print("Booked times:", booked_times)
            available_times = [t for t in available_times if t not in booked_times]
            print("Available times:", available_times)
            
    if request.method == 'POST': 
        time_val = request.POST.get('time')
        status = request.POST.get('status')
        
        cursor.execute(
            "SELECT COUNT(*) FROM appointment WHERE doctor_id = %s AND date = %s AND time = %s",
            [doctor_id, selected_date, time_val]
        )
        appointment_exists = cursor.fetchone()[0]

        if appointment_exists > 0:
            messages.error(request, "The selected time slot is already booked. Please choose another time.")
            return redirect(request.path)
        else:
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
        'tomorrow': tomorrow,
        'selected_doctor': selected_doctor,
        'selected_date': selected_date
    })

def total_appointments(request):
    patient_id = request.session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT a.*, d.name AS doctor, d.specialization
        FROM appointment a 
        JOIN doctor d ON a.doctor_id = d.doctor_id
        WHERE a.patient_id = %s;
    """, [patient_id])
    
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

    if not appointment:  
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
    cursor.execute("""
        SELECT 
            a.*, 
            p.name AS patient_name, 
            d.name AS doctor_name,
            r.report_id  
        FROM appointment a
        JOIN patient p ON a.patient_id = p.patient_id
        JOIN doctor d ON a.doctor_id = d.doctor_id
        LEFT JOIN report r ON a.appointment_id = r.appointment_id;
    """)
    
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

def delete_entity(request, entity_type, entity_id):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        if entity_type == 'doctor':
            cursor.execute("DELETE FROM appointment WHERE doctor_id = %s", [entity_id])
            
            cursor.execute("DELETE FROM report WHERE doctor_id = %s", [entity_id])
            
            cursor.execute("DELETE FROM doctor WHERE doctor_id = %s", [entity_id])
            
            messages.success(request, "Doctor successfully removed!")  

            return redirect('doctor_list')

        elif entity_type == 'patient':
            cursor.execute("DELETE FROM appointment WHERE patient_id = %s", [entity_id])
            
            cursor.execute("DELETE FROM report WHERE patient_id = %s", [entity_id])
            
            cursor.execute("DELETE FROM patient WHERE patient_id = %s", [entity_id])

            messages.success(request, "Patient successfully removed!")  

            return redirect('patient_list')

        elif entity_type == 'appointment':
            cursor.execute("DELETE FROM appointment WHERE appointment_id = %s", [entity_id])

            messages.success(request, "Appointment successfully removed!")  

            return redirect('appointment_list')

        elif entity_type == 'report':
            cursor.execute("DELETE FROM report WHERE report_id = %s", [entity_id])

            messages.success(request, "Report successfully removed!")  

            return redirect('report_list')

        else:
            return HttpResponse("Invalid entity type", status=400)

    return HttpResponse("Invalid request", status=400)
