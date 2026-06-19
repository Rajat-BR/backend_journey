import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Basic Vite config - no extra plugins needed for this simple app
export default defineConfig({
  plugins: [react()],
});
