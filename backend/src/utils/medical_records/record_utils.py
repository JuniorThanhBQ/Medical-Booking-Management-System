def check_record_access_permission(current_user, record):
    role_name = current_user.role.name
    profile_id = current_user.profile.id if current_user.profile else None

    if role_name == "PATIENT" and record.patient_profile_id != profile_id:
        return False
    if role_name == "DOCTOR" and record.doctor_profile_id != profile_id:
        return False
    return True
