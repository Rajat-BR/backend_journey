import { useState } from "react";
import { registerUser } from "../api/api";

// -------------------------------------------------------------------
// Register Page: username, email, password -> Register button
// -------------------------------------------------------------------
function RegisterPage({ goToLogin }) {
  // One useState per input field - simple and explicit for beginners
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault(); // prevent the browser's default page reload on submit

    // FastAPI Endpoint:
    // POST /register
    // (registerUser() lives in src/api/api.js - it's mocked for now)
    const result = await registerUser(username, email, password);

    if (result.success) {
      setMessage("Registered successfully! Redirecting to login...");
      goToLogin();
    }
  };

  return (
    <div className="page">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Register</button>
      </form>

      {message && <p>{message}</p>}

      <p>
        Already have an account?{" "}
        <button onClick={goToLogin} className="link-button">
          Log in
        </button>
      </p>
    </div>
  );
}

export default RegisterPage;
