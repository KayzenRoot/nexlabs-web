export function PrincipleCard({ label, description }: { label: string; description: string }) {
  return <article className="principle-card"><p className="label">{label}</p><p>{description}</p></article>;
}
