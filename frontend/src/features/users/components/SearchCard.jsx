import { useState, useMemo } from "react";
import SearchField from "./SearchField";
import { CalendarIcon, ArrowRightFilledIcon } from "@/assets/icons";
import { toISODate } from "../utils/booking-utils";

const SearchCard = ({ onSearch }) => {
  const [query, setQuery] = useState("");
  const [date, setDate] = useState("");

  const { minDate, maxDate } = useMemo(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const max = new Date(today);
    max.setDate(max.getDate() + 14);

    return {
      minDate: toISODate(today),
      maxDate: toISODate(max),
    };
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();

    if (onSearch) {
      onSearch({
        query: query.trim(),
        date: date || null,
      });
    }
  };

  return (
    <form className="dashboard__search-card" onSubmit={handleSubmit}>
      <div className="dashboard__search-row">
        <SearchField
          name="query"
          label="Tìm kiếm"
          placeholder="Bác sĩ, chuyên khoa..."
          icon={
            <>
              <path
                d="M11 5a6 6 0 1 1-4.243 1.757A5.984 5.984 0 0 1 11 5m0-2a8 8 0 1 0 5.657 2.343A7.999 7.999 0 0 0 11 3Z"
                fill="currentColor"
              />
              <path
                d="m20.707 21.707-4.2-4.2a1 1 0 0 0-1.414-1.414l-1.586 1.586 4.2 4.2a1 1 0 0 0 1.414-1.414Z"
                fill="currentColor"
              />
            </>
          }
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />

        <div className="dashboard__field">
          <label className="dashboard__label">Ngày khám</label>

          <div className="dashboard__input-wrap">
            <CalendarIcon size={24} />

            <input
              name="date"
              className="dashboard__input"
              type="date"
              min={minDate}
              max={maxDate}
              value={date}
              onChange={(event) => setDate(event.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="dashboard__search-footer">
        <p className="dashboard__hint">
          Tìm bác sĩ theo chuyên khoa, tên và ngày khám phù hợp trong 15 ngày
          tới.
        </p>

        <button className="dashboard__search-btn" type="submit">
          Tìm kiếm
        </button>
      </div>
    </form>
  );
};

export default SearchCard;
