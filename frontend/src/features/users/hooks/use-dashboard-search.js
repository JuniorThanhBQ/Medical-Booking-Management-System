import { useCallback, useEffect, useRef, useState } from "react";
import { getDoctors } from "@/services/public-api-service";
import { validateAppointmentDate } from "../utils/dashboard-util";
import { normalizeQuery } from "@/utils/utils";

const SEARCH_DEBOUNCE_MS = 300;

export function useDashboardSearch(specialties) {
  const [searchResults, setSearchResults] = useState(null);
  const [lastSearchParams, setLastSearchParams] = useState(null);
  const [searchError, setSearchError] = useState(null);
  const [searching, setSearching] = useState(false);

  const debounceRef = useRef(null);

  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, []);

  const handleSearch = useCallback(
    ({ query, date }) => {
      if (debounceRef.current) clearTimeout(debounceRef.current);

      const normalizedQuery = normalizeQuery(query || "");

      const { isValid, error: dateError } = validateAppointmentDate(date);
      if (!isValid) {
        setSearchResults([]);
        setLastSearchParams({ query, date });
        setSearchError(dateError);
        return;
      }

      setLastSearchParams({ query, date });
      setSearchError(null);
      setSearching(true);

      debounceRef.current = setTimeout(async () => {
        try {
          const doctors = await getDoctors({ keywords: normalizedQuery });
          const specialtyIds = new Set(doctors.map((d) => d.specialtyId));
          const results = specialties.filter((s) => specialtyIds.has(s.id));
          setSearchResults(results);
        } catch {
          setSearchError("Không thể tìm kiếm. Vui lòng thử lại.");
          setSearchResults([]);
        } finally {
          setSearching(false);
        }
      }, SEARCH_DEBOUNCE_MS);
    },
    [specialties],
  );

  return { searchResults, lastSearchParams, searchError, searching, handleSearch };
}
