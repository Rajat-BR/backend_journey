// -----------------------------------------------------------------
// MOCK DATA
// -----------------------------------------------------------------
// This file holds fake data so the frontend has something to show
// before your FastAPI backend exists. Once your backend is ready,
// this file is no longer needed - api.js will fetch real data instead.

export const mockUser = {
  id: 1,
  username: "demo_user",
  email: "demo@example.com",
};

export const mockSessions = [
  {
    id: 1,
    subject: "Math",
    topic: "Linear Algebra",
    duration: 45,
    notes: "Reviewed matrix multiplication",
  },
  {
    id: 2,
    subject: "Computer Science",
    topic: "FastAPI Basics",
    duration: 60,
    notes: "Learned about path parameters",
  },
  {
    id: 3,
    subject: "English",
    topic: "Essay Writing",
    duration: 30,
    notes: "Practiced thesis statements",
  },
];
