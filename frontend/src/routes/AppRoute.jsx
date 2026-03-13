import { Routes, Route } from "react-router-dom";
import LandingPage from "../features/users/pages/LandingPage.jsx";
import AuthPage from "../features/auth/pages/sigin/AuthPage.jsx";
import Dashboard from "../features/users/pages/Dashboard.jsx";

export default function AppRoute() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}
