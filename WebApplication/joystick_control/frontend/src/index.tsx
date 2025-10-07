import React, { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import JoystickControl from "./joystick_control"


const rootElement = document.getElementById("root")

if (!rootElement) {
  throw new Error("Root element not found")
}

const root = createRoot(rootElement)

root.render(
  <StrictMode>
      <JoystickControl/>
  </StrictMode>
)