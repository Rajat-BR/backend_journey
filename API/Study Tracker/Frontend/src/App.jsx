import { useState } from "react";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import { getSessions, addSession, updateSession, deleteSession } from "./api/api";

// -------------------------------------------------------------------
// App.jsx is the ONLY place that holds global state:
//   - currentPage:  which page is visible ("login" | "register" | "dashboard")
//   - currentUser:  the logged-in user, or null if nobody is logged in
//   - sessions:     the list of study sessions
//
// Pages do not manage this data themselves. They receive it as props
// and call the functions below (e.g. handleAddSession) to change it.
// This keeps the data flow easy to follow: one direction, one source
// of truth, no Context API / Redux needed.
// -------------------------------------------------------------------
function App() {
  const [currentPage, setCurrentPage] = useState("login");
  const [currentUser, setCurrentUser] = useState(null);
  const [sessions, setSessions] = useState([]);

  // Called by LoginPage after a successful login
  const handleLoginSuccess = async (user) => {
    setCurrentUser(user);

    // FastAPI Endpoint:
    // GET /sessions
    const fetchedSessions = await getSessions();
    setSessions(fetchedSessions);

    setCurrentPage("dashboard");
  };

  // Called by DashboardPage when the user clicks "Logout"
  const handleLogout = () => {
    setCurrentUser(null);
    setSessions([]);
    setCurrentPage("login");
  };

  // Called by DashboardPage's form when adding a new session
  const handleAddSession = async (sessionData) => {
    // FastAPI Endpoint:
    // POST /sessions
    const savedSession = await addSession(sessionData);
    setSessions([...sessions, savedSession]);
  };

  // Called by DashboardPage's form when saving edits to a session
  const handleUpdateSession = async (id, updatedFields) => {
    // FastAPI Endpoint:
    // PATCH /sessions/{id}
    const updated = await updateSession(id, updatedFields);
    setSessions(
      sessions.map((session) =>
        session.id === id ? { ...session, ...updated } : session
      )
    );
  };

  // Called by DashboardPage when the user clicks "Delete" on a session
  const handleDeleteSession = async (id) => {
    // FastAPI Endpoint:
    // DELETE /sessions/{id}
    await deleteSession(id);
    setSessions(sessions.filter((session) => session.id !== id));
  };

  // Simple page switcher - no routing library needed for 3 pages
  return (
    <div className="app-container">
      {currentPage === "login" && (
        <LoginPage
          onLoginSuccess={handleLoginSuccess}
          goToRegister={() => setCurrentPage("register")}
        />
      )}

      {currentPage === "register" && (
        <RegisterPage goToLogin={() => setCurrentPage("login")} />
      )}

      {currentPage === "dashboard" && (
        <DashboardPage
          user={currentUser}
          sessions={sessions}
          onLogout={handleLogout}
          onAddSession={handleAddSession}
          onUpdateSession={handleUpdateSession}
          onDeleteSession={handleDeleteSession}
        />
      )}
    </div>
  );
}

export default App;
