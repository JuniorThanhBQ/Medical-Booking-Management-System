# Medical Booking Management System (MBMS)

## I. Project Description
### 1. Introduction
The Medical Booking Management System (MBMS) project, formerly known as the online medical appointment booking application (Medical Appointment B3). The development team's direction is to build a PWA (Progressive Web App) and a NA (Native App - Android Focusing) that work well in real life, satisfying management business requirements related to "booking" for a specific clinic/hospital.
    
### 2. Objectives
There are three major objectives that the development team wants to achieve:
1. Satisfy the necessary business criteria of a general "Booking" system. Develop functions that satisfactorily resolve the management business requirements of a "Booking" system for a specific clinic / hospital.
2. The system functions well in real-world environments; the expected project outcome is a PWA | NA product allowing potential users to try it with simple installation steps.
3. Develop the application following the AI-driven development (AIDD) and Scrum approach.


## II. Development Team

| Student ID | Full Name | Role | Specific Tasks |
| :--- | :--- | :--- | :--- |
| **2351050164** | Văn Trung Thành | Product Owner - Team Member | Manage the application development process and QA-QC content of the project. Responsible for the backend and CI/CD |
| **2351050133** | Nguyễn Thanh Phong | Scrum Master - Team Member | Manage the application design, functionality, and interface to ensure usability. Responsible for the frontend and End-User experience | 
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
The system is designed based on the Client-Server architectural pattern with REST architectural style. The four selected qualities are functional suitability, security, reliability, and performance. 

In this, the system has 5 main containers and two secondary containers defined and run via docker-compose.yml. 

Summary of operational flow:
Client-side (Browser) → API Server → Redis: retrieve cloudinary links/infrequently changing payloads → MySQL: query data if Redis has no cache. In addition, RabbitMQ processes asynchronous appointment notifications.

**C4 Model - Container**
![b3_client_server_ architecture_image](docs/architecture/c4-container.png)

## V. Installation and Operation (Old)

### System Requirements
- Docker Desktop
- Git
- Ngrok, Cloudinary, Email Reputation service keys, and Google account app password.

### Running Locally
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8
    ```
2.  **Prepare environment:** Create .env file following .env.example template.
3.  **Launch using one of the two ways:**
    - **Dev:** docker compose up -d --build
    - **Production:** docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

### Running as a Web Server
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8/web-server
    ```
2.  **Prepare environment:** Create .env file according to the template (required).
3.  **Launch:**
    ```bash
    docker compose -f docker-compose-server.prod.yml up -d --build
    ```
4.  **Get URL:** Access http://localhost:7000/status to get the web app URL.

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
- [Web Server Guide](web-server/README.md)
