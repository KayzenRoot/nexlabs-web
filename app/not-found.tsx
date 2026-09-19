import Link from "next/link";

export default function NotFound() {
  return (
    <section className="shell not-found" aria-labelledby="not-found-heading">
      <p className="eyebrow">NEXLABS / 404</p>
      <h1 id="not-found-heading">This route is not part of the current system.</h1>
      <p>The page you are looking for is not available in this CP-01 foundation.</p>
      <Link className="button button-primary" href="/">
        Return home
      </Link>
    </section>
  );
}
