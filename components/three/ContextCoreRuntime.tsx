"use client";

import { Canvas, useFrame, useLoader, useThree } from "@react-three/fiber";
import { useEffect, useRef, useState, Suspense } from "react";
import { AnimationMixer, LoopOnce, LoopRepeat } from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { ContextCoreDebugPanel } from "@/components/three/ContextCoreDebugPanel";
import { getContextCoreAsset, type LiveFidelityTier } from "@/three/core/contextCoreAssets";
import { clipNameForState, createContextCoreMachine, transitionContextCore } from "@/three/state/contextCoreStateMachine";

type RuntimeStats = { fps: number; dpr: number; drawCalls: number; triangles: number; state: string; reason: string; asset: string };
type Props = { tier: LiveFidelityTier; paused: boolean; onReady: () => void; onFailure: (reason: string) => void };
type SceneProps = Props & { onStats: (stats: RuntimeStats) => void };

function ContextCoreScene({ tier, paused, onReady, onFailure, onStats }: SceneProps) {
  const asset = getContextCoreAsset(tier);
  const gltf = useLoader(GLTFLoader, asset?.modelUrl ?? "");
  const { gl } = useThree();
  const mixerRef = useRef<AnimationMixer | null>(null);
  const readyRef = useRef(false);
  const loadedRef = useRef(false);
  const [machine, setMachine] = useState(createContextCoreMachine);
  const lastStatsAt = useRef(0);

  useEffect(() => {
    if (!asset || loadedRef.current) return;
    loadedRef.current = true;
    const next = transitionContextCore(createContextCoreMachine(), { type: "LOAD_SUCCESS", clipNames: gltf.animations.map((clip) => clip.name), tier });
    setMachine(next);
    if (next.status === "STATIC") onFailure("missing-required-clips");
    mixerRef.current = new AnimationMixer(gltf.scene);
    return () => {
      mixerRef.current?.stopAllAction();
      mixerRef.current = null;
    };
  }, [asset, gltf, onFailure, tier]);

  useEffect(() => {
    if (paused || machine.status !== "LIVE" || machine.paused || machine.state === "IDLE") return undefined;
    const timeout = window.setTimeout(() => setMachine((current) => transitionContextCore(current, { type: "ADVANCE" })), 650);
    return () => window.clearTimeout(timeout);
  }, [machine.paused, machine.state, machine.status, paused]);

  useEffect(() => {
    if (machine.status !== "LIVE" || !mixerRef.current) return undefined;
    const clip = gltf.animations.find((item) => item.name === clipNameForState(machine.state, tier));
    if (!clip) {
      onFailure("clip-resolution-failure");
      return undefined;
    }
    const action = mixerRef.current.clipAction(clip);
    action.reset();
    action.clampWhenFinished = machine.state !== "IDLE";
    action.setLoop(machine.state === "IDLE" ? LoopRepeat : LoopOnce, machine.state === "IDLE" ? Infinity : 1).play();
    return () => { action.stop(); };
  }, [gltf.animations, machine.state, machine.status, onFailure, tier]);

  useFrame((_state, delta) => {
    if (paused) return;
    mixerRef.current?.update(delta);
    if (!readyRef.current) {
      readyRef.current = true;
      onReady();
    }
    if (process.env.NODE_ENV !== "production") {
      const now = performance.now();
      if (now - lastStatsAt.current >= 500) {
        lastStatsAt.current = now;
        onStats({ fps: delta > 0 ? 1 / delta : 0, dpr: gl.getPixelRatio(), drawCalls: gl.info.render.calls, triangles: gl.info.render.triangles, state: machine.state, reason: machine.status === "LIVE" ? "semantic-runtime" : "static-fallback", asset: asset?.modelUrl ?? "static" });
      }
    }
  });

  return <primitive object={gltf.scene} dispose={null} />;
}

export function ContextCoreRuntime(props: Props) {
  const dpr: [number, number] = props.tier === "HIGH" ? [1, 1.5] : props.tier === "MEDIUM" ? [1, 1.25] : [1, 1.1];
  const [stats, setStats] = useState<RuntimeStats>({ fps: 0, dpr: 1, drawCalls: 0, triangles: 0, state: "DORMANT", reason: "initializing", asset: getContextCoreAsset(props.tier)?.modelUrl ?? "static" });
  return <><Canvas className="context-core-canvas" aria-hidden="true" frameloop={props.paused ? "demand" : "always"} dpr={dpr} camera={{ position: [0, 0, 4], fov: 35 }} gl={{ alpha: true, antialias: props.tier === "HIGH", powerPreference: "low-power" }} onCreated={({ gl }) => { if (!gl.getContext()) props.onFailure("webgl-context-failure"); }}><Suspense fallback={null}><ContextCoreScene {...props} onStats={setStats} /></Suspense></Canvas><ContextCoreDebugPanel tier={props.tier} reason={stats.reason} state={stats.state} paused={props.paused} fps={stats.fps} dpr={stats.dpr} drawCalls={stats.drawCalls} triangles={stats.triangles} asset={stats.asset} /></>;
}
