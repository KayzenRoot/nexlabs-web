import type { HTMLAttributes, ReactNode } from "react";

export function Container({ children, className = "", size = "content", ...props }: HTMLAttributes<HTMLDivElement> & { children: ReactNode; size?: "content" | "reading" | "wide" }) {
  return <div className={["container", `container-${size}`, className].filter(Boolean).join(" ")} {...props}>{children}</div>;
}

export function Stack({ children, className = "", ...props }: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
  return <div className={["stack", className].filter(Boolean).join(" ")} {...props}>{children}</div>;
}

export function Cluster({ children, className = "", ...props }: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
  return <div className={["cluster", className].filter(Boolean).join(" ")} {...props}>{children}</div>;
}

export function Surface({ children, className = "", as: Tag = "div", ...props }: HTMLAttributes<HTMLDivElement> & { children: ReactNode; as?: "div" | "article" | "aside" }) {
  return <Tag className={["surface", className].filter(Boolean).join(" ")} {...props}>{children}</Tag>;
}

export function Section({ children, className = "", ...props }: HTMLAttributes<HTMLElement> & { children: ReactNode }) {
  return <section className={["section", className].filter(Boolean).join(" ")} {...props}>{children}</section>;
}
