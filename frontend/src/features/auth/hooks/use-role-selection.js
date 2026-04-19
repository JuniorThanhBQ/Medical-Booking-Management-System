import { useState } from "react";

export function useRoleSelection() {
  const [role, setRole] = useState(null);

  const selectRole = (roleId) => {
    setRole(roleId);
  };

  const resetRole = () => {
    setRole(null);
  };

  return {
    role,
    setRole: selectRole,
    resetRole,
  };
}
