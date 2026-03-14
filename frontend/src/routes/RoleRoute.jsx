import { Navigate, Outlet } from "react-router-dom";

export default function RoleRoute({ allowedRoles }) {
  const user = localStorage.getItem("user");

  console.log("user Role ROute",user)


  if (!user) {
    return <Navigate to="/auth" replace />;
  }

  const role = JSON.parse(user).role;



  if (!allowedRoles.includes(role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
