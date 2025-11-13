import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

console.log('Main.tsx loaded');
console.log('Environment:', import.meta.env);

const rootElement = document.getElementById("root");
if (!rootElement) {
  console.error('Root element not found!');
  document.body.innerHTML = '<div style="padding: 20px; font-family: sans-serif;"><h1>Error: Root element not found</h1></div>';
} else {
  try {
    createRoot(rootElement).render(<App />);
    console.log('App rendered successfully');
  } catch (error) {
    console.error('Error rendering app:', error);
    document.body.innerHTML = `<div style="padding: 20px; font-family: sans-serif;"><h1>Error loading app</h1><pre>${error}</pre></div>`;
  }
}
