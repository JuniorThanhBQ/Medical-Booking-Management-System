import json
import os
import sys
from datetime import datetime

from werkzeug.security import generate_password_hash

current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, root_dir)

from src import create_app, db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.auth_profile.models import (CtaLabel, DoctorProfile,
                                             GenderRole, PatientProfile,
                                             Specialty, User, UserRole)
from src.modules.doctor.models import DayOfWeek, WorkDate, WorkSchedule
from src.modules.medical_records.models import MedicalRecord, MedicalRecordType
from src.modules.notification.models import Notification


def load_fixtures(app):
    fixture_path = os.path.join(os.path.dirname(__file__), "data.json")
    if not os.path.exists(fixture_path):
        print(f"Lỗi: Không tìm thấy file {fixture_path}")
        return

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with app.app_context():
        try:
            if User.query.first():
                print("Database đã có dữ liệu.")
                return

            specialty_map = {}
            for sp in data.get("specialties", []):
                specialty = Specialty(
                    name=sp["name"],
                    description=sp["description"],
                    level=sp["level"],
                    cta_label=CtaLabel[sp["cta_label"]]
                )
                db.session.add(specialty)
                db.session.flush()
                specialty_map[sp["id"]] = specialty.id

            user_map = {}
            for u in data.get("users", []):
                user = User(
                    username=u["username"],
                    password=generate_password_hash(u["password"]),
                    first_name=u["first_name"],
                    last_name=u["last_name"],
                    email=u["email"],
                    role=UserRole[u["role"]]
                )
                db.session.add(user)
                db.session.flush()
                user_map[u["id"]] = user.id

            doc_profile_map = {}
            for dp in data.get("doctor_profiles", []):
                profile = DoctorProfile(
                    user_id=user_map[dp["user_id"]],
                    phone=dp["phone"],
                    gender=GenderRole[dp["gender"]],
                    title=dp["title"],
                    bio=dp["bio"],
                    address=dp.get("address"),
                    birthday=datetime.strptime(dp["birthday"], "%Y-%m-%d").date() if dp.get("birthday") else None,
                    specialty_id=specialty_map[dp["specialty_id"]]
                )
                db.session.add(profile)
                db.session.flush()
                doc_profile_map[dp["id"]] = profile.id

            pat_profile_map = {}
            for pp in data.get("patient_profiles", []):
                profile = PatientProfile(
                    user_id=user_map[pp["user_id"]],
                    phone=pp["phone"],
                    gender=GenderRole[pp["gender"]],
                    address=pp.get("address"),
                    birthday=datetime.strptime(pp["birthday"], "%Y-%m-%d").date() if pp.get("birthday") else None,
                    medical_history=pp.get("medical_history")
                )
                db.session.add(profile)
                db.session.flush()
                pat_profile_map[pp["id"]] = profile.id

            ws_map = {}
            for ws in data.get("work_schedules", []):
                schedule = WorkSchedule(
                    title=ws["title"],
                    description=ws["description"],
                    start_time=datetime.strptime(ws["start_time"], "%H:%M:%S").time(),
                    end_time=datetime.strptime(ws["end_time"], "%H:%M:%S").time(),
                    doctor_id=doc_profile_map[ws["doctor_id"]]
                )
                db.session.add(schedule)
                db.session.flush()
                ws_map[ws["id"]] = schedule.id

            for wd in data.get("work_dates", []):
                for day_str in wd["days"]:
                    work_date = WorkDate(
                        day_of_week=DayOfWeek[day_str],
                        work_schedule_id=ws_map[wd["work_schedule_id"]]
                    )
                    db.session.add(work_date)

            med_record_map = {}
            for mr in data.get("medical_records", []):
                record = MedicalRecord(
                    note=mr.get("note"),
                    type=MedicalRecordType[mr["type"]],
                    diagnosis=mr["diagnosis"],
                    prescription_text=mr["prescription_text"],
                    treatment_orders=mr["treatment_orders"],
                    doctor_profile_id=doc_profile_map[mr["doctor_id"]],
                    patient_profile_id=pat_profile_map[mr["patient_id"]]
                )
                db.session.add(record)
                db.session.flush()
                med_record_map[mr["id"]] = record.id

            appt_map = {}
            for appt in data.get("appointments", []):
                m_id = med_record_map.get(appt.get("medical_record_id")) if appt.get("medical_record_id") else None
                appointment = Appointment(
                    name=appt["name"],
                    note=appt["note"],
                    status=StatusRole[appt["status"]],
                    appointment_date=datetime.strptime(appt["appointment_date"], "%Y-%m-%dT%H:%M:%S"),
                    doctor_profile_id=doc_profile_map[appt["doctor_id"]],
                    patient_profile_id=pat_profile_map[appt["patient_id"]],
                    medical_record_id=m_id
                )
                db.session.add(appointment)
                db.session.flush()
                appt_map[appt["id"]] = appointment.id

            for nt in data.get("notifications", []):
                notification = Notification(
                    title=nt["title"],
                    message=nt["message"],
                    is_read=nt["is_read"],
                    user_id=user_map[nt["user_id"]],
                    appointment_id=appt_map[nt["appointment_id"]]
                )
                db.session.add(notification)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"{str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    app = create_app()
    load_fixtures(app)