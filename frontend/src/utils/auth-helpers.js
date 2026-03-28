import { getToken, getUser } from "@/repository/local-storage-repository";

export const isAuthenticated = () => Boolean(getToken());

export const getStoredUser = () => getUser();

export const getStoredUserRole = () => getStoredUser()?.role ?? null;

export const getUserToken = () => getToken();
