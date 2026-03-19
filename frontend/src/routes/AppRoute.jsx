import { Routes, Route } from "react-router-dom";
import LandingPage from "../features/users/pages/LandingPage.jsx";
import AuthPage from "../features/auth/pages/sigin/AuthPage.jsx";
import Dashboard from "../features/users/pages/Dashboard.jsx";
import TodayPatientsPage from "../features/doctor/pages/TodayPatientsPage.jsx";
import SchedulePage from "../features/doctor/pages/SchedulePage.jsx";
import ExaminationPage from "../features/doctor/pages/ExaminationPage.jsx";
import RoleRoute from "./RoleRoute.jsx";
import SpecialtyPage from "../features/users/pages/SpecialtyPage.jsx";
import BookAppointmentPage from "../features/users/pages/BookAppointmentPage.jsx";
import ProfilePage from "../features/users/pages/ProfilePage.jsx";
import ActivityPage from "../features/users/pages/ActivityPage.jsx";
import AppointmentRecordPage from "../features/users/pages/AppointmentRecordPage.jsx";

export default function AppRoute() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/activity" element={<ActivityPage />} />

      <Route element={<RoleRoute allowedRoles={["Patient", "Admin"]} />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/specialties/:specialtyId" element={<SpecialtyPage />} />
        <Route
          path="/specialties/:specialtyId/book"
          element={<BookAppointmentPage />}
        />
        <Route path="/appointments/:appointmentId/record" element={<AppointmentRecordPage />} />
      </Route>

      <Route element={<RoleRoute allowedRoles={["Doctor"]} />}>
        <Route path="/doctor/today" element={<TodayPatientsPage />} />
        <Route path="/doctor/exam/:appointmentId" element={<ExaminationPage />} />
        <Route path="/schedule" element={<SchedulePage />} />
      </Route>
    </Routes>
  );
}
