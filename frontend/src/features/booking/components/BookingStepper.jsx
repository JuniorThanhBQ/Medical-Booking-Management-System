import { STEPS } from "@utils/booking-utils";

export function BookingStepper({ stepIndex, onGoToStep }) {
  return (
    <div className="booking__stepper">
      {STEPS.map((s, idx) => {
        const isActive = idx === stepIndex;
        const isDone = idx < stepIndex;
        return (
          <button
            key={s.id}
            type="button"
            className={`booking__step${
              isActive ? " booking__step--active" : ""
            }${isDone ? " booking__step--done" : ""}`}
            onClick={() => onGoToStep(idx)}
          >
            <span className="booking__step-label">{s.label}</span>
          </button>
        );
      })}
    </div>
  );
}
