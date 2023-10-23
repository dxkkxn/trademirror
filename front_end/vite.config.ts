import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 4500,
  },
  // resolve:{alias:{path:"path-browserify",}},
  // base: "http://apitestjppm.com/frontend",
  plugins: [react()],
});
