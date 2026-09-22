"use client";

import { Component, type ReactNode } from "react";

type Props = { children: ReactNode; onError: (reason: string) => void };
type State = { failed: boolean };

export class ThreeErrorBoundary extends Component<Props, State> {
  state: State = { failed: false };

  static getDerivedStateFromError(): State {
    return { failed: true };
  }

  componentDidCatch() {
    this.props.onError("runtime-exception");
  }

  render() {
    return this.state.failed ? null : this.props.children;
  }
}
