import type { ButtonHTMLAttributes, HTMLAttributes, ReactNode } from "react";

export function Button({ children, className = "", variant = "secondary", ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { children: ReactNode; variant?: "primary" | "secondary" }) {
  return <button className={["action", `action-${variant}`, className].filter(Boolean).join(" ")} {...props}>{children}</button>;
}

export function Badge({ children, className = "", ...props }: HTMLAttributes<HTMLSpanElement> & { children: ReactNode }) {
  return <span className={["badge", className].filter(Boolean).join(" ")} {...props}>{children}</span>;
}

export function Divider({ className = "", ...props }: HTMLAttributes<HTMLHRElement>) {
  return <hr className={["divider", className].filter(Boolean).join(" ")} {...props} />;
}

export function Grid({ children, className = "", ...props }: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
  return <div className={["grid", className].filter(Boolean).join(" ")} {...props}>{children}</div>;
}
