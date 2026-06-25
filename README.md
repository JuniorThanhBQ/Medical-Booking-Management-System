# Medical Booking Management System (MBMS)

## I. Project Description
### 1. Introduction
The Medical Booking Management System (MBMS) project, formerly known as the online medical appointment booking application (Medical Appointment B3). The development team's direction is a PWA (Progressive Web App) and an NA (Native App - Android Focusing) that work well in practice, meeting the management business requirements related to "booking" for a specific clinic/hospital.
    
### 2. Objectives
There are three major objectives that the development team aims to achieve:
1. Meet the necessary business criteria of a general "Booking" system. Develop functions that satisfactorily address the "Booking" management business requirements of a specific clinic/hospital.
2. The system works well in a real-world environment, with the expected project outcome being a PWA | NA product allowing potential users to try it out with simple installation steps.
3. Develop the application following the AI-driven development (AIDD) and Scrum approaches.


## II. Development Team

| Student ID | Full Name | Role | Specific Tasks |
| :--- | :--- | :--- | :--- |
| **2351050164** | Văn Trung Thành | Product Owner - Team members | Managing the application development process and project QA - QC content. In charge of back-end and CI/CD |
| **2351050133** | Nguyễn Thanh Phong | Scrum master - Team members | Managing application design, features, and interface to ensure usability. In charge of front-end and End-User | 
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
The system is designed based on the Client–Server architecture pattern with a REST architectural style. The four selected characteristics are functional suitability, security, reliability, and performance. 

Among these, the system has 5 main containers and two secondary containers defined and executed via docker-compose.yml. 

Workflow summary:
Client-side (Browser) → API Server → Redis: retrieve Cloudinary links/rarely changing payloads → MySQL: query data if there is no cache in Redis. In addition, RabbitMQ handles asynchronous processing for appointment notifications.

**C4 Model - Container**
![b3_client_server_ architecture_image](docs/architecture/c4-container.png)

## V. Installation and Operation (Old)

### System Requirements
- Docker Desktop
- Git
- API keys/credentials for Ngrok, Cloudinary, Email Reputation, and a Google account app-password.

### Running Locally
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8
    ```
2.  **Prepare the environment:** Create a `.env` file based on the `.env.example` template.
3.  **Run using one of the following methods:**
    - **Dev:** docker compose up -d --build
    - **Production:** docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

### Running as a Web Server 
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8/web-server
    ```
2.  **Prepare the environment:** Create a `.env` file based on the template (required).
3.  **Launch:**
    ```bash
    docker compose -f docker-compose-server.prod.yml up -d --build
    ```
4.  **Get URL:** Access http://localhost:7000/status to get the web app URL.

## VI. Access Information (Old)
The ports below may vary depending on the configuration in the `.env` file.

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
