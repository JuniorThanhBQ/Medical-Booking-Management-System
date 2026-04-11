import json
import os
import sys
import traceback
from datetime import datetime

from werkzeug.security import generate_password_hash

current_directory = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_directory, "../../"))
sys.path.insert(0, root_directory)

from src import create_app, db
from src.modules.appointments.models import (Appointment, MedicalRecord,
                                             MedicalRecordType, StatusRole)
from src.modules.doctors.models import (DayOfWeek, DoctorProfile,
                                        MedicalService, Specialty, VisitType,
                                        WorkDate, WorkSchedule)
from src.modules.notification.models import (DeliveryStatus, Notification,
                                             NotificationType)
from src.modules.users.models import GenderRole, PatientProfile, User, UserRole


class FixtureLoader:
    def __init__(self, data):
        self.data = data
        self.specialty_mapping = {}
        self.medical_service_mapping = {}
        self.user_mapping = {}
        self.doctor_profile_mapping = {}
        self.patient_profile_mapping = {}
        self.work_schedule_mapping = {}
        self.medical_record_mapping = {}
        self.appointment_mapping = {}

    def load_specialties(self):
        for specialty_data in self.data.get("specialties", []):
            specialty = Specialty(
                name=specialty_data["name"],
                description=specialty_data["description"],
                level=specialty_data["level"]
            )
            db.session.add(specialty)
            db.session.flush()
            self.specialty_mapping[specialty_data["id"]] = specialty.id

    def load_medical_services_and_visit_types(self):
        for service_data in self.data.get("medical_services", []):
            service = MedicalService(
                name=service_data["name"],
                description=service_data["description"],
                specialty_id=self.specialty_mapping[service_data["specialty_id"]]
            )
            db.session.add(service)
            db.session.flush()
            self.medical_service_mapping[service_data["id"]] = service.id

        for visit_data in self.data.get("visit_types", []):
            visit_type = VisitType(
                name=visit_data["name"],
                duration_minutes=visit_data["duration_minutes"],
                buffer_before=visit_data.get("buffer_before", 0),
                buffer_after=visit_data.get("buffer_after", 0),
                medical_service_id=self.medical_service_mapping[visit_data["medical_service_id"]]
            )
            db.session.add(visit_type)
            db.session.flush()

    def load_users(self):
        for user_data in self.data.get("users", []):
            user = User(
                username=user_data["username"],
                password=generate_password_hash(user_data["password"]),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                role=UserRole[user_data["role"]]
            )
            db.session.add(user)
            db.session.flush()
            self.user_mapping[user_data["id"]] = user.id

    def load_profiles(self):
        for doctor_profile_data in self.data.get("doctor_profiles", []):
            profile = DoctorProfile(
                user_id=self.user_mapping[doctor_profile_data["user_id"]],
                phone=doctor_profile_data["phone"],
                gender=GenderRole[doctor_profile_data["gender"]],
                title=doctor_profile_data["title"],
                bio=doctor_profile_data["bio"],
                address=doctor_profile_data.get("address"),
                birthday=datetime.strptime(doctor_profile_data["birthday"],
                                           "%Y-%m-%d").date()
                if doctor_profile_data.get("birthday") else None,
                specialty_id=self.specialty_mapping[doctor_profile_data["specialty_id"]]
            )
            db.session.add(profile)
            db.session.flush()
            self.doctor_profile_mapping[doctor_profile_data["id"]] = profile.id

        for patient_profile_data in self.data.get("patient_profiles", []):
            profile = PatientProfile(
                user_id=self.user_mapping[patient_profile_data["user_id"]],
                phone=patient_profile_data["phone"],
                gender=GenderRole[patient_profile_data["gender"]],
                address=patient_profile_data.get("address"),
                birthday=datetime.strptime(patient_profile_data["birthday"],
                                           "%Y-%m-%d").date()
                if patient_profile_data.get("birthday") else None,
                medical_history=patient_profile_data.get("medical_history")
            )
            db.session.add(profile)
            db.session.flush()
            self.patient_profile_mapping[patient_profile_data["id"]] = profile.id

    def load_schedules(self):
        for work_schedule_data in self.data.get("work_schedules", []):
            schedule = WorkSchedule(
                title=work_schedule_data["title"],
                description=work_schedule_data["description"],
                start_time=datetime.strptime(work_schedule_data["start_time"],
                                             "%H:%M:%S").time(),
                end_time=datetime.strptime(work_schedule_data["end_time"],
                                           "%H:%M:%S").time(),
                doctor_id=self.doctor_profile_mapping[work_schedule_data["doctor_id"]]
            )
            db.session.add(schedule)
            db.session.flush()
            self.work_schedule_mapping[work_schedule_data["id"]] = schedule.id

        for work_date_data in self.data.get("work_dates", []):
            for day_string in work_date_data["days"]:
                work_date = WorkDate(
                    day_of_week=DayOfWeek[day_string],
                    work_schedule_id=self.work_schedule_mapping[work_date_data["work_schedule_id"]]
                )
                db.session.add(work_date)

    def load_medical_records_and_appointments(self):
        for medical_record_data in self.data.get("medical_records", []):
            record = MedicalRecord(
                note=medical_record_data.get("note"),
                type=MedicalRecordType[medical_record_data["type"]],
                diagnosis=medical_record_data["diagnosis"],
                prescription_text=medical_record_data["prescription_text"],
                treatment_orders=medical_record_data["treatment_orders"],
                doctor_profile_id=self.doctor_profile_mapping[medical_record_data["doctor_id"]],
                patient_profile_id=self.patient_profile_mapping[medical_record_data["patient_id"]]
            )
            db.session.add(record)
            db.session.flush()
            self.medical_record_mapping[medical_record_data["id"]] = record.id

        for appointment_data in self.data.get("appointments", []):
            medical_record_id = self.medical_record_mapping.get(
                appointment_data.get("medical_record_id")) \
                if appointment_data.get("medical_record_id") else None
            appointment = Appointment(
                name=appointment_data["name"],
                note=appointment_data["note"],
                status=StatusRole[appointment_data["status"]],
                appointment_date=datetime.strptime(appointment_data["appointment_date"],
                                                   "%Y-%m-%dT%H:%M:%S"),
                doctor_profile_id=self.doctor_profile_mapping[appointment_data["doctor_id"]],
                patient_profile_id=self.patient_profile_mapping[appointment_data["patient_id"]],
                medical_service_id=self.medical_service_mapping[appointment_data["medical_service_id"]],
                medical_record_id=medical_record_id
            )
            db.session.add(appointment)
            db.session.flush()
            self.appointment_mapping[appointment_data["id"]] = appointment.id

    def load_notifications(self):
        for notification_data in self.data.get("notifications", []):
            appointment_id = notification_data.get("appointment_id")
            mapped_appointment_id = self.appointment_mapping[appointment_id] \
                if appointment_id else None

            created_at = notification_data.get("created_at")
            created_dt = None
            if created_at:
                clean_str = created_at.replace("Z", "+00:00")
                created_dt = datetime.fromisoformat(clean_str)

            notification = Notification(
                title=notification_data["title"],
                message=notification_data["message"],
                is_read=notification_data.get("is_read", False),
                user_id=self.user_mapping[notification_data["user_id"]],
                appointment_id=mapped_appointment_id,
                type=NotificationType[notification_data["type"]],
                send_email=notification_data.get("send_email", False),
                email_status=DeliveryStatus[notification_data["email_status"]],
                created_date=created_dt
            )

            db.session.add(notification)

    def load_data(self):
        try:
            self.load_specialties()
            self.load_medical_services_and_visit_types()
            self.load_users()
            self.load_profiles()
            self.load_schedules()
            self.load_medical_records_and_appointments()
            self.load_notifications()

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            sys.exit(1)


def main():
    app = create_app()
    app.config["DISABLE_SIGNALS"] = True
    json_path = os.path.join(os.path.dirname(__file__), "data.json")

    if not os.path.exists(json_path):
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    with app.app_context():
        if User.query.first():
            return

        fixture_loader = FixtureLoader(data)
        fixture_loader.load_data()


if __name__ == "__main__":
    main()