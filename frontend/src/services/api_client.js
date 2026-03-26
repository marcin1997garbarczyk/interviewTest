import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000
});

export const sendChatMessage = async (payload) => {
  const response = await apiClient.post("/api/chat", payload);
  return response.data;
};

export const fetchConversationHistory = async (sessionId) => {
  const response = await apiClient.get(`/api/chat/${sessionId}/history`);
  return response.data;
};

export const clearConversationHistory = async (sessionId) => {
  const response = await apiClient.delete(`/api/chat/${sessionId}/history`);
  return response.data;
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await apiClient.post("/api/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
};

export const approveAction = async (payload) => {
  const response = await apiClient.post("/api/approve_action", payload);
  return response.data;
};
