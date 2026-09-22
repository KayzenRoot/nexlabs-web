"use client";

import dynamic from "next/dynamic";
import { useCallback, useEffect, useRef, useState } from "react";
import { StaticContextCore } from "@/components/three/StaticContextCore";
import { ThreeErrorBoundary } from "@/components/three/ThreeErrorBoundary";
import { useAdaptiveFidelity } from "@/three/quality/useAdaptiveFidelity";
import { canUseWebGL, prefersReducedMotion } from "@/three/runtime/capabilities";
import { observeHeroVisibility } from "@/three/runtime/visibility";

const ContextCoreRuntime = dynamic(() => import("@/components/three/ContextCoreRuntime").then((module) => module.ContextCoreRuntime), { ssr: false });

export function ThreeBoundary() {
  const hostRef = useRef<HTMLDivElement>(null);
  const [heroVisible, setHeroVisible] = useState(false);
  const [supportsWebGL, setSupportsWebGL] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const [runtimeFailed, setRuntimeFailed] = useState(false);
  const [runtimeStarted, setRuntimeStarted] = useState(false);
  const [readyTier, setReadyTier] = useState<"LOW" | "MEDIUM" | "HIGH" | null>(null);
  const fidelity = useAdaptiveFidelity({ active: runtimeStarted && !runtimeFailed, paused: !heroVisible, prefersReducedMotion: reducedMotion, canUseWebGL: supportsWebGL, runtimeFailed });

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => {
      setSupportsWebGL(canUseWebGL());
      setReducedMotion(prefersReducedMotion());
    });
    if (!hostRef.current) return undefined;
    const cancelObservation = observeHeroVisibility(hostRef.current, (visible) => {
      window.requestAnimationFrame(() => {
        setHeroVisible(visible);
        if (visible) setRuntimeStarted(true);
      });
    });
    return () => {
      window.cancelAnimationFrame(frame);
      cancelObservation();
    };
  }, []);

  const eligible = supportsWebGL && !reducedMotion && !runtimeFailed && fidelity.tier !== "STATIC";

  const handleFailure = useCallback(() => {
    setRuntimeFailed(true);
    setRuntimeStarted(false);
    setReadyTier(null);
  }, []);
  const handleReady = useCallback(() => setReadyTier(fidelity.tier === "STATIC" ? "LOW" : fidelity.tier), [fidelity.tier]);
  const liveTier = fidelity.tier === "STATIC" ? "LOW" : fidelity.tier;
  const runtimeMounted = runtimeStarted && eligible;
  const runtimeReady = runtimeMounted && readyTier === liveTier;

  return <div ref={hostRef} className={["context-core-boundary", runtimeReady ? "is-live" : "is-static"].join(" ")} role="img" aria-label="Context Core visual system">
    <StaticContextCore />
    {runtimeMounted ? <div className="context-core-runtime" aria-hidden="true"><ThreeErrorBoundary onError={handleFailure}><ContextCoreRuntime key={liveTier} tier={liveTier} paused={fidelity.paused || !heroVisible} onReady={handleReady} onFailure={handleFailure} /></ThreeErrorBoundary></div> : null}
  </div>;
}
