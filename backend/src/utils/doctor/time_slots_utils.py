from datetime import timedelta


def check_is_conflicting(slot_start, duration, appointments):
    if isinstance(duration, int):
        duration_td = timedelta(minutes=duration)
    else:
        duration_td = duration

    slot_end = slot_start + duration_td

    for appointment in appointments:
        appointment_start = appointment.appointment_date

        if appointment.medical_service and appointment.medical_service.visit_type:
            visit_type = appointment.medical_service.visit_type
            appointment_duration_minutes = (visit_type.duration_minutes
                                            + visit_type.buffer_before
                                            + visit_type.buffer_after)
        else:
            appointment_duration_minutes = 30

        appointment_end = appointment_start + timedelta(minutes=appointment_duration_minutes)

        if slot_start < appointment_end and slot_end > appointment_start:
            return True

    return False


def is_valid_working_day(doctor, target_date):
    if not doctor.profile or doctor.profile.profile_type != "doctor":
        return False, None

    schedule = doctor.profile.work_schedule
    if not schedule:
        return False, None

    target_day_name = target_date.strftime('%A').upper()
    working_days = [work_schedule.day_of_week.name for work_schedule in schedule.work_dates]

    if target_day_name not in working_days:
        return False, None

    return True, schedule


def format_work_schedule(work_schedule):
    if not work_schedule:
        return None

    return {
        "title": work_schedule.title,
        "description": work_schedule.description,
        "startTime": work_schedule.start_time.strftime("%H:%M:%S") if work_schedule.start_time else None,
        "endTime": work_schedule.end_time.strftime("%H:%M:%S") if work_schedule.end_time else None,
        "workDate": [wd.day_of_week.name.capitalize() for wd in work_schedule.work_dates],
    }
