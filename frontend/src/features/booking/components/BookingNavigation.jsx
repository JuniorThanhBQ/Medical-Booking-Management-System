import { STEPS } from "@/utils/booking-utils.js";

export function BookingNavigation({
  stepIndex,
  stepsLength = STEPS.length,
  canGoNext,
  onBack,
  onNext,
  onGoToStep,
}) {
  return (
    <div className="booking__controls">
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

      <div className="booking__nav">
        <button
          type="button"
          className="booking__secondary"
          onClick={onBack}
          disabled={stepIndex === 0}
        >
          Back
        </button>

        <button
          type="button"
          className="booking__primary"
          onClick={onNext}
          disabled={stepIndex >= stepsLength - 1 || !canGoNext}
        >
          Next
        </button>
      </div>
    </div>
  );
}