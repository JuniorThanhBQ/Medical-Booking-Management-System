import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import { defineConfig, globalIgnores } from "eslint/config";
import security from "eslint-plugin-security";

export default defineConfig([
  globalIgnores(["dist"]),
  security.configs.recommended,
  { 
    ignores: [
      "dist/**",
      "node_modules/**",
      "src/components/LoadingSpinner.jsx",
      "src/configs/const.js",
      "src/features/doctor/components/LeaveRequestsCard.jsx",
      "src/features/doctor/components/WeeklyScheduleCard.jsx",
      "src/features/doctor/hooks/use-exam-store.js",
      "src/features/doctor/hooks/use-schedule-store.js",
      "src/features/doctor/pages/ExaminationPage.jsx",
      "src/features/users/components/EditProfileForm.jsx",
      "src/features/users/components/ServicesSection.jsx",
      "src/features/users/components/SpecialtyCard.jsx",
      "src/features/users/hooks/use-dashboard-search.js",
      "src/features/users/pages/BookAppointmentPage.jsx",
      "src/features/users/pages/ProfilePage.jsx",
      "src/utils/utils.jsx",
    ],
    files: ["**/*.{js,jsx}"],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: "latest",
        ecmaFeatures: { jsx: true },
        sourceType: "module",
      },
    },
    rules: {
      "no-unused-vars": ["error", { varsIgnorePattern: "^[A-Z_]" }],
    },
  },
]);
