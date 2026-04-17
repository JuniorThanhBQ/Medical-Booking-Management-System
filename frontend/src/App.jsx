import "@/assets/css/App.css";

import AppRoute from "@routes/AppRoute.jsx";
import { Toaster } from "sonner";

function App() {
  return (
    <>
      <AppRoute />
      <Toaster
        position="top-right"
        expand={false}
        richColors
        visibleToasts={2}
        duration={2000}
        pauseWhenPageIsHidden
        closeButton
        theme="light"
      />
    </>
  );
}

export default App;
