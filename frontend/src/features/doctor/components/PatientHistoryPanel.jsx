import { useState } from "react";

export default function PatientHistoryPanel({ patient, notes, history }) {
  const [expandedId, setExpandedId] = useState(null);

  function toggleRecord(id) {
    setExpandedId((prev) => (prev === id ? null : id));
  }

  return (
    <aside className="exam__sidebar">
      <div className="exam__patient-info">
        <h2 className="exam__patient-name">{patient?.name || "—"}</h2>
        {patient && (
          <p className="exam__patient-demo">
            {patient.age} tuổi · {patient.gender} · {patient.phone}
          </p>
        )}
      </div>

      {notes && (
        <div className="exam__patient-notes">
          <h3 className="exam__patient-notes-title">Ghi chú bệnh nhân</h3>
          <p className="exam__patient-notes-text">{notes}</p>
        </div>
      )}

      <div className="exam__history">
        <h3 className="exam__history-title">Lịch sử khám</h3>
        {history.length === 0 && (
          <p className="exam__history-empty">Chưa có lịch sử khám.</p>
        )}
        <ul className="exam__history-list">
          {history.map((record) => (
            <li key={record.id} className="exam__history-item">
              <button
                type="button"
                className="exam__history-toggle"
                onClick={() => toggleRecord(record.id)}
                aria-expanded={expandedId === record.id}
              >
                <span className="exam__history-date">
                  {new Date(record.createdAt).toLocaleDateString("vi-VN")}
                </span>
                <span className="exam__history-diag">{record.diagnosis}</span>
                <span className="exam__history-arrow">
                  {expandedId === record.id ? "▲" : "▼"}
                </span>
              </button>
              {expandedId === record.id && (
                <div className="exam__history-detail">
                  <p><strong>Ghi chú:</strong> {record.notes || "—"}</p>
                  <p><strong>Đơn thuốc:</strong> {record.prescriptionText || "—"}</p>
                  {record.treatmentOrders && (
                    <p><strong>Chỉ định:</strong> {record.treatmentOrders}</p>
                  )}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}
