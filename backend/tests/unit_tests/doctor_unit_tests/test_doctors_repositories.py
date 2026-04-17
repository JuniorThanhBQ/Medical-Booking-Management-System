from datetime import datetime, time, timedelta

from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.doctors.models import (DayOfWeek, DoctorProfile,
                                        MedicalService, Specialty, WorkDate,
                                        WorkSchedule)
from src.modules.doctors.repositories import (commit_session, get_doctor_by_id,
                                              get_medical_service_by_id,
                                              get_or_create_work_schedule,
                                              get_paginated_doctors,
                                              get_paginated_medical_services,
                                              get_paginated_specialties,
                                              get_specialty_by_id,
                                              get_upcoming_appointments,
                                              is_conflict_appointment,
                                              update_work_dates)
from src.modules.users.models import User, UserRole
from tests.test_base import test_app, test_client, test_session

