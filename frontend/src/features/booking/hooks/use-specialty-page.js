import { getSpecialtyDetail } from "@features/shared/services/public-api-service";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";

export const useSpecialtyPage = () => {
  const { specialtyId } = useParams();
  const { accessToken } = useAuth();
  const loggedIn = Boolean(accessToken);
  const [specialty, setSpecialty] = useState(null);
  const [loading, setLoading] = useState(!!specialtyId);
  const [error, setError] = useState(
    !specialtyId ? "Không tìm thấy chuyên khoa." : null,
  );

  useEffect(() => {
    if (!specialtyId) {
      return;
    }

    let cancelled = false;
    const fetchSpecialty = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getSpecialtyDetail(specialtyId);
        if (!cancelled) setSpecialty(data);
      } catch {
        if (!cancelled)
          setError("Không thể tải thông tin chuyên khoa. Vui lòng thử lại.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchSpecialty();
    return () => {
      cancelled = true;
    };
  }, [specialtyId]);

  return {
    loggedIn,
    specialty,
    loading,
    error,
  };
};
