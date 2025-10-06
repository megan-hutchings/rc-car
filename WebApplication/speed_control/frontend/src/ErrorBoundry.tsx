import React, { ErrorInfo } from "react"

interface Props {
  children: React.ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Error caught in ErrorBoundary:", error, info)
  }

  render() {
    if (this.state.hasError) {
      return <div>⚠️ Something went wrong: {this.state.error?.message}</div>
    }

    return this.props.children
  }
}

export default ErrorBoundary
