export type VisibilityMode = "ACTIVE" | "PAUSED";

export function resolveVisibilityMode(documentHidden: boolean, heroVisible: boolean): VisibilityMode {
  return documentHidden || !heroVisible ? "PAUSED" : "ACTIVE";
}

export function observeHeroVisibility(element: HTMLElement, onChange: (visible: boolean) => void): () => void {
  if (typeof window === "undefined" || typeof IntersectionObserver === "undefined") {
    onChange(true);
    return () => undefined;
  }

  let visible = false;
  const emit = () => {
    const next = !document.hidden && visible;
    onChange(next);
  };
  const observer = new IntersectionObserver(
    ([entry]) => {
      visible = Boolean(entry?.isIntersecting);
      emit();
    },
    { rootMargin: "200px 0px", threshold: 0.15 },
  );
  observer.observe(element);
  document.addEventListener("visibilitychange", emit);
  return () => {
    observer.disconnect();
    document.removeEventListener("visibilitychange", emit);
  };
}
