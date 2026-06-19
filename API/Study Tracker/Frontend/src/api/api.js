// ===================================================================
// API FILE
// ===================================================================
// This is the ONLY file that talks to the backend. Pages never call
// fetch() themselves - they call the functions below instead.
//
// RIGHT NOW: every function returns mock/fake data so the app works
// without a backend.
//
// LATER: once your FastAPI server is running, delete the mock line
// in each function and uncomment the fetch() call above it.
// ===================================================================

import { mockUser, mockSessions } from "../data/mockData";

// Update this if your FastAPI server runs somewhere else.
const BASE_URL = "http://127.0.0.1:8000";

// FastAPI Endpoint:
// POST /register
export async function registerUser(username, email, password) {
  // const response = await fetch(`${BASE_URL}/register`, {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ username, email, password }),
  // });
  // return response.json();

  console.log("[mock] registerUser:", { username, email, password });
  return Promise.resolve({ success: true, user: { username, email } });
}

// FastAPI Endpoint:
// POST /login
export async function loginUser(email, password) {
  // const response = await fetch(`${BASE_URL}/login`, {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ email, password }),
  // });
  // return response.json(); // will likely include a token once you add auth

  console.log("[mock] loginUser:", { email, password });
  return Promise.resolve({ success: true, user: mockUser });
}

// FastAPI Endpoint:
// GET /me
// (Not called anywhere yet - useful later once you add real login
// sessions/tokens and want to check "who is currently logged in".)
export async function getCurrentUser() {
  const response = await fetch(`${BASE_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();

  return Promise.resolve(mockUser);
}

// FastAPI Endpoint:
// GET /sessions
export async function getSessions() {
  const response = await fetch(`${BASE_URL}/sessions`);
  return response.json();

  return Promise.resolve(mockSessions);
}

// FastAPI Endpoint:
// POST /sessions
export async function addSession(sessionData) {
  const response = await fetch(`${BASE_URL}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(sessionData),
  });
  return response.json();

  console.log("[mock] addSession:", sessionData);
  return Promise.resolve({ id: Date.now(), ...sessionData });
}

// FastAPI Endpoint:
// PATCH /sessions/{id}
export async function updateSession(id, updatedFields) {
  const response = await fetch(`${BASE_URL}/sessions/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updatedFields),
  });
  return response.json();

  console.log("[mock] updateSession:", id, updatedFields);
  return Promise.resolve({ id, ...updatedFields });
}

// FastAPI Endpoint:
// DELETE /sessions/{id}
export async function deleteSession(id) {
  const response = await fetch(`${BASE_URL}/sessions/${id}`, {
    method: "DELETE",
  });
  return response.json();

  console.log("[mock] deleteSession:", id);
  return Promise.resolve({ success: true });
}
