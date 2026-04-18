export const BookingPanelHeader = ({ onNext, title, disabled = false }) => {
  return (
    <div className="booking__panel-header">
      <h2 className="booking__panel-title">{title}</h2>
      <button 
        className="booking__panel-next" 
        onClick={onNext}
        disabled={disabled}
      >
        <span>→</span>
      </button>
    </div>
  );
};