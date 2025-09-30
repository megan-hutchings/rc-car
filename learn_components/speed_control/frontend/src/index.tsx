import React, { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import SpeedControl from "./speed_control_component"
import ErrorBoundary from "./ErrorBoundry"  // Make sure the filename matches (typo?)

const rootElement = document.getElementById("root")

if (!rootElement) {
  throw new Error("Root element not found")
}

const root = createRoot(rootElement)

root.render(
  <StrictMode>
    <ErrorBoundary>
      <SpeedControl />
    </ErrorBoundary>
  </StrictMode>
)

// import React from "react"
// import ReactDOM from "react-dom/client"
// import { SpeedControl } from "./speed_control_component"  // note: named import

// const root = document.getElementById("root")
// if (!root) throw new Error("Root element not found")

// const mockProps = {
//   args: { name: "Dev User" },
//   disabled: false,
//   theme: undefined,
//   width: 400,
// }

// ReactDOM.createRoot(root).render(
//   <React.StrictMode>
//     <SpeedControl {...mockProps} />
//   </React.StrictMode>
// )

// import React from "react";
// import ReactDOM from "react-dom/client";

// function App() {
//   return <h1>Hello React!</h1>;
// }

// const rootElement = document.getElementById("root");
// if (rootElement) {
//   const root = ReactDOM.createRoot(rootElement);
//   root.render(<App />);
// }
