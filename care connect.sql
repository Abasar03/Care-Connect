CREATE TABLE admin (
    admin_id SERIAL PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,        
    password VARCHAR(255) NOT NULL
);

CREATE TABLE department (
    dep_id SERIAL PRIMARY KEY,  
    name VARCHAR(100) NOT NULL,                
    location VARCHAR(100) NOT NULL,
    admin_id INT,                             
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

CREATE TABLE doctor (
    doctor_id SERIAL PRIMARY KEY, 
    name VARCHAR(100) NOT NULL,                   
    specialization VARCHAR(100),               
    contact_num BIGINT,                            
    schedule VARCHAR(50),                               
    email VARCHAR(150) NOT NULL UNIQUE,          
    password VARCHAR(255) NOT NULL,              
    dep_id INT,                                
    admin_id INT,                              
    FOREIGN KEY (dep_id) REFERENCES department(dep_id) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

CREATE TABLE patient (
    patient_id SERIAL PRIMARY KEY, 
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(100),               
    contact_num BIGINT,                            
    address VARCHAR(50),                               
    email VARCHAR(150) NOT NULL UNIQUE,          
    password VARCHAR(255) NOT NULL,                                           
    admin_id INT,                              
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY, 
    date DATE,
    time VARCHAR(50),
    status VARCHAR(50),                               
    doctor_id INT,
    patient_id INT,
    admin_id INT,   
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

CREATE TABLE report (
    report_id SERIAL PRIMARY KEY, 
    date DATE,             
    diagnosis VARCHAR(50),                               
    treatment VARCHAR(50),
    doctor_id INT,
    patient_id INT,
    admin_id INT,   
    appointment_id INT,
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointment(appointment_id) ON DELETE CASCADE
);

Insert INTO admin (email, password)
VALUES ('your_email', crypt('your_password', gen_salt('bf')));;
    -- Replace your_email and your_password with your actual email and password.
    
INSERT INTO department (name, location, admin_id)
VALUES 
    ('Cardiology', 'Building A',1),
    ('Neurology', 'Building B',1),
    ('Orthopedics', 'Building C',1),
    ('Pediatrics', 'Building A',1),
    ('Medicine', 'Building B',1),
    ('Dermatology', 'Building C',1);



