const SearchField = ({ label, placeholder, icon, name, value, onChange }) => {
  return (
    <div className="dashboard__field">
      <label className="dashboard__label" htmlFor={name}>
        {label}
      </label>

      <div className="dashboard__input-wrap">
        <svg viewBox="0 0 24 24">
          {icon}
        </svg>

        <input
          id={name}
          name={name}
          className="dashboard__input"
          type="text"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
        />
      </div>
    </div>
  );
};

export default SearchField;