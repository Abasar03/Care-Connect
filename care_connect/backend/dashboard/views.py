from django.shortcuts import render,redirect
from django.contrib import messages
from care_connect.views import get_db_connection

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
    print("Selected department:", department)  # Debugging
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM doctor WHERE specialization = %s", [department])
    doctors = [doctor[0] for doctor in cursor.fetchall()]  # Extract only names
    print("Found doctors:", doctors)  # Debugging
    
    available_times = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00", 
        "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00"
    ]
    
    if request.method == 'POST': 
        
        doctor = request.POST.get('doctor[0]')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')
        
        print(doctor, date, time, status)
        
        cursor.execute("SELECT doctor_id FROM doctor WHERE name= %s", [doctor])
        doctor_id = cursor.fetchone()
        
        cursor.execute("SELECT time FROM appointment WHERE doctor_id = %s", [doctor_id])
        booked_times = [row[0] for row in cursor.fetchall()]
        available_times = [time for time in available_times if time not in booked_times]

        cursor.execute(
            "INSERT INTO appointment (date, time, status, patient_id, doctor_id) VALUES (%s, %s, %s, %s, %s)",
            (date, time, status, patient_id, doctor_id),
        )
        conn.commit()
        
    return render(request, 'doctors_list.html', {'department': department, 'doctors': doctors, 'available_times': available_times})
    
def total_appointments(request):
    patient_id = request.session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM appointment WHERE patient_id = %s", [patient_id])
    appointments = cursor.fetchall()
    
    return render(request, 'total_appointments.html', {'appointments': appointments})