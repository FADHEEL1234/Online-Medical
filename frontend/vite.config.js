import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // development proxy: forward calls starting with /api to Django
    // backend running on localhost:8000. this removes CORS headaches and
    // prevents the network error message as long as the backend process is
    // actually running.
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
