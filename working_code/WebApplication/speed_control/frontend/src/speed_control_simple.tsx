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
 * @param {string} props.args.max_value - Example argument showing how to access Python-defined values
 * @param {string} props.args.min_value - Example argument showing how to access Python-defined values
 * @param {string} props.args.default_value - Example argument showing how to access Python-defined values
 * @param {string} props.args.increment - Example argument showing how to access Python-defined values
 * @param {string} props.args.interval_ms - Example argument showing how to access Python-defined values
 * @param {boolean} props.disabled - Whether the component is in a disabled state
 * @param {Object} props.theme - Streamlit theme object for consistent styling
 * @returns {ReactElement} The rendered component
 * 
 */



function SpeedControlSimple({ args, disabled, theme }: ComponentProps): ReactElement {
  //Extract custom arguments passed from Python
  const {
    max_value = 2000,
    min_value = 1000,
    default_value = 1500,
    increment = 10,
    interval_ms = 100,
  } = args

  console.log("Args from Python:", args)
  console.log("Theme from Streamlit:", theme)
  console.log("Disabled:", disabled)

  //Component state
  const [isFocused, setIsFocused] = useState(false)


  const [speed, setSpeed] = useState<number>(default_value)
  const [activeDir, setActiveDir] = useState<'fwd' | 'bwd' | null>(null) // 'fwd' | 'bwd' | null // just for button colours
  const [stopPressed, setStopPressed] = useState(false)


  /**
   * Dynamic styling based on Streamlit theme and component state
   * This demonstrates how to use the Streamlit theme for consistent styling
   */
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

  // Send speed to Streamlit
  useEffect(() => {
    Streamlit.setComponentValue(speed)
  }, [speed])




  useEffect(() => {
  const handleKeyDown = (event: KeyboardEvent) => {
    if (disabled) return

    switch (event.key) {
      case "ArrowUp":
        startChangingSpeed("fwd")
        break
      case "ArrowDown":
        startChangingSpeed("bwd")
        break
    }
  } 
  const handleKeyUp = (event: KeyboardEvent) => {
    switch (event.key) {
      case "ArrowUp":
      case "ArrowDown":
        returnToStop()
        break
    }
  }

  window.addEventListener("keydown", handleKeyDown)
  window.addEventListener("keyup", handleKeyUp)

  return () => {
    window.removeEventListener("keydown", handleKeyDown)
    window.removeEventListener("keyup", handleKeyUp)
  }
}, [disabled])

const startChangingSpeed = (direction: "fwd" | "bwd") => {

  setActiveDir(direction)
  setStopPressed(false)

  if (direction === "fwd") {
    setSpeed(prev => {
      if (prev !== max_value) return max_value
      Streamlit.setComponentValue(max_value)
      return prev
    })
  } else if (direction === "bwd") {
    setSpeed(prev => {
      if (prev !== min_value) return min_value
      Streamlit.setComponentValue(min_value)
      return prev
    })
  }
}
  
  const returnToStop = () => {
    setActiveDir(null)
    setSpeed(prev => {
      if (prev !== default_value) {
        return default_value
      } else {
        // Send it manually because setSpeed won't re-trigger useEffect
        Streamlit.setComponentValue(default_value)
        return prev
      }
    })
  }



  const handleStop = () => {
    setSpeed(default_value)
    setStopPressed(true)
  }



  
return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        justifyContent: 'space-between',
        padding: '10px',
        boxSizing: 'border-box',
      }}
    >
      {/* FWD Button */}
      <button
        style={{
          flex: 1,
          height: '100px',
          margin: '0 5px',
          backgroundColor: activeDir === 'fwd' ? 'lightgreen' : '',
          border: '1px solid gray',
          fontSize: '18px',
          cursor: 'pointer',
        }}
        onMouseDown={() => startChangingSpeed("fwd")}
        onMouseUp={returnToStop}
        onMouseLeave={returnToStop}
        onTouchStart={() => startChangingSpeed("fwd")}
        onTouchEnd={returnToStop}
        onTouchCancel={returnToStop}
      >
        FWD!
      </button>

      {/* STOP Button */}
      <button
        style={{
          flex: 1,
          height: '100px',
          margin: '0 5px',
          backgroundColor: stopPressed ? 'lightcoral' : '',
          border: '1px solid gray',
          fontSize: '18px',
          cursor: 'pointer',
        }}
        onClick={handleStop}
      >
        STOP
      </button>

      {/* BWD Button */}
      <button
        style={{
          flex: 1,
          height: '100px',
          margin: '0 5px',
          backgroundColor: activeDir === 'bwd' ? 'lightgreen' : '',
          border: '1px solid gray',
          fontSize: '18px',
          cursor: 'pointer',
        }}
        onMouseDown={() => startChangingSpeed("bwd")}
        onMouseUp={returnToStop}
        onMouseLeave={returnToStop}
        onTouchStart={() => startChangingSpeed("bwd")}
        onTouchEnd={returnToStop}
        onTouchCancel={returnToStop}
      >
        BWD!
      </button>
    </div>
  )
}
/**
 * withStreamlitConnection is a higher-order component (HOC) that:
 * 1. Establishes communication between this component and Streamlit
 * 2. Passes Streamlit's theme settings to your component
 * 3. Handles passing arguments from Python to your component
 * 4. Handles component re-renders when Python args change
 *
 * You don't need to modify this wrapper unless you need custom connection behavior.
 */

export default withStreamlitConnection(SpeedControlSimple)
