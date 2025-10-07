import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps,
} from "streamlit-component-lib"
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  ReactElement,
} from "react"


/**
 *
 * @param {ComponentProps} props - The props object passed from Streamlit
 * @param {Object} props.args - Custom arguments passed from the Python side
 * @param {string} props.args.max_value_x - Example argument showing how to access Python-defined values
 * @param {string} props.args.min_value_x - Example argument showing how to access Python-defined values
 * @param {string} props.args.default_value_x - Example argument showing how to access Python-defined values
 * @param {string} props.args.max_value_y - Example argument showing how to access Python-defined values
 * @param {string} props.args.min_value_y - Example argument showing how to access Python-defined values
 * @param {string} props.args.default_value_y - Example argument showing how to access Python-defined values
 * @param {string} props.args.deadzone_y - Example argument showing how to access Python-defined values
 * @param {string} props.args.interval_ms - Example argument showing how to access Python-defined values
 * @param {boolean} props.disabled - Whether the component is in a disabled state
 * @param {Object} props.theme - Streamlit theme object for consistent styling
 * @returns {ReactElement} The rendered component
 * 
 */


function mapToRange(
  value: number,
  inputMin: number,
  inputMax: number,
  outputMin: number,
  outputMax: number
): number {
  // Clamp the input value to be within input range
  const clamped = Math.max(inputMin, Math.min(value, inputMax))

  // Normalize to 0–1 range
  const normalized = (clamped - inputMin) / (inputMax - inputMin)

  // Scale to output range
  return outputMin + normalized * (outputMax - outputMin)
}


function JoystickControl({ args, disabled, theme }: ComponentProps): ReactElement {
  //Extract custom arguments passed from Python
  const {
    max_value_y = 2000,
    min_value_y = 1000,
    default_value_y = 1500,
    deadzone_y = 0,
    max_value_x = 180,
    min_value_x = 0,
    default_value_x = 90,
    interval_ms = 100,
  } = args

  console.log("Args from Python:", args)
  console.log("Theme from Streamlit:", theme)
  console.log("Disabled:", disabled)

  //Component state
  const [isFocused, setIsFocused] = useState(false)  
  const containerRef = useRef<HTMLImageElement>(null)

  const [isDragging, setIsDragging] = useState(false)
  const [mousePos, setMousePos] = useState({ speed: default_value_y, dir: default_value_x })
  const [mousePosPx, setMousePosPx] = useState({ speed: 0, dir: 0 })



  const style: React.CSSProperties = useMemo(() => {
    if (!theme) return {}

    // Use the theme object to style the button border
    // Access theme properties like primaryColor, backgroundColor, etc.
    const borderStyling = `1px solid ${isFocused ? theme.primaryColor : "gray"}`
    return { border: borderStyling, outline: borderStyling }
  }, [theme, isFocused])

  useEffect(() => {
    try {
      Streamlit.setComponentReady()
      Streamlit.setFrameHeight()
    } catch (error) {
      console.error("Error in useEffect:", error)
      Streamlit.setComponentValue({ error: String(error) })
    }
  }, [])


  const handleMouseDown = () => {
    setIsDragging(true)
  }

  const handleMouseUp = () => {
    setIsDragging(false)
  }

  const handleMouseMove = (e: React.MouseEvent) => {
  if (!isDragging || !containerRef.current) return

  const rect = containerRef.current.getBoundingClientRect()
  const rawX = e.clientX - rect.left
  const rawY = e.clientY - rect.top

  const containerSize = 300 // width and height in pixels


  // no deadzone
  // const mappedY = mapToRange(
  //   rawY,
  //   0,
  //   containerSize,
  //   Number(max_value_y),
  //   Number(min_value_y)
  // )

  //handle Y direction deadzone
  let mappedY: number
  if (rawY < containerSize/2){ // if in top half of circle
    mappedY = mapToRange(rawY, 0, containerSize/2, max_value_y, (default_value_y + deadzone_y))
  } else if (rawY >containerSize/2){ // bottom half of circle
    mappedY = mapToRange(rawY, containerSize/2, containerSize,(default_value_y - deadzone_y), min_value_y)
  }else {
    mappedY = 1500
  }


  const mappedX = mapToRange(
    rawX,
    0,
    containerSize,
    Number(min_value_x),
    Number(max_value_x)
  )



  setMousePos({
    speed: Math.round(mappedY),
    dir: Math.round(mappedX),
  })

  setMousePosPx({
    speed: rawY,
    dir: rawX,
  })
}

  // useEffect(() => {
  //   if (isDragging) {
  //     Streamlit.setComponentValue(mousePos)
  //   }
  // }, [mousePos, isDragging])




/////// TOUCH SCREEN SUPPORT
// Use a ref to always access the latest mousePos
const mousePosRef = useRef(mousePos)
useEffect(() => {
  mousePosRef.current = mousePos
}, [mousePos])


const handleTouchStart = (e: React.TouchEvent) => {
  e.preventDefault()
  setIsDragging(true)
}
const handleTouchMove = (e: React.TouchEvent) => {
  if (!isDragging || !containerRef.current) return
  const touch = e.touches[0]
  const rect = containerRef.current.getBoundingClientRect()
  const rawX = touch.clientX - rect.left
  const rawY = touch.clientY - rect.top

  const containerSize = 300
  const mappedX = mapToRange(
    rawX,
    0,
    containerSize,
    Number(min_value_x),
    Number(max_value_x)
  )
  const mappedY = mapToRange(
    rawY,
    0,
    containerSize,
    Number(max_value_y), // inverted Y
    Number(min_value_y)
  )

  setMousePos({
    speed: Math.round(mappedY),
    dir: Math.round(mappedX),
  })

  setMousePosPx({
    speed: rawY,
    dir: rawX,
  })
}

const handleTouchEnd = (e: React.TouchEvent) => {
  setIsDragging(false)
}




useEffect(() => {
  if (!isDragging) {
    mousePosRef.current = {speed: default_value_y, dir: default_value_x}
    Streamlit.setComponentValue(mousePosRef.current)
    return
  }
  

  const interval = setInterval(() => {
    Streamlit.setComponentValue(mousePosRef.current)
  }, interval_ms)

  return () => clearInterval(interval)
}, [isDragging, interval_ms])



return (
  <div
    ref={containerRef as React.RefObject<HTMLDivElement>}
    onMouseDown={handleMouseDown}
    onMouseUp={handleMouseUp}
    onMouseLeave={handleMouseUp}
    onMouseMove={handleMouseMove}
    onTouchStart={handleTouchStart}
    onTouchMove={handleTouchMove}
    onTouchEnd={handleTouchEnd}
    style={{
      position: "relative",
      width: "300px",
      height: "300px",
      userSelect: "none",
      touchAction: "none",
    }}
  >
    {/* Base joystick image */}
    <img
      src="./red-circle.png"   // assuming it's in /public
      draggable={false}
      alt="Joystick base"
      style={{
        width: "100%",
        height: "100%",
        objectFit: "cover",
        borderRadius: "50%",
        pointerEvents: "none", // allow events to pass through image to parent
      }}
    />

    {/* Draggable marker */}
    {isDragging && (
      <div
        style={{
          position: "absolute",
          left: mousePosPx.dir - 10,     // center marker by offsetting
          top: mousePosPx.speed - 10,
          width: "20px",
          height: "20px",
          backgroundColor: "blue",
          borderRadius: "50%",
          pointerEvents: "none",     // don't intercept mouse events
          border: "2px solid white",
        }}
      />
    )}
  <p>Mouse X: {mousePos.speed}</p>
  <p>Mouse Y: {mousePos.dir}</p>
  <p>Mouse X Px: {mousePosPx.speed}</p>
  <p>Mouse Y PX: {mousePosPx.dir}</p>
  <p>Dragging?: {isDragging ? "Yes" : "No"}</p>
  </div>
)



// simple red circle
// return (
//   <img
//     ref={containerRef}
//     src="./red-circle.png"  // Update this path
//     onMouseDown={handleMouseDown}
//     onMouseUp={handleMouseUp}
//     onMouseLeave={handleMouseUp}
//     onMouseMove={handleMouseMove}
//     draggable={false}
//     style={{
//       width: "300px",
//       height: "300px",
//       borderRadius: "50%",           // Makes the image behave like a circle
//       userSelect: "none",
//       display: "block",
//       objectFit: "cover",            // Ensure the image fills the circle
//       border: "1px solid #ccc",
//     }}
//     alt="Joystick base"
//   />
// )


// empy box
  // return (
  //   <div
  //     ref={containerRef}
  //     onMouseDown={handleMouseDown}
  //     onMouseUp={handleMouseUp}
  //     onMouseLeave={handleMouseUp} // handle edge case: mouse leaves the area
  //     onMouseMove={handleMouseMove}
  //     style={{
  //       width: "100%",
  //       height: "300px",
  //       backgroundColor: "#f0f0f0",
  //       border: "1px solid #ccc",
  //       userSelect: "none",
  //     }}
  //   >
  //     <p>Mouse X: {mousePos.speed}</p>
  //     <p>Mouse Y: {mousePos.dir}</p>
  //     <p>Dragging?: {isDragging ? "Yes" : "No"}</p>
  //   </div>
  // )
}


export default withStreamlitConnection(JoystickControl)
