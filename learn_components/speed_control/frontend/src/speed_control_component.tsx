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



function SpeedControl({ args, disabled, theme }: ComponentProps): ReactElement {
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
  //const [numClicks, setNumClicks] = useState(0)
  //Ref to store the interval ID for holding
  //const holdInterval = useRef<ReturnType<typeof setInterval> | null>(null)

  const [speed, setSpeed] = useState<number>(default_value)
  //const intervalRef = useRef<NodeJS.Timeout | null>(null)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)


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

  // Clear interval on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [])

  const startChangingSpeed = (direction: "fwd" | "bwd") => {
    if (intervalRef.current) clearInterval(intervalRef.current)

    intervalRef.current = setInterval(() => {
      setSpeed(prev => {
        let newSpeed = prev

        if (direction === "fwd" && prev < max_value) {
          newSpeed = Math.min(prev + increment, max_value)
        } else if (direction === "bwd" && prev > min_value) {
          newSpeed = Math.max(prev - increment, min_value)
        }

        return newSpeed
      })
    }, interval_ms )
  }

  
  const returnToStop = (direction: "fwd" | "bwd") => {
    if (intervalRef.current) clearInterval(intervalRef.current)

    intervalRef.current = setInterval(() => {
      setSpeed(prev => {
        if (direction === "fwd" && prev > default_value ) {
          return Math.max(prev - increment, default_value )
        } else if (direction === "bwd" && prev < default_value ) {
          return Math.min(prev + increment, default_value )
        } else {
          clearInterval(intervalRef.current!)
          return default_value 
        }
      })
    }, interval_ms)
  }

  const handleStop = () => {
    if (intervalRef.current) clearInterval(intervalRef.current)
    setSpeed(default_value )
  }


  // const onFocus = useCallback(() => {
  //   setIsFocused(true)
  // }, [])

  // // Start incrementing on hold
  // const handleMouseDown = useCallback(() => {
  //   if (disabled) return

  //   holdInterval.current = setInterval(() => {
  //     setNumClicks(prev => {
  //       const updated = prev + 1
  //       Streamlit.setComponentValue(updated)
  //       return updated
  //     })
  //   }, 100) // Adjust speed as needed (ms)
  // }, [disabled])

  // //Stop incrementing when released
  // const handleMouseUp = useCallback(() => {
  //   if (holdInterval.current) {
  //     clearInterval(holdInterval.current)
  //     holdInterval.current = null
  //   }
  // }, [])

  // const onBlur = useCallback(() => {
  //   setIsFocused(false)
  //   handleMouseUp() // Also stop holding if user tabs away
  // }, [handleMouseUp])

  
  return (
    <div style={{ display: 'flex', gap: '10px', overflow: 'visible' }}>
      <button
        style={{
          width: '80px',
          height: '80px',
          padding: '10px 0',       // add vertical padding
          margin: 0,               // remove extra margin
          overflow: 'visible',
          border: '1px solid gray',
          cursor: 'pointer',
          lineHeight: 'normal',    // avoid clipping due to line height
          fontSize: '16px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',   // center text vertically
          boxSizing: 'border-box',
          }}
        onMouseDown={() => startChangingSpeed("fwd")}
        onMouseUp={() => returnToStop("fwd")}
        onMouseLeave={() => returnToStop("fwd")}
      >
        FWD
      </button>

      <button onClick={handleStop}>STOP</button>

      <button
        onMouseDown={() => startChangingSpeed("bwd")}
        onMouseUp={() => returnToStop("bwd")}
        onMouseLeave={() => returnToStop("bwd")}
      >
        BWD
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

export default withStreamlitConnection(SpeedControl)
