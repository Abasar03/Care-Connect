# Care Connect
Care Connect is an intuitive hospital appointment management platform that allows users to create an account, book appointments with doctors, and view real-time availability fetched from the hospital’s scheduling system. The project is designed to simplify appointment booking and provide seamless healthcare access.

## Team Members
- [Abasar Paudyal](https://github.com/Abasar03)
- [Anil Banjade](https://github.com/Anil-Banjade)
- [Kohinoor Dallakoti](https://github.com/unpredictable-thing)

## Project Overview
Care Connect is designed to help users manage their hospital appointments efficiently. The platform offers features such as user registration, appointment scheduling, and real-time doctor availability updates. The technology stack includes:<br>

- Backend: Django
- Frontend: HTML/TailwindCSS
- Database: PostgreSQL for storing user data and appointment details

## Key Features

## Prerequisites
Before installing Care Connect, ensure you have:

- Python and Django installed on your machine
- TailwindCSS installed for frontend styling
- A PostgreSQL database set up
- A modern web browser

## Installation
Follow these steps to set up TrackFolio on your local machine:
1. Clone the repository:
```
[git clone https://github.com/yourusername/TrackFolio.git](https://github.com/Abasar03/Care_Connect.git)
```

2. Create a PostgreSQL database and run the SQL scripts provided in 'care connect.sql' to set up tables.

3. Create an environment file:
    - In the care_connect directory, create a .env file.
    - Add the required environment variables as listed in .env.example.  

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Run database migrations:
```
python manage.py migrate
```

6. Start the development server:
```
Start the development server:
```

## Usage
1. Open your web browser and go to http://localhost:8000 (or the port set in .env).
2. Register a new account or log in with an existing one.
3. Book an appointment with the appropriate doctor and department.

## Conbtributing
We welcome contributions to Care Connect. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
Care Connect is released under the MIT License. You are free to use, modify, and distribute the code under the license terms.

## Acknowledgments
Thanks to open-source contributors and tools that made this project possible.
Special thanks to Er. RAJAD Shakya for his support in providing us with this project.

## Future Enhancements
We plan to enhance Care Connect with the following features:

- **Online Payment:** Integrate online payment for seamless appointment booking.
- **Search Functionality:** Implement search functionality based on doctor name.
- **Mobile App:** Build a mobile version for better accessibility.
- **Dark Mode:** User-customizable themes for better UI/UX.

For more details, visit the project repositories:
**[Care Connect]**(https://github.com/Abasar03/Care-Connect/tree/main/care_connect)

By continuously improving Care Connect, we aim to provide an efficient and user-friendly hospital appointment system.
## Directory Structure
```
Care-Connect
├─ care_connect
│  ├─ care_connect
│  │  └─ python_files
│  ├─ dashboard
│  │  ├─ migrations
│  │  ├─ templates/dashboard
│  │  │  └─ dashbaord_html_files
│  │  └─ python_files
│  ├─ static/css
│  │  └─ css_files
│  ├─ templates
│  │  └─ html_files
│  ├─ theme
│  ├─ manage.py
│  ├─ package_lock.json
│  └─ package.json
├─ care connect proposal.pdf
├─ README.md
├─ care connect.sql
└─ requirements.txt
```
 
