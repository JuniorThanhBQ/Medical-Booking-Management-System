import { APPOINTMENT_STATUS } from "@/configs/const";
export const mockTodayAppointments = [
  {
    id: 1,
    patientName: "Nguyễn Văn A",
    startTime: "08:00",
    endTime: "08:30",
    status: APPOINTMENT_STATUS.IN_PROGRESS,
    notes: "Khám tổng quát",
  },
  {
    id: 2,
    patientName: "Trần Thị B",
    startTime: "08:30",
    endTime: "09:00",
    status: APPOINTMENT_STATUS.SCHEDULED,
    notes: "Tái khám",
  },
  {
    id: 3,
    patientName: "Lê Văn C",
    startTime: "09:00",
    endTime: "09:30",
    status: APPOINTMENT_STATUS.SCHEDULED,
  },
  {
    id: 4,
    patientName: "Phạm Thị D",
    startTime: "10:00",
    endTime: "10:30",
    status: APPOINTMENT_STATUS.COMPLETED,
  },
];

export const mockLeaveRequests = [
  {
    id: 1,
    type: "vacation",
    fromDate: "2026-03-17",
    toDate: "2026-03-19",
    reason: "Nghỉ phép",
    status: "pending",
  },
  {
    id: 2,
    type: "sick",
    fromDate: "2026-03-20",
    toDate: "2026-03-20",
    reason: "Bị ốm",
    status: "approved",
  },
];  

export const mockAvailableAppointmentsInLeave = [
  {
    id: 1,
    patientName: "Nguyễn Văn A",
    startTime: "08:00",
    endTime: "08:30",
    status: APPOINTMENT_STATUS.IN_PROGRESS,
    notes: "Khám tổng quát",
  },
  {
    id: 2,
    patientName: "Trần Thị B",
    startTime: "08:30",
    endTime: "09:00",
    status: APPOINTMENT_STATUS.SCHEDULED,
    notes: "Tái khám",
  },
  {
    id: 3,
    patientName: "Lê Văn C",
    startTime: "09:00",
    endTime: "09:30",
    status: APPOINTMENT_STATUS.SCHEDULED,
  },
  {
    id: 4,
    patientName: "Phạm Thị D",
    startTime: "10:00",
    endTime: "10:30",
    status: APPOINTMENT_STATUS.COMPLETED,
  },
];