import { Routes, Route } from 'react-router-dom'
import LandingPage from '../features/users/pages/LandingPage.jsx'
import SignInChoicePage from '../features/auth/pages/sigin/SignInChoicePage.jsx'

export default function AppRoute() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/signin" element={<SignInChoicePage />} />
    </Routes>
  )
}

