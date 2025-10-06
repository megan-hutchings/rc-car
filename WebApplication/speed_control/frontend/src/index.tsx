import React, { StrictMode } from "react"
import { createRoot } from "react-dom/client"
//import SpeedControl from "./speed_control_component
import SpeedControlSimple from "./speed_control_simple"
import ErrorBoundary from "./ErrorBoundry"  // Make sure the filename matches (typo?)

const rootElement = document.getElementById("root")

if (!rootElement) {
  throw new Error("Root element not found")
}

const root = createRoot(rootElement)

root.render(
  <StrictMode>
    <ErrorBoundary>
      <SpeedControlSimple/>
    </ErrorBoundary>
  </StrictMode>
)

