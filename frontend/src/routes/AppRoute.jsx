import { Routes, Route } from "react-router-dom";
import LandingPage from "../features/users/pages/LandingPage.jsx";
import AuthPage from "../features/auth/pages/sigin/AuthPage.jsx";
import Dashboard from "../features/users/pages/Dashboard.jsx";
import RoleRoute from "./RoleRoute.jsx";
import SpecialtyPage from "../features/users/pages/SpecialtyPage.jsx";
import BookAppointmentPage from "../features/users/pages/BookAppointmentPage.jsx";

export default function AppRoute() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/auth" element={<AuthPage />} />

      <Route element={<RoleRoute allowedRoles={["Patient", "Admin"]} />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/specialties/:specialtyId" element={<SpecialtyPage />} />
        <Route
          path="/specialties/:specialtyId/book"
          element={<BookAppointmentPage />}
        />
      </Route>
    </Routes>
  );
}
