import React, { StrictMode } from "react"
import { createRoot } from "react-dom/client"
//import SpeedControl from "./speed_control_component
import DirControlSimple from "./dir_control_simple"


const rootElement = document.getElementById("root")

if (!rootElement) {
  throw new Error("Root element not found")
}

const root = createRoot(rootElement)

root.render(
  <StrictMode>
      <DirControlSimple/>
  </StrictMode>
)

