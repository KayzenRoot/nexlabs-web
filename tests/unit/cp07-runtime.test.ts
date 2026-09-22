import { describe, expect, it } from "vitest";
import { createInitialAdaptiveState, stepAdaptiveFidelity, type AdaptiveFidelityState } from "@/three/quality/adaptiveFidelity";
import { contextCoreAssets } from "@/three/core/contextCoreAssets";
import { clipNameForState, createContextCoreMachine, requiredClipNames, transitionContextCore } from "@/three/state/contextCoreStateMachine";
import { resolveVisibilityMode } from "@/three/runtime/visibility";

const signals = (frameTimeMs: number, nowMs: number) => ({
  frameTimeMs,
  nowMs,
  prefersReducedMotion: false,
  canUseWebGL: true,
  runtimeFailed: false,
  documentHidden: false,
  heroOffscreen: false,
});

function runFrames(state: AdaptiveFidelityState, count: number, frameTimeMs: number, start = 0) {
  let current = state;
  for (let index = 0; index < count; index += 1) current = stepAdaptiveFidelity(current, signals(frameTimeMs, start + index * 100));
  return current;
}

describe("CP-07 adaptive fidelity", () => {
  it("starts conservatively and respects reduced motion", () => {
    expect(createInitialAdaptiveState({ prefersReducedMotion: false, canUseWebGL: true }).tier).toBe("LOW");
    const reduced = createInitialAdaptiveState({ prefersReducedMotion: true, canUseWebGL: true });
    expect(reduced.tier).toBe("STATIC");
    expect(reduced.sessionLocked).toBe(true);
  });

  it("ignores an isolated slow frame", () => {
    let state = createInitialAdaptiveState({ prefersReducedMotion: false, canUseWebGL: true });
    state = runFrames(state, 29, 16);
    state = stepAdaptiveFidelity(state, signals(60, 2900));
    state = runFrames(state, 1, 16, 3000);
    expect(state.tier).toBe("LOW");
  });

  it("downgrades only after sustained slow evidence", () => {
    const state = runFrames(createInitialAdaptiveState({ prefersReducedMotion: false, canUseWebGL: true }), 30, 40);
    expect(state.tier).toBe("STATIC");
    expect(state.reason).toBe("sustained-slow-frames");
  });

  it("upgrades one tier after delayed stability", () => {
    const start: AdaptiveFidelityState = { ...createInitialAdaptiveState({ prefersReducedMotion: false, canUseWebGL: true }), tier: "LOW", sessionLocked: false };
    const state = runFrames(start, 210, 16);
    expect(state.tier).toBe("MEDIUM");
  });

  it("locks the session to STATIC after runtime failure and pauses hidden work", () => {
    const start = createInitialAdaptiveState({ prefersReducedMotion: false, canUseWebGL: true });
    const failed = stepAdaptiveFidelity(start, { ...signals(16, 0), runtimeFailed: true });
    expect(failed.tier).toBe("STATIC");
    expect(failed.sessionLocked).toBe(true);
    const paused = stepAdaptiveFidelity(start, { ...signals(16, 0), documentHidden: true });
    expect(paused.paused).toBe(true);
    expect(resolveVisibilityMode(true, true)).toBe("PAUSED");
    expect(resolveVisibilityMode(false, false)).toBe("PAUSED");
    expect(resolveVisibilityMode(false, true)).toBe("ACTIVE");
  });
});

describe("CP-07 Context Core semantic machine", () => {
  it("maps all approved clips to exact tiered GLB action names", () => {
    expect(clipNameForState("DORMANT", "HIGH")).toBe("NL_ANIM_Dormant_HIGH");
    expect(requiredClipNames("MEDIUM")).toEqual([
      "NL_ANIM_Dormant_MEDIUM",
      "NL_ANIM_Intake_MEDIUM",
      "NL_ANIM_Index_MEDIUM",
      "NL_ANIM_Retrieve_MEDIUM",
      "NL_ANIM_Assemble_MEDIUM",
      "NL_ANIM_Resolve_MEDIUM",
      "NL_ANIM_Idle_MEDIUM",
    ]);
    expect(contextCoreAssets.LOW.bytes).toBe(65540);
  });

  it("runs the bounded intro once and settles in IDLE", () => {
    let machine = transitionContextCore(createContextCoreMachine(), { type: "LOAD_SUCCESS", tier: "HIGH", clipNames: requiredClipNames("HIGH") });
    expect(machine.status).toBe("LIVE");
    for (let index = 0; index < 6; index += 1) machine = transitionContextCore(machine, { type: "ADVANCE" });
    expect(machine.state).toBe("IDLE");
    expect(transitionContextCore(machine, { type: "ADVANCE" }).state).toBe("IDLE");
  });

  it("fails closed for missing clips and preserves pause state", () => {
    let machine = transitionContextCore(createContextCoreMachine(), { type: "LOAD_SUCCESS", tier: "LOW", clipNames: ["NL_ANIM_Dormant_LOW"] });
    expect(machine.status).toBe("STATIC");
    expect(machine.state).toBe("RESOLVE");
    expect(machine.missingClips.length).toBe(6);
    machine = transitionContextCore(transitionContextCore(createContextCoreMachine(), { type: "LOAD_SUCCESS", tier: "HIGH", clipNames: requiredClipNames("HIGH") }), { type: "PAUSE" });
    expect(transitionContextCore(machine, { type: "ADVANCE" }).state).toBe("DORMANT");
    expect(transitionContextCore(machine, { type: "RESUME" }).paused).toBe(false);
    expect(transitionContextCore(machine, { type: "FAIL" }).sessionFailed).toBe(true);
  });
});
