import { siteContent } from "@/content/site";

export function HomeShell() {
  const { hero } = siteContent;
  return (
    <section className="hero" aria-labelledby="home-heading">
      <div className="shell hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">{hero.eyebrow}</p>
          <h1 id="home-heading">{hero.heading}</h1>
          <p className="hero-body">{hero.body}</p>
          <div className="action-row" aria-label="Featured links">
            <a className="button button-primary" href={hero.primaryAction.href} rel="noreferrer" target="_blank">
              {hero.primaryAction.label}
              <span className="sr-only"> (opens in a new tab)</span>
            </a>
            <a className="button button-secondary" href={hero.secondaryAction.href} rel="noreferrer" target="_blank">
              {hero.secondaryAction.label}
              <span className="sr-only"> (opens in a new tab)</span>
            </a>
          </div>
        </div>
        <aside className="evidence-panel" aria-labelledby="evidence-heading">
          <p className="eyebrow">Engineering evidence</p>
          <h2 id="evidence-heading">A public starting point.</h2>
          {siteContent.evidence.map((evidence) => (
            <div className="evidence-card" key={evidence.id}>
              <p className="evidence-id">{evidence.id}</p>
              <h3>{evidence.label}</h3>
              <p>{evidence.description}</p>
              <a href={evidence.href} rel="noreferrer" target="_blank">
                Open on GitHub<span className="sr-only"> (opens in a new tab)</span>
              </a>
            </div>
          ))}
        </aside>
      </div>
    </section>
  );
}
