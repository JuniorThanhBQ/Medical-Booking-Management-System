import AuthPage from "@features/auth/pages/AuthPage.jsx";
import EmailVerificationPage from "@features/auth/pages/EmailVerificationPage.jsx";
import BookAppointmentPage from "@features/booking/pages/BookAppointmentPage";
import SpecialtyPage from "@features/booking/pages/SpecialtyPage";
import DoctorRegistration from "@features/doctor/pages/DoctorRegistration.jsx";
import ExaminationPage from "@features/doctor/pages/ExaminationPage.jsx";
import SchedulePage from "@features/doctor/pages/SchedulePage.jsx";
import TodayPatientsPage from "@features/doctor/pages/TodayPatientsPage.jsx";
import NotificationDetailPage from "@features/notification/pages/NotificationDetailPage.jsx";
import NotificationPage from "@features/notification/pages/NotificationPage.jsx";
import ReceptionistAppointmentDetailPage from "@features/receptionist/pages/AppointmentDetailPage.jsx";
import AppointmentsPage from "@features/receptionist/pages/AppointmentsPage.jsx";
import DoctorDetail from "@features/users/components/DoctorDetail.jsx";
import ActivityPage from "@features/users/pages/ActivityPage.jsx";
import AppointmentDetailPage from "@features/users/pages/AppointmentDetailPage.jsx";
import AppointmentRecordPage from "@features/users/pages/AppointmentRecordPage.jsx";
import Dashboard from "@features/users/pages/Dashboard.jsx";
import LandingPage from "@features/users/pages/LandingPage.jsx";
import PatientProfilePage from "@features/users/pages/PatientProfilePage.jsx";
import ProfilePage from "@features/users/pages/ProfilePage.jsx";
import { Route, Routes } from "react-router-dom";

import PrivateRoute from "./PrivateRoute.jsx";
import RoleRoute from "./RoleRoute.jsx";

export default function AppRoute() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/email-verification" element={<EmailVerificationPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/specialties/:specialtyId" element={<SpecialtyPage />} />
      <Route path="/doctors/:id" element={<DoctorDetail />} />
      <Route path="/doctor-registration" element={<DoctorRegistration />} />

      <Route element={<PrivateRoute />}>
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/activity" element={<ActivityPage />} />
        <Route path="/notifications" element={<NotificationPage />} />
        <Route
          path="/notifications/:notificationId"
          element={<NotificationDetailPage />}
        />
        <Route
          path="/appointments/:appointmentId"
          element={<AppointmentDetailPage />}
        />

        <Route
          element={
            <RoleRoute allowedRoles={["RECEPTIONIST", "PATIENT", "ADMIN"]} />
          }
        >
          <Route
            path="/specialties/:specialtyId/book"
            element={<BookAppointmentPage />}
          />
          <Route
            path="/appointments/:appointmentId/record"
            element={<AppointmentRecordPage />}
          />
        </Route>

        <Route element={<RoleRoute allowedRoles={["DOCTOR", "ADMIN"]} />}>
          <Route path="/schedule" element={<SchedulePage />} />
          <Route path="/doctor/today" element={<TodayPatientsPage />} />
          <Route
            path="/doctor/exam/:appointmentId"
            element={<ExaminationPage />}
          />
        </Route>

        <Route element={<RoleRoute allowedRoles={["RECEPTIONIST", "ADMIN"]} />}>
          <Route
            path="/receptionist/appointments"
            element={<AppointmentsPage />}
          />
          <Route
            path="/receptionist/appointments/:appointmentId"
            element={<ReceptionistAppointmentDetailPage />}
          />
          <Route
            path="/receptionist/appointments/:appointmentId/patient-profile"
            element={<PatientProfilePage />}
          />
        </Route>
      </Route>
    </Routes>
  );
}
