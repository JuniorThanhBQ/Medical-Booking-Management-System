from src.modules.doctors.views import (RetrieveMyScheduleAPI,
                                       ScheduleRequestAPI, doctors_namespace)

doctors_namespace.add_resource(RetrieveMyScheduleAPI, '/my-schedule')
doctors_namespace.add_resource(ScheduleRequestAPI, '/schedule-requests')
