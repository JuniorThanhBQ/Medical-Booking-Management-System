import { useCallback, useState } from "react";
import { getDoctors } from "@/services/public-api-service";
import { normalizeQuery } from "@/utils/utils";

export function useDashboardSearch(specialties) {
  const [searchResults, setSearchResults] = useState(null);
  const [lastSearchParams, setLastSearchParams] = useState(null);
  const [searchError, setSearchError] = useState(null);
  const [searching, setSearching] = useState(false);

  const handleSearch = useCallback(
    async ({ query }) => {
      const normalizedQuery = normalizeQuery(query || "");

      setLastSearchParams({ query });
      setSearchError(null);
      setSearching(true);

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
    },
    [specialties],
  );

  return { searchResults, lastSearchParams, searchError, searching, handleSearch };
}
