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
        visibleToasts={3}
        duration={2500}
        pauseWhenPageIsHidden
        closeButton
        offset="8px"
        theme="light"
      />
    </>
  );
}

export default App;
