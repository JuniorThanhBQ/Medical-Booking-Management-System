import { useState } from "react";

export const useAppointmentCard = (appointment, onUpdateStatus) => {
  const [showActions, setShowActions] = useState(false);
  const [newStatus, setNewStatus] = useState(appointment.status);
  const [newNote, setNewNote] = useState(appointment.note || "");

  const handleUpdate = () => {
    onUpdateStatus(appointment.id, newStatus, newNote);
    setShowActions(false);
  };

  const toggleActions = () => {
    setShowActions(!showActions);
  };

  return {
    showActions,
    newStatus,
    setNewStatus,
    newNote,
    setNewNote,
    handleUpdate,
    toggleActions,
  };
};
