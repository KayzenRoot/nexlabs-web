import type { FidelityTier } from "@/three/quality/adaptiveFidelity";

export type LiveFidelityTier = Exclude<FidelityTier, "STATIC">;

export const CONTEXT_CORE_CLIPS = [
  "DORMANT",
  "INTAKE",
  "INDEX",
  "RETRIEVE",
  "ASSEMBLE",
  "RESOLVE",
  "IDLE",
] as const;

export type ContextCoreSemanticState = (typeof CONTEXT_CORE_CLIPS)[number];

export type ContextCoreAsset = {
  tier: LiveFidelityTier;
  modelUrl: string;
  fallbackUrl: string;
  sourcePath: string;
  sourceSha256: string;
  bytes: number;
  requiredCapabilities: readonly ["webgl", "glb"];
};

export const contextCoreAssets: Record<LiveFidelityTier, ContextCoreAsset> = {
  HIGH: {
    tier: "HIGH",
    modelUrl: "/models/context-core/context-core-high.glb",
    fallbackUrl: "/images/context-core/hero-16x9.png",
    sourcePath: "artifacts/cp06/exports/NEXLABS_CP06_HIGH_v001.glb",
    sourceSha256: "811ba946fa693c4151df3cb688cc73a4bf178e31a28fb88e39f1c9d18dec3870",
    bytes: 73448,
    requiredCapabilities: ["webgl", "glb"],
  },
  MEDIUM: {
    tier: "MEDIUM",
    modelUrl: "/models/context-core/context-core-med.glb",
    fallbackUrl: "/images/context-core/hero-16x9.png",
    sourcePath: "artifacts/cp06/exports/NEXLABS_CP06_MED_v001.glb",
    sourceSha256: "016e2704a3c60fc61ccde1084c848330cc0cc8ff8d8961b09d74b83d139ccf2e",
    bytes: 69528,
    requiredCapabilities: ["webgl", "glb"],
  },
  LOW: {
    tier: "LOW",
    modelUrl: "/models/context-core/context-core-low.glb",
    fallbackUrl: "/images/context-core/hero-16x9.png",
    sourcePath: "artifacts/cp06/exports/NEXLABS_CP06_LOW_v001.glb",
    sourceSha256: "97421e7c4c961b407f11d78fb924c022391f52731ac09deec2263fdbf94870e7",
    bytes: 65540,
    requiredCapabilities: ["webgl", "glb"],
  },
};

export const contextCoreStaticFallbacks = {
  landscape: {
    url: "/images/context-core/hero-16x9.png",
    webpUrl: "/release-visuals/hero/context-core-16x9.webp",
    avifUrl: "/release-visuals/hero/context-core-16x9.avif",
    sourcePath: "artifacts/cp06/static/hero-16x9.png",
    sourceSha256: "42833aa76e81070a2aa9a61c4d15673bcc6e21168d7f66dcf8bd34b309ca726b",
    bytes: 83401,
  },
  portrait: {
    url: "/images/context-core/hero-4x5.png",
    webpUrl: "/release-visuals/hero/context-core-4x5.webp",
    avifUrl: "/release-visuals/hero/context-core-4x5.avif",
    sourcePath: "artifacts/cp06/static/hero-4x5.png",
    sourceSha256: "673530c6587376cdb8311d72189fa42f33dce0b5f1f17bc96661f4a74130a72e",
    bytes: 95512,
  },
  square: {
    url: "/images/context-core/hero-1x1.png",
    webpUrl: "/release-visuals/hero/context-core-1x1.webp",
    avifUrl: "/release-visuals/hero/context-core-1x1.avif",
    sourcePath: "artifacts/cp06/static/hero-1x1.png",
    sourceSha256: "956fb4c5c584ed6c9ae40ae9fe1aad7735593b2c002d5f0d50545a44956918e6",
    bytes: 85498,
  },
} as const;

export function getContextCoreAsset(tier: FidelityTier): ContextCoreAsset | undefined {
  return tier === "STATIC" ? undefined : contextCoreAssets[tier];
}
