import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import security from "eslint-plugin-security";
import reactPlugin from "eslint-plugin-react";

export default [
  {
    ignores: ["dist", "node_modules"],
  },
  {
    files: ["src/**/*.{js,jsx}"],
    plugins: {
      "react": reactPlugin,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
      "security": security,
    },
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    settings: {
      react: {
        version: "detect",
      },
    },
    rules: {
      ...js.configs.recommended.rules,
      ...reactPlugin.configs.recommended.rules,
      ...reactPlugin.configs["jsx-runtime"].rules, 
      ...reactHooks.configs.recommended.rules,
      ...security.configs.recommended.rules,
      "no-unused-vars": "warn",
      "react-refresh/only-export-components": "off", 
      "security/detect-object-injection": "off",
      "react/prop-types": "off",
      "react-hooks/exhaustive-deps": "off",
      "no-empty": "off",
    },
  },
];