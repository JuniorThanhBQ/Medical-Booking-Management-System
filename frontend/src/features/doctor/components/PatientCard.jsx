import "@css/doctor/patient-tab.css";

import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { getStatusLabel } from "@/configs/const";
import { getAge } from "@/utils/Utils.js";

export default function PatientCard({
  appointment,
  patient,
  lastRecord,
  canExamine,
}) {
  const navigate = useNavigate();
  const statusClass = `today-patients__status--${appointment.status}`;

  const handleCardClick = () => {
    if (!canExamine) {
      toast.error("Vui lòng đợi đến giờ hẹn để bắt đầu khám bệnh.");
      return;
    }
    toast.info("Bạn đang tiến hành khám bệnh nhân.");
    navigate(`/doctor/exam/${appointment.id}`);
  };

  return (
    <div
      className={"today-patients__card"}
      role="button"
      tabIndex={0}
      onClick={handleCardClick}
    >
      <div className="today-patients__card-main">
        <div className="today-patients__card-info">
          <h3 className="today-patients__card-name">
            {appointment.patientName}
          </h3>
          {patient && (
            <span className="today-patients__card-demo">
              {getAge(patient.dateOfBirth)} tuổi · {patient.gender}
            </span>
          )}
        </div>

        <span className="today-patients__card-time">
          {appointment.startTime} – {appointment.endTime}
        </span>
      </div>

      {lastRecord && (
        <p className="today-patients__card-history">
          Lần khám trước: {lastRecord.diagnosis}
        </p>
      )}

      <div className="today-patients__card-footer">
        <span className={`today-patients__status ${statusClass}`}>
          {getStatusLabel(appointment.status)}
        </span>
      </div>
    </div>
  );
}
