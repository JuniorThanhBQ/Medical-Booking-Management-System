import { create } from "zustand";
import { EXAM_STATUS } from "@/configs/const";
import { mockMedicalRecords } from "@/data/mocks/patients";
import { getExamStore, setExamStore } from "@/repository/local-storage-repository";
import { getUserToken } from "@/utils/auth-helpers";
import {
  createMedicalRecordForAppointment,
  getAppointmentDetail,
  getAppointmentPatientProfile,
  getMedicalRecordDetail,
  updateMedicalRecord,
} from "../services/examination-api.js";
import {
  EMPTY_FORM,
  toExamFormData,
  toMedicalRecordPayload,
  toPatient,
  toRecordHistory,
} from "@utils/examination-utils.js";

function loadPersistedState() {
  const parsed = getExamStore();
  return parsed ? { records: parsed.records || {} } : null;
}

function persistState(state) {
  const draftRecords = Object.fromEntries(
    Object.entries(state.records).filter(
      ([_, r]) => r.status === EXAM_STATUS.DRAFT
    )
  );
  setExamStore({ records: draftRecords });
}

const persisted = loadPersistedState();

const initialState = {
  records: persisted?.records ?? {},
  notifications: [],
  examination: {
    formData: { ...EMPTY_FORM },
    isCompleted: false,
    loading: true,
    error: "",
    actionError: "",
    appointment: null,
    patient: null,
    history: [],
  },
};

function normalizeExamStatus(status) {
  if (status === "DONE" || status === EXAM_STATUS.COMPLETED) {
    return EXAM_STATUS.COMPLETED;
  }
  return EXAM_STATUS.DRAFT;
}

function patchExamination(set, patch) {
  set((state) => ({
    examination: {
      ...state.examination,
      ...patch,
    },
  }));
}

export const useExamStore = create((set, get) => ({
  ...initialState,

  setExamFormData: (formData) => {
    patchExamination(set, { formData });
  },

  resetExaminationState: () => {
    patchExamination(set, { ...initialState.examination });
  },

  refreshMedicalRecordData: async (appointmentId, currentAppointment = null) => {
    const token = getUserToken();
    if (!token) throw new Error("missing-token");

    const appointmentDetail =
      currentAppointment || (await getAppointmentDetail(token, appointmentId));
    patchExamination(set, { appointment: appointmentDetail });

    if (!appointmentDetail?.medicalRecordId) {
      patchExamination(set, {
        history: [],
        formData: { ...EMPTY_FORM },
        isCompleted: false,
      });
      return null;
    }

    const record = await getMedicalRecordDetail(token, appointmentDetail.medicalRecordId);
    patchExamination(set, {
      formData: toExamFormData(record),
      history: toRecordHistory(record),
      isCompleted: record?.status === "DONE",
    });

    return { appointmentDetail, record };
  },

  loadExamination: async (appointmentId) => {
    const token = getUserToken();
    if (!token) {
      patchExamination(set, {
        loading: false,
        error: "Không tìm thấy phiên đăng nhập. Vui lòng đăng nhập lại.",
        appointment: null,
      });
      return;
    }

    patchExamination(set, { loading: true, error: "", actionError: "" });

    try {
      const [appointmentDetail, profile] = await Promise.all([
        getAppointmentDetail(token, appointmentId),
        getAppointmentPatientProfile(token, appointmentId),
      ]);

      patchExamination(set, {
        appointment: appointmentDetail,
        patient: toPatient(appointmentDetail, profile, appointmentId),
      });

      if (appointmentDetail?.medicalRecordId) {
        await get().refreshMedicalRecordData(appointmentId, appointmentDetail);
      } else {
        const local = get().getRecord(appointmentId);
        patchExamination(set, {
          formData: toExamFormData(local),
          isCompleted: false,
          history: [],
        });
      }
    } catch {
      patchExamination(set, {
        appointment: null,
        error: "Không thể tải dữ liệu khám bệnh. Vui lòng thử lại.",
      });
    } finally {
      patchExamination(set, { loading: false });
    }
  },

  saveDraftToServer: async (appointmentId, doctorName) => {
    await saveOrCompleteExam({ appointmentId, doctorName, mode: "draft", set, get });
  },

  completeExamToServer: async (appointmentId, doctorName) => {
    await saveOrCompleteExam({ appointmentId, doctorName, mode: "complete", set, get });
  },

  saveRecord: (appointmentId, data) => {
    set((state) => {
      const existing = state.records[appointmentId] || {};
      return {
        ...state,
        records: {
          ...state.records,
          [appointmentId]: {
            ...existing,
            ...data,
            id: existing.id || `rec_${Date.now()}`,
            appointmentId,
            status: normalizeExamStatus(data.status),
            updatedAt: new Date().toISOString(),
            createdAt: existing.createdAt || new Date().toISOString(),
          },
        },
      };
    });
    persistState(get());
  },

  getRecord: (appointmentId) => {
    return get().records[appointmentId] || null;
  },

  getPatientHistory: (patientId) => {
    const savedRecords = Object.values(get().records).filter(
      (r) => r.patientId === patientId && r.status === EXAM_STATUS.COMPLETED
    );
    const mockRecords = mockMedicalRecords.filter(
      (r) => r.patientId === patientId
    );
    return [...mockRecords, ...savedRecords].sort(
      (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
    );
  },

  completeExam: (appointmentId, data) => {
    set((state) => {
      const existing = state.records[appointmentId] || {};
      const record = {
        ...existing,
        ...data,
        id: existing.id || `rec_${Date.now()}`,
        appointmentId,
        status: EXAM_STATUS.COMPLETED,
        updatedAt: new Date().toISOString(),
        createdAt: existing.createdAt || new Date().toISOString(),
      };
      const notification = {
        id: `notif-${Date.now()}`,
        patientId: data.patientId,
        appointmentId,
        message: `Kết quả khám bệnh của bạn đã sẵn sàng.`,
        createdAt: new Date().toISOString(),
        read: false,
      };

      return {
        records: { ...state.records, [appointmentId]: record },
        notifications: [notification, ...state.notifications],
      };
    });
    persistState(get());
  },

  getNotifications: (patientId) => {
    return get().notifications.filter((n) => n.patientId === patientId);
  },
}));

async function saveOrCompleteExam({ appointmentId, doctorName, mode, set, get }) {
  const token = getUserToken();
  if (!token) {
    patchExamination(set, { actionError: "Không tìm thấy phiên đăng nhập. Vui lòng đăng nhập lại." });
    return;
  }

  const { examination } = get();
  if (!examination.appointment) return;

  const isComplete = mode === "complete";
  const payload = toMedicalRecordPayload(
    examination.formData,
    isComplete ? "DONE" : "FOLLOW_UP"
  );
  patchExamination(set, { actionError: "" });

  try {
    if (examination.appointment?.medicalRecordId) {
      await updateMedicalRecord(token, examination.appointment.medicalRecordId, payload);
    } else {
      await createMedicalRecordForAppointment(token, Number(appointmentId), payload);
    }

    const refreshed = await get().refreshMedicalRecordData(appointmentId, examination.appointment);
    const refreshedRecord = refreshed?.record || null;
    const recordPayload = {
      ...payload,
      ...refreshedRecord,
      patientId: examination.appointment?.patientId || examination.patient?.id,
      doctorName,
    };

    if (isComplete) {
      get().completeExam(appointmentId, recordPayload);
      patchExamination(set, { isCompleted: true });
      return;
    }

    get().saveRecord(appointmentId, recordPayload);
  } catch {
    patchExamination(set, {
      actionError: isComplete
        ? "Không thể hoàn tất phiếu khám. Vui lòng thử lại."
        : "Không thể lưu nháp lúc này. Vui lòng thử lại.",
    });
  }
}
