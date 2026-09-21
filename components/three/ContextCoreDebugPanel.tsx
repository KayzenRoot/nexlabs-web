type Props = {
  tier: string;
  reason: string;
  state: string;
  paused: boolean;
  fps: number;
  dpr: number;
  drawCalls: number;
  triangles: number;
  asset: string;
};

export function ContextCoreDebugPanel(props: Props) {
  if (process.env.NODE_ENV === "production") return null;
  return <aside className="context-core-debug" aria-label="Context Core runtime debug"><strong>3D debug</strong><span>{props.tier} / {props.state}</span><span>{props.reason} · {props.paused ? "paused" : "active"}</span><span>{Math.round(props.fps)} FPS · DPR {props.dpr.toFixed(2)}</span><span>{props.drawCalls} calls · {props.triangles} tris</span><span>{props.asset}</span></aside>;
}
