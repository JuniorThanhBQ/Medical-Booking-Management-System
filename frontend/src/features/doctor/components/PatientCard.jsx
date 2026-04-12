import { useNavigate } from "react-router-dom";
import { APPOINTMENT_STATUS, getStatusLabel } from "@/configs/const";
import { getAge } from "@/utils/utils.jsx";

export default function PatientCard({ appointment, patient, lastRecord }) {
  const navigate = useNavigate();

  const isInProgress = appointment.status === APPOINTMENT_STATUS.IN_PROGRESS;
  const statusClass = `today-patients__status--${appointment.status}`;

  function handleClick() {
    navigate(`/doctor/exam/${appointment.id}`);
  }

  return (
    <div
      className={`today-patients__card${isInProgress ? " today-patients__card--in-progress" : ""}`}
      role="button"
      tabIndex={0}
      onClick={handleClick}
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
