import { Action } from "@/components/ui/Action";
import { Container } from "@/components/ui/Layout";

export default function NotFound() {
  return (
    <section className="not-found" aria-labelledby="not-found-heading">
      <Container size="reading">
      <p className="eyebrow">NEXLABS / 404</p>
      <h1 id="not-found-heading">This route did not resolve.</h1>
      <p>The page you are looking for is not part of the current NexLabs system.</p>
      <Action href="/" variant="primary">
        Return home
      </Action>
      </Container>
    </section>
  );
}
