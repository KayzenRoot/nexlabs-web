import type { HTMLAttributes, ReactNode } from "react";

export function Text({ children, className = "", ...props }: HTMLAttributes<HTMLParagraphElement> & { children: ReactNode }) {
  return <p className={className} {...props}>{children}</p>;
}

type HeadingProps = HTMLAttributes<HTMLHeadingElement> & { children: ReactNode; level?: 1 | 2 | 3; eyebrow?: string };

export function Heading({ children, className = "", level = 2, eyebrow, ...props }: HeadingProps) {
  const Tag = `h${level}` as "h1" | "h2" | "h3";
  return <>{eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}<Tag className={className} {...props}>{children}</Tag></>;
}

export function Label({ children, className = "", ...props }: HTMLAttributes<HTMLSpanElement> & { children: ReactNode }) {
  return <span className={["label", className].filter(Boolean).join(" ")} {...props}>{children}</span>;
}
