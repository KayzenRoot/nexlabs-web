"use client";

import { useEffect, useRef, useState } from "react";
import { createInitialAdaptiveState, stepAdaptiveFidelity, type AdaptiveFidelityState } from "@/three/quality/adaptiveFidelity";

type UseAdaptiveFidelityOptions = {
  active: boolean;
  paused: boolean;
  prefersReducedMotion: boolean;
  canUseWebGL: boolean;
  runtimeFailed: boolean;
};

export function useAdaptiveFidelity(options: UseAdaptiveFidelityOptions): AdaptiveFidelityState {
  const { active, canUseWebGL, paused, prefersReducedMotion, runtimeFailed } = options;
  const [state, setState] = useState(() => createInitialAdaptiveState(options));
  const stateRef = useRef(state);
  const optionsRef = useRef(options);

  useEffect(() => {
    optionsRef.current = { active, canUseWebGL, paused, prefersReducedMotion, runtimeFailed };
  }, [active, canUseWebGL, paused, prefersReducedMotion, runtimeFailed]);

  useEffect(() => {
    const initial = createInitialAdaptiveState({ canUseWebGL, prefersReducedMotion });
    const frame = requestAnimationFrame(() => {
      stateRef.current = initial;
      setState(initial);
    });
    return () => cancelAnimationFrame(frame);
  }, [canUseWebGL, prefersReducedMotion]);

  useEffect(() => {
    if (!active) return undefined;
    let frame = 0;
    let last = performance.now();
    const tick = (now: number) => {
      const currentOptions = optionsRef.current;
      const previous = stateRef.current;
      const next = stepAdaptiveFidelity(previous, {
        frameTimeMs: now - last,
        nowMs: now,
        prefersReducedMotion: currentOptions.prefersReducedMotion,
        canUseWebGL: currentOptions.canUseWebGL,
        runtimeFailed: currentOptions.runtimeFailed,
        documentHidden: typeof document !== "undefined" && document.hidden,
        heroOffscreen: currentOptions.paused,
      });
      last = now;
      stateRef.current = next;
      if (next.tier !== previous.tier || next.reason !== previous.reason || next.paused !== previous.paused || next.sessionLocked !== previous.sessionLocked) setState(next);
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [active]);

  return state;
}
