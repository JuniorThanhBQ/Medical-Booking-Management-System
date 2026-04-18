import os
import uuid
from datetime import datetime, timedelta

from werkzeug.utils import secure_filename

from src.modules.appointments.models import StatusRole
from src.modules.doctors.models import DayOfWeek
from src.modules.doctors.rabbitmq.tasks import \
    process_doctor_registration_email
from src.utils.appointment.formatter_utils import format_appointment
from src.utils.doctor.formatter_utils import (format_speciality_output,
                                              parse_and_validate_date)
from src.utils.doctor.time_slots_utils import (check_is_conflicting,
                                               format_work_schedule,
                                               is_valid_working_day)
from src.utils.handle_db_errors import handle_db_errors


class DoctorService:
    def __init__(self, doctor_repository, appointment_repository):
        self.doctor_repository = doctor_repository
        self.appointment_repository = appointment_repository

    def get_available_time_slots(self, doctor, target_date, medical_service):
        is_valid, schedule = is_valid_working_day(doctor, target_date)
        if not is_valid or not medical_service.visit_type:
            return []

        visit_type = medical_service.visit_type
        duration = visit_type.duration_minutes + visit_type.buffer_before + visit_type.buffer_after

        appointments = self.doctor_repository.get_booked_appointments(doctor.profile.id, target_date)
        doctor_name = f"{doctor.first_name} {doctor.last_name} ".strip()
        locked_dates = self.appointment_repository.get_locked_time_slots(doctor_name, target_date)

        current_date = datetime.combine(target_date, schedule.start_time)
        end_date = datetime.combine(target_date, schedule.end_time)
        now_date = datetime.now()
        available = []

        while current_date + timedelta(minutes=duration) <= end_date:
            if (current_date > now_date
                    and not check_is_conflicting(current_date, duration, appointments)
                    and current_date not in locked_dates):
                available.append(current_date.isoformat() + "Z")
            current_date += timedelta(minutes=duration)

        return available

    @handle_db_errors
    def get_my_schedule_service(self, current_user):
        if current_user.role.name != "DOCTOR":
            return {"message": "Chỉ bác sĩ mới có quyền truy cập"}, "FORBIDDEN"

        profile = current_user.profile
        if not profile or profile.profile_type != "doctor":
            return {"message": "Hồ sơ bác sĩ không hợp lệ"}, "NOT_FOUND"

        work_schedule_data = None
        if profile.work_schedule:
            work_schedule_data = format_work_schedule(profile.work_schedule)

        now = datetime.now()
        statuses = [StatusRole.APPROVED, StatusRole.PENDING]
        upcoming_appointments = self.doctor_repository.get_upcoming_appointments(profile.id, now, statuses)

        appointment_data = [
            format_appointment(appointment=app, patient_user=app.patient.user, doctor=current_user)
            for app in upcoming_appointments
        ]

        result = {
            "workSchedule": work_schedule_data,
            "appointments": appointment_data
        }
        return result, "SUCCESS"

    @handle_db_errors
    def request_schedule_change_service(self, current_user, data):
        if current_user.role.name not in ["DOCTOR", "RECEPTIONIST", "ADMIN"]:
            return {"message": "Không đủ quyền hạn để yêu cầu đổi lịch"}, "FORBIDDEN"

        profile = current_user.profile
        if not profile or profile.profile_type != "doctor":
            return {"message": "Hồ sơ bác sĩ không hợp lệ"}, "NOT_FOUND"

        now = datetime.now()
        end_date = now + timedelta(days=30)
        statuses = [StatusRole.APPROVED, StatusRole.PENDING]

        conflicting = self.doctor_repository.is_conflict_appointment(profile.id, now, end_date, statuses)

        if conflicting:
            return {"message": "Vui lòng cập nhật các lịch hẹn bị ảnh hưởng truớc khi đổi."}, "FORBIDDEN"

        new_work_schedule_data = data.get("newWorkSchedule", {})
        if not new_work_schedule_data:
            return {"message": "Thiếu thông tin lịch làm việc mới"}, "ERROR_BAD_REQUEST"

        try:
            start_time = datetime.strptime(new_work_schedule_data.get("start_time", "00:00:00"), "%H:%M:%S").time()
            end_time = datetime.strptime(new_work_schedule_data.get("end_time", "00:00:00"), "%H:%M:%S").time()
        except ValueError:
            return {"message": "Định dạng không hợp lệ (HH:MM:SS)"}, "ERROR_BAD_REQUEST"

        work_schedule = self.doctor_repository.get_or_create_work_schedule(profile.id)
        work_schedule.title = new_work_schedule_data.get("title", work_schedule.title)
        work_schedule.description = new_work_schedule_data.get("description", work_schedule.description)
        work_schedule.start_time = start_time
        work_schedule.end_time = end_time

        work_days = new_work_schedule_data.get("work_date", [])
        days_enum = []
        for day_str in work_days:
            try:
                days_enum.append(DayOfWeek[day_str.upper()])
            except KeyError:
                pass

        self.doctor_repository.update_work_dates(work_schedule.id, days_enum)
        self.doctor_repository.commit_session()

        return {"message": "Cập nhật lịch thành công!"}, "SUCCESS"

    @handle_db_errors
    def get_specialties_service(self, page=1, per_page=5, keywords=None):
        pagination = self.doctor_repository.get_paginated_specialties(page, per_page, keywords)
        items = [format_speciality_output(specialty) for specialty in pagination.items]

        result = {
            "items": items,
            "meta": {
                "total": pagination.total,
                "pages": pagination.pages,
                "currentPage": pagination.page,
                "perPage": pagination.per_page,
                "hasNext": pagination.has_next,
                "hasPrev": pagination.has_prev
            }
        }
        return result, "SUCCESS"

    @handle_db_errors
    def get_doctors_service(self, page=1, per_page=5, keywords=None, specialty_id=None, work_dates=None):
        pagination = self.doctor_repository.get_paginated_doctors(
            page, per_page, keywords, specialty_id, work_days=work_dates)
        items = []

        for doctor in pagination.items:
            profile = doctor.profile
            items.append({
                "id": profile.id,
                "firstName": doctor.first_name,
                "lastName": doctor.last_name,
                "avatar": profile.avatar,
                "gender": profile.gender.name if profile.gender else None,
                "title": profile.title,
                "specialtyId": profile.specialty_id,
                "bio": profile.bio,
            })

        result = {
            "items": items,
            "meta": {
                "total": pagination.total,
                "pages": pagination.pages,
                "currentPage": pagination.page,
                "perPage": pagination.per_page,
                "hasNext": pagination.has_next,
                "hasPrev": pagination.has_prev
            }
        }
        return result, "SUCCESS"

    @handle_db_errors
    def get_medical_services_service(self, page=1, per_page=5, keywords=None, specialty_id=None):
        pagination = self.doctor_repository.get_paginated_medical_services(
            page, per_page=per_page, keywords=keywords, specialty_id=specialty_id)
        items = [{
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "specialtyId": service.specialty_id
        } for service in pagination.items]

        result = {
            "items": items,
            "meta": {
                "total": pagination.total,
                "pages": pagination.pages,
                "currentPage": pagination.page,
                "perPage": pagination.per_page,
                "hasNext": pagination.has_next,
                "hasPrev": pagination.has_prev
            }
        }
        return result, "SUCCESS"

    @handle_db_errors
    def get_medical_service_detail_service(self, service_id):
        service = self.doctor_repository.get_medical_service_by_id(service_id)
        if not service:
            return {"message": "Không tồn tại dịch vụ này"}, "NOT_FOUND"

        result = {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "specialty": {
                "id": service.specialty.id,
                "name": service.specialty.name,
                "level": service.specialty.level
            } if service.specialty else None,
            "visitType": {
                "id": service.visit_type.id,
                "name": service.visit_type.name,
                "durationMinutes": service.visit_type.duration_minutes
            } if service.visit_type else None
        }
        return result, "SUCCESS"

    @handle_db_errors
    def get_specialty_detail_service(self, specialty_id):
        specialty = self.doctor_repository.get_specialty_by_id(specialty_id)
        if not specialty:
            return {"message": "Không tồn tại chuyên khoa này"}, "NOT_FOUND"

        return format_speciality_output(specialty), "SUCCESS"

    @handle_db_errors
    def get_doctor_detail_service(self, doctor_id):
        doctor = self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor or not doctor.profile:
            return {"message": "Bác sĩ không tồn tại"}, "NOT_FOUND"

        profile = doctor.profile
        schedule_data = format_work_schedule(profile.work_schedule)

        result = {
            "id": profile.id,
            "firstName": doctor.first_name,
            "lastName": doctor.last_name,
            "email": doctor.email,
            "profile": {
                "avatar": profile.avatar,
                "dateOfBirth": profile.birthday.isoformat() if profile.birthday else None,
                "gender": profile.gender.name if profile.gender else None,
                "phone": profile.phone,
                "title": profile.title,
                "specialtyId": profile.specialty_id,
                "bio": profile.bio,
            },
            "workSchedule": schedule_data,
        }
        return result, "SUCCESS"

    @handle_db_errors
    def get_time_slots_service(self, doctor_id, date_str, service_id):
        if not service_id:
            return {"message": "Thiếu mã dịch vụ"}, "ERROR_BAD_REQUEST"

        doctor = self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor or not doctor.profile:
            return {"message": "Bác sĩ không tồn tại"}, "NOT_FOUND"

        target_date, err_msg = parse_and_validate_date(date_str)
        if err_msg:
            return {"message": err_msg}, "ERROR_BAD_REQUEST"

        medical_service = self.doctor_repository.get_medical_service_by_id(service_id)
        if not medical_service:
            return {"message": "Dịch vụ không tồn tại"}, "NOT_FOUND"

        profile = doctor.profile
        if profile.specialty_id != medical_service.specialty_id:
            return {"message": "Bác sĩ không cung cấp dịch vụ này"}, "ERROR_BAD_REQUEST"

        if not profile.work_schedule:
            return {"message": "Bác sĩ không tồn tại"}, "404"

        work_schedule_data = format_work_schedule(profile.work_schedule)
        available_slots = self.get_available_time_slots(doctor, target_date, medical_service)

        return [{
            "workSchedule": work_schedule_data,
            "availableTimeSlots": available_slots,
        }], "SUCCESS"

    def send_doctor_registration_service(self, data, cv_file):
        if not cv_file:
            return {"message": "Vui lòng đính kèm file CV"}, "BAD_REQUEST"

        filename = secure_filename(cv_file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        temp_dir = "/app/shared_tmp"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, unique_filename)

        cv_file.save(file_path)

        process_doctor_registration_email.delay(data, file_path, filename)

        return {"message": "Hồ sơ của bạn đã được tiếp nhận và đang xử lý."}, "SUCCESS"
