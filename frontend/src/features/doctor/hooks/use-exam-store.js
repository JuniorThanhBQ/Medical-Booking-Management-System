import { create } from "zustand";
import { EXAM_STATUS, APPOINTMENT_STATUS } from "@/configs/const";
import { mockMedicalRecords } from "@/data/mocks/patients";
import { getExamStore, setExamStore } from "@/repository/local-storage-repository";

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
};

export const useExamStore = create((set, get) => ({
  ...initialState,

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
            status: data.status || EXAM_STATUS.DRAFT,
            updatedAt: new Date().toISOString(),
            createdAt: existing.createdAt || new Date().toISOString(),
          },
        },
      };
    });
    persistState(get());
  },

  getRecord: (appointmentId) => {
    const localRecord = get().records[appointmentId] || null;
    return localRecord;
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
      console.log("completed record: ", record)
      const notification = {
        id: `notif-${Date.now()}`,
        patientId: data.patientId,
        appointmentId,
        message: `Kết quả khám bệnh của bạn đã sẵn sàng.`,
        createdAt: new Date().toISOString(),
        read: false,
      };
      console.log("notification: ", notification)

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
