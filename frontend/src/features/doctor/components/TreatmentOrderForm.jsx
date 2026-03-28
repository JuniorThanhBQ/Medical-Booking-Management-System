import { useState } from "react";


export default function TreatmentOrderForm({ value, onChange, disabled }) {
  const [expanded, setExpanded] = useState(Boolean(value));

  return (
    <div className="exam__treatment">
      <button
        type="button"
        className="exam__treatment-toggle"
        onClick={() => setExpanded((prev) => !prev)}
        aria-expanded={expanded}
      >
        Chỉ định xét nghiệm / điều trị
        <span>{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && (
        <textarea
          className="exam__textarea"
          placeholder="VD: Xét nghiệm máu, X-quang ngực..."
          rows={3}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
        />
      )}
    </div>
  );
}
