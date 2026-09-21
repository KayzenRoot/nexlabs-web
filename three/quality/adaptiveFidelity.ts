export const FIDELITY_TIERS = ["STATIC", "LOW", "MEDIUM", "HIGH"] as const;
export type FidelityTier = (typeof FIDELITY_TIERS)[number];

export type FidelityReason =
  | "initial-conservative"
  | "reduced-motion"
  | "webgl-unavailable"
  | "runtime-failure"
  | "document-hidden"
  | "hero-offscreen"
  | "warmup"
  | "sustained-slow-frames"
  | "stable-frame-time"
  | "paused";

export type AdaptiveFidelityState = {
  tier: FidelityTier;
  reason: FidelityReason;
  paused: boolean;
  sessionLocked: boolean;
  samples: readonly number[];
  stableFrames: number;
  lastDowngradeAt: number | null;
};

export type AdaptiveFidelitySignals = {
  frameTimeMs: number;
  nowMs: number;
  prefersReducedMotion: boolean;
  canUseWebGL: boolean;
  runtimeFailed: boolean;
  documentHidden: boolean;
  heroOffscreen: boolean;
};

export const ADAPTIVE_FIDELITY_LIMITS = {
  warmupFrames: 30,
  rollingWindow: 30,
  slowFrameMs: 28,
  stableFrameMs: 18,
  downgradeThreshold: 0.7,
  upgradeStableFrames: 180,
  upgradeCooldownMs: 10_000,
} as const;

function lowerTier(tier: FidelityTier): FidelityTier {
  const index = FIDELITY_TIERS.indexOf(tier);
  return index <= 0 ? "STATIC" : FIDELITY_TIERS[index - 1];
}

function higherTier(tier: FidelityTier): FidelityTier {
  const index = FIDELITY_TIERS.indexOf(tier);
  return index >= FIDELITY_TIERS.length - 1 ? "HIGH" : FIDELITY_TIERS[index + 1];
}

export function selectInitialTier({ prefersReducedMotion, canUseWebGL }: Pick<AdaptiveFidelitySignals, "prefersReducedMotion" | "canUseWebGL">): FidelityTier {
  if (prefersReducedMotion) return "STATIC";
  if (!canUseWebGL) return "STATIC";
  return "LOW";
}

export function createInitialAdaptiveState(signals: Pick<AdaptiveFidelitySignals, "prefersReducedMotion" | "canUseWebGL">): AdaptiveFidelityState {
  const tier = selectInitialTier(signals);
  return {
    tier,
    reason: signals.prefersReducedMotion ? "reduced-motion" : signals.canUseWebGL ? "initial-conservative" : "webgl-unavailable",
    paused: false,
    sessionLocked: tier === "STATIC",
    samples: [],
    stableFrames: 0,
    lastDowngradeAt: null,
  };
}

export function stepAdaptiveFidelity(state: AdaptiveFidelityState, signals: AdaptiveFidelitySignals): AdaptiveFidelityState {
  if (signals.prefersReducedMotion) return { ...state, tier: "STATIC", reason: "reduced-motion", paused: false, sessionLocked: true };
  if (signals.runtimeFailed) return { ...state, tier: "STATIC", reason: "runtime-failure", paused: false, sessionLocked: true };
  if (!signals.canUseWebGL) return { ...state, tier: "STATIC", reason: "webgl-unavailable", paused: false, sessionLocked: true };
  if (state.sessionLocked) return state;
  if (signals.documentHidden) return { ...state, paused: true, reason: "document-hidden" };
  if (signals.heroOffscreen) return { ...state, paused: true, reason: "hero-offscreen" };

  const samples = [...state.samples, signals.frameTimeMs].slice(-ADAPTIVE_FIDELITY_LIMITS.rollingWindow);
  const stableFrames = signals.frameTimeMs <= ADAPTIVE_FIDELITY_LIMITS.stableFrameMs ? state.stableFrames + 1 : 0;
  const next = { ...state, paused: false, samples, stableFrames, reason: samples.length < ADAPTIVE_FIDELITY_LIMITS.warmupFrames ? "warmup" : state.reason };
  if (samples.length < ADAPTIVE_FIDELITY_LIMITS.warmupFrames) return next;

  const slowSamples = samples.filter((sample) => sample > ADAPTIVE_FIDELITY_LIMITS.slowFrameMs).length;
  if (slowSamples / samples.length >= ADAPTIVE_FIDELITY_LIMITS.downgradeThreshold && next.tier !== "STATIC") {
    return {
      ...next,
      tier: lowerTier(next.tier),
      reason: "sustained-slow-frames",
      samples: [],
      stableFrames: 0,
      lastDowngradeAt: signals.nowMs,
    };
  }

  const cooldownComplete = next.lastDowngradeAt === null || signals.nowMs - next.lastDowngradeAt >= ADAPTIVE_FIDELITY_LIMITS.upgradeCooldownMs;
  if (next.tier !== "HIGH" && next.stableFrames >= ADAPTIVE_FIDELITY_LIMITS.upgradeStableFrames && cooldownComplete) {
    return { ...next, tier: higherTier(next.tier), reason: "stable-frame-time", stableFrames: 0, samples: [] };
  }

  return next;
}
