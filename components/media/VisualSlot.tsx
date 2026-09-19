import type { HTMLAttributes } from "react";

type VisualSlotProps = HTMLAttributes<HTMLDivElement> & { label?: string; description?: string; decorative?: boolean };

export function VisualSlot({ label = "Provisional visual system slot", description = "Reserved for an approved NexLabs visual asset.", decorative = false, className = "", ...props }: VisualSlotProps) {
  return <div className={["visual-slot", className].filter(Boolean).join(" ")} aria-hidden={decorative || undefined} role={decorative ? undefined : "img"} aria-label={decorative ? undefined : label} {...props}><span className="visual-slot-grid" aria-hidden="true" /><span className="visual-slot-copy">{decorative ? null : <><span className="label">{label}</span><span>{description}</span></>}</span></div>;
}

export function HeroVisualSlot() {
  return <VisualSlot className="hero-visual-slot" label="Provisional NexLabs visual system slot" description="Replaceable media boundary; no final brand artwork is represented." />;
}
