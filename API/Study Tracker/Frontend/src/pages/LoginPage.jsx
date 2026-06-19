import { useState } from "react";
import { loginUser } from "../api/api";

// -------------------------------------------------------------------
// Login Page: email, password -> Login button
// -------------------------------------------------------------------
function LoginPage({ onLoginSuccess, goToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // FastAPI Endpoint:
    // POST /login
    // (loginUser() lives in src/api/api.js - it's mocked for now)
    const result = await loginUser(email, password);

    if (result.success) {
      onLoginSuccess(result.user);
    } else {
      setError("Login failed. Please check your credentials.");
    }
  };

  return (
    <div className="page">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
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

        <button type="submit">Login</button>
      </form>

      {error && <p className="error">{error}</p>}

      <p>
        Don't have an account?{" "}
        <button onClick={goToRegister} className="link-button">
          Register
        </button>
      </p>
    </div>
  );
}

export default LoginPage;
