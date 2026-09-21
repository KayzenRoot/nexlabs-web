import type { LiveFidelityTier } from "@/three/core/contextCoreAssets";
import { CONTEXT_CORE_CLIPS, type ContextCoreSemanticState } from "@/three/core/contextCoreAssets";

export type ContextCoreMachine = {
  status: "STATIC" | "LIVE";
  state: ContextCoreSemanticState;
  paused: boolean;
  introIndex: number;
  missingClips: readonly string[];
  sessionFailed: boolean;
};

export type ContextCoreEvent =
  | { type: "LOAD_SUCCESS"; clipNames: readonly string[]; tier: LiveFidelityTier }
  | { type: "ADVANCE" }
  | { type: "PAUSE" }
  | { type: "RESUME" }
  | { type: "FAIL" };

const CLIP_SUFFIX: Record<ContextCoreSemanticState, string> = {
  DORMANT: "Dormant",
  INTAKE: "Intake",
  INDEX: "Index",
  RETRIEVE: "Retrieve",
  ASSEMBLE: "Assemble",
  RESOLVE: "Resolve",
  IDLE: "Idle",
};

export function clipNameForState(state: ContextCoreSemanticState, tier: LiveFidelityTier): string {
  return `NL_ANIM_${CLIP_SUFFIX[state]}_${tier}`;
}

export function requiredClipNames(tier: LiveFidelityTier): readonly string[] {
  return CONTEXT_CORE_CLIPS.map((state) => clipNameForState(state, tier));
}

export function createContextCoreMachine(): ContextCoreMachine {
  return { status: "STATIC", state: "DORMANT", paused: false, introIndex: 0, missingClips: [], sessionFailed: false };
}

export function transitionContextCore(machine: ContextCoreMachine, event: ContextCoreEvent): ContextCoreMachine {
  if (event.type === "FAIL") return { ...machine, status: "STATIC", state: "RESOLVE", sessionFailed: true, paused: false };
  if (event.type === "PAUSE") return { ...machine, paused: true };
  if (event.type === "RESUME") return { ...machine, paused: false };
  if (event.type === "LOAD_SUCCESS") {
    const missingClips = requiredClipNames(event.tier).filter((clip) => !event.clipNames.includes(clip));
    if (missingClips.length > 0) return { ...machine, status: "STATIC", state: "RESOLVE", missingClips, sessionFailed: true };
    return { ...machine, status: "LIVE", state: "DORMANT", introIndex: 0, missingClips: [], sessionFailed: false };
  }
  if (event.type === "ADVANCE" && machine.status === "LIVE" && !machine.paused) {
    const nextIndex = Math.min(machine.introIndex + 1, CONTEXT_CORE_CLIPS.length - 1);
    return { ...machine, introIndex: nextIndex, state: CONTEXT_CORE_CLIPS[nextIndex] };
  }
  return machine;
}
