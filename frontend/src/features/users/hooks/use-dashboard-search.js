import { useCallback, useState } from "react";
import { getDoctors, getTimeSlots } from "@/services/public-api-service";
import { validateAppointmentDate } from "../utils/dashboard-util";
import { normalizeQuery } from "@/utils/utils";

export function useDashboardSearch(specialties) {
  const [searchResults, setSearchResults] = useState(null);
  const [lastSearchParams, setLastSearchParams] = useState(null);
  const [searchError, setSearchError] = useState(null);
  const [searching, setSearching] = useState(false);

  const handleSearch = useCallback(
    async ({ query, date }) => {
      const normalizedQuery = normalizeQuery(query || "");

      if (date) {
        const { isValid, error: dateError } = validateAppointmentDate(date);
        if (!isValid) {
          setSearchResults([]);
          setLastSearchParams({ query, date });
          setSearchError(dateError);
          return;
        }
      }

      setLastSearchParams({ query, date });
      setSearchError(null);
      setSearching(true);

      try {
        const doctors = await getDoctors({ keywords: normalizedQuery });

        let filteredDoctors = doctors;
        if (date && doctors.length > 0) {
          const slotResults = await Promise.allSettled(
            doctors.map((d) => getTimeSlots(d.id, date)),
          );
          filteredDoctors = doctors.filter((_, i) => {
            const result = slotResults[i];
            if (result.status !== "fulfilled") return false;
            return result.value.some((s) => s.availableTimeSlots?.length > 0);
          });
        }

        const specialtyIds = new Set(filteredDoctors.map((d) => d.specialtyId));
        const results = specialties.filter((s) => specialtyIds.has(s.id));
        setSearchResults(results);
      } catch {
        setSearchError("Không thể tìm kiếm. Vui lòng thử lại.");
        setSearchResults([]);
      } finally {
        setSearching(false);
      }
    },
    [specialties],
  );

  return { searchResults, lastSearchParams, searchError, searching, handleSearch };
}
