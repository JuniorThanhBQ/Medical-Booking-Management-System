import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";

import { useExamStore } from "./use-exam-store";

export const useExaminationPage = () => {
  const { appointmentId } = useParams();
  const navigate = useNavigate();
  const { user, api } = useAuth();
  const examination = useExamStore((s) => s.examination);
  const setExamFormData = useExamStore((s) => s.setExamFormData);
  const loadExamination = useExamStore((s) => s.loadExamination);
  const resetExaminationState = useExamStore((s) => s.resetExaminationState);
  const saveDraftToServer = useExamStore((s) => s.saveDraftToServer);
  const completeExamToServer = useExamStore((s) => s.completeExamToServer);

  const doctorName = user?.name || "Bác sĩ";

  useEffect(() => {
    if (!api || !appointmentId || appointmentId === "undefined") return;

    loadExamination(api, appointmentId);

    return () => {
      resetExaminationState();
    };
  }, [appointmentId, api, loadExamination, resetExaminationState]);

  function handleSaveDraft() {
    if (api) {
      saveDraftToServer(api, appointmentId, doctorName);
    }
  }

  function handleComplete() {
    if (api) {
      completeExamToServer(api, appointmentId, doctorName);
    }
  }

  const hasNotFound =
    !examination.loading && !examination.error && !examination.appointment;

  return {
    navigate,
    examination,
    setExamFormData,
    handleSaveDraft,
    handleComplete,
    hasNotFound,
  };
};
