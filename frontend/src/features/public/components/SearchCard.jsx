import { useState } from "react";

const SearchCard = ({ onSearch, searching }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (onSearch) {
      onSearch({ query: query.trim() });
    }
  };

  return (
    <form className="search-card" onSubmit={handleSubmit}>
      {/* Header */}
      <div className="search-card__header">
        <h3 className="search-card__title">Đặt lịch khám ngay</h3>
        <p className="search-card__desc">
          Nhập tên bác sĩ hoặc chuyên khoa để tìm phòng khám phù hợp với bạn.
        </p>
      </div>

      {/* Search input */}
      <div className="search-card__field-wrap">
        <div className="search-card__input-group">
          <svg className="search-card__icon" viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M11 5a6 6 0 1 1-4.243 1.757A5.984 5.984 0 0 1 11 5m0-2a8 8 0 1 0 5.657 2.343A7.999 7.999 0 0 0 11 3Z"
              fill="currentColor"
            />
            <path
              d="m20.707 21.707-4.2-4.2a1 1 0 0 0-1.414-1.414l-1.586 1.586 4.2 4.2a1 1 0 0 0 1.414-1.414Z"
              fill="currentColor"
            />
          </svg>

          <input
            id="search-query"
            name="query"
            className="search-card__input"
            type="text"
            placeholder="Ví dụ: Tim mạch, Da liễu, Nguyễn Văn A..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoComplete="off"
          />

          {query && (
            <button
              type="button"
              className="search-card__clear"
              onClick={() => setQuery("")}
              aria-label="Xóa tìm kiếm"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M18 6 6 18M6 6l12 12"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          )}
        </div>

        <button className="search-card__btn" type="submit" disabled={searching}>
          {searching ? (
            <>
              <span className="search-card__spinner" aria-hidden="true" />
              Đang tìm...
            </>
          ) : (
            <>
              Tìm kiếm
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M5 12h14M13 6l6 6-6 6"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </>
          )}
        </button>
      </div>

    </form>
  );
};

export default SearchCard;
