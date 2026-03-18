export function BookingStepNav({
  stepIndex,
  stepsLength,
  canGoNext,
  onBack,
  onNext,
}) {
  return (
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
  );
}
