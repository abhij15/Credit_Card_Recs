import React from "react";
import ReactDOM from "react-dom/client";

const App: React.FC = () => {
  return (
    <div>
      <h1>Credit Card Optimizer</h1>
      <p>Frontend scaffold is working.</p>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

