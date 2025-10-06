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



function DirControlSimple({ args, disabled, theme }: ComponentProps): ReactElement {
  //Extract custom arguments passed from Python
  const {
    max_value = 180,
    min_value = 0,
    default_value = 90,
    increment = 10,
    interval_ms = 100,
  } = args

  console.log("Args from Python:", args)
  console.log("Theme from Streamlit:", theme)
  console.log("Disabled:", disabled)

  //Component state
  const [isFocused, setIsFocused] = useState(false)


  const [dir, setDir] = useState<number>(default_value)
  const [activeDir, setActiveDir] = useState<'fwd' | 'bwd' | null>(null) // 'fwd' | 'bwd' | null // just for button colours

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
    Streamlit.setComponentValue(dir)
  }, [dir])




  useEffect(() => {
  const handleKeyDown = (event: KeyboardEvent) => {
    if (disabled) return

    switch (event.key) {
      case "ArrowUp":
        startChangingDir("fwd")
        break
      case "ArrowDown":
        startChangingDir("bwd")
        break
    }
  } 
  const handleKeyUp = (event: KeyboardEvent) => {
    switch (event.key) {
      case "ArrowUp":
      case "ArrowDown":
        returnToCentre()
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

const startChangingDir = (direction: "fwd" | "bwd") => {
  setActiveDir(direction)

  if (direction === "fwd") {
    setDir(prev => {
      if (prev !== max_value) return max_value
      Streamlit.setComponentValue(max_value)
      return prev
    })
  } else if (direction === "bwd") {
    setDir(prev => {
      if (prev !== min_value) return min_value
      Streamlit.setComponentValue(min_value)
      return prev
    })
  }
}
  
  const returnToCentre = () => {
    setActiveDir(null)
    setDir(prev => {
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
    setDir(default_value)
  }



  
//   return (
//     <div
//       style={{
//         display: 'flex',
//         flexWrap: 'wrap',
//         gap: '10px',
//         justifyContent: 'center',
//         padding: '10px',
//       }}>
//       <button
//         style={{
//           width: '80px',
//           height: '80px',
//           padding: '10px 0',       // add vertical padding
//           margin: 0,               // remove extra margin
//           overflow: 'visible',
//           border: '1px solid gray',
//           cursor: 'pointer',
//           lineHeight: 'normal',    // avoid clipping due to line height
//           fontSize: '16px',
//           display: 'flex',
//           justifyContent: 'center',
//           alignItems: 'center',   // center text vertically
//           boxSizing: 'border-box',
//           }}
//         onMouseDown={() => startChangingDir("fwd")}
//         onMouseUp={() => returnToCentre()}
//         onMouseLeave={() => returnToCentre()}
//         onTouchStart={() => startChangingDir("fwd")}
//         onTouchEnd={() => returnToCentre()}
//         onTouchCancel={() => returnToCentre()}
//       >
//         LEFT!
//       </button>

//       <button onClick={handleStop}>STOP</button>

//       <button
//         onMouseDown={() => startChangingDir("bwd")}
//         onMouseUp={() => returnToCentre()}
//         onMouseLeave={() => returnToCentre()}
//         onTouchStart={() => startChangingDir("bwd")}
//         onTouchEnd={() => returnToCentre()}
//         onTouchCancel={() => returnToCentre()}
//       >
//         RIGHT!
//       </button>
//     </div>
//   )
// }


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
      {/* LEFT (FWD) BUTTON */}
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
        onMouseDown={() => startChangingDir("fwd")}
        onMouseUp={returnToCentre}
        onMouseLeave={returnToCentre}
        onTouchStart={() => startChangingDir("fwd")}
        onTouchEnd={returnToCentre}
        onTouchCancel={returnToCentre}
      >
        LEFT!
      </button>

      {/* RIGHT (BWD) BUTTON */}
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
        onMouseDown={() => startChangingDir("bwd")}
        onMouseUp={returnToCentre}
        onMouseLeave={returnToCentre}
        onTouchStart={() => startChangingDir("bwd")}
        onTouchEnd={returnToCentre}
        onTouchCancel={returnToCentre}
      >
        RIGHT!
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

export default withStreamlitConnection(DirControlSimple)
