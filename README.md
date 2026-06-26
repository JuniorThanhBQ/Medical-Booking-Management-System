# Medical Booking Management System (MBMS)

## I. Project Description
### 1. Introduction
The Medical Booking Management System (MBMS) project, formerly known as the online medical appointment booking application (Medical Appointment B3). The development team's direction is a PWA (Progressive Web App) and an NA (Native App - Android Focusing) that work well in practice, satisfying the management workflows related to "booking" for a specific clinic/hospital.
    
### 2. Objectives
There are three major objectives that the development team wants to achieve:
1. Meet the necessary functional criteria of a general "Booking" system. Develop functions that satisfactorily resolve the booking management requirements of a specific clinic/hospital.
2. The system works well in a real-world environment. The project's outcome is expected to be a product in PWA | NA form, allowing potential users to try it out with simple installation steps.
3. Develop the application following the AI-driven development (AIDD) and Scrum approach.


## II. Development Team

| Student ID | Full Name | Role | Specific Tasks |
| :--- | :--- | :--- | :--- |
| **2351050164** | Van Trung Thanh | Product Owner - Team member | Manage the application development process and QA - QC content of the project. In charge of the backend and CI/CD |
| **2351050133** | Nguyen Thanh Phong | Scrum master - Team member | Manage designs, functions, and the application interface to ensure usability. In charge of the frontend and End-User | 
| # | # | # | # | # |

## III. Technologies Used
 
### Main Technologies
| Container | Technology | Version | Reason for Use |
| :--- | :--- | :--- | :--- | 
| **Backend** | # | # | # |
| **Frontend** | # | # | # |
| **Database** | PostgreSQL | # | # |
| # | # | # | # |

### Other Technologies
- **Container:** Docker (v29.3.0) and Docker Compose (v5.1.0)
- **Version control:** Git (Latest) and GitHub
- **AI Agents**: Claude Agents (Free Version)

## IV. System Architecture (Old)
The system is designed based on the Client-Server architectural pattern with the REST architectural style. The four chosen attributes are functional suitability, security, reliability, and performance. 

In this, the system has 5 main containers and two auxiliary containers defined and executed via docker-compose.yml. 

Workflow Summary:
Client-side (Browser) → API Server → Redis: get cloudinary link/rarely changing payload → MySQL: query database if Redis does not have cached data. In addition, RabbitMQ handles asynchronous processing for appointment notifications.

**C4 Model - Container**
![b3_client_server_ architecture_image](docs/architecture/c4-container.png)

## V. Installation and Operation (Old)

### System Requirements
- Docker Desktop
- Git
- Ngrok, Cloudinary, Email Reputation service keys, and Google account app-password.

### Local Running
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8
    ```
2.  **Environment preparation:** Create a .env file following .env.example.
3.  **Launch in one of two ways:**
    - **Dev:** docker compose up -d --build
    - **Production:** docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

### Running as a Web Server
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8/web-server
    ```
2.  **Environment preparation:** Create a .env file following the template (required).
3.  **Launch:**
    ```bash
    docker compose -f docker-compose-server.prod.yml up -d --build
    ```
4.  **Get URL:** Visit http://localhost:7000/status to get the URL of the web app.

## VI. Access Information (Old)
The ports below may vary depending on the configuration in the .env file

- **Frontend (Local):** [http://localhost:81](http://localhost:81)
- **Backend API (Local):** [http://localhost:8000](http://localhost:8000)
- **RabbitMQ Management (Local):** [http://localhost:15672](http://localhost:15672)
- **Web app (Production):** [https://resonate-proponent-thrower.ngrok-free.dev](https://resonate-proponent-thrower.ngrok-free.dev) (Depends on ngrok)

## VII. Demo (Old)

**Demo:** [Medical-Appointment-Demo](https://drive.google.com/drive/u/0/folders/1DxsuBUrXGs3e7ExIcdaz8nEen7Jye9QF)

## VIII. Detailed Documentation
- [ADRs](docs/adrs/)
- [API Documentation](docs/api/)
- [Architecture](docs/architecture/)
- [Web server guide](web-server/README.md)