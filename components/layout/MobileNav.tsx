"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { NavigationItem } from "@/lib/content/types";

export function MobileNav({ items }: { items: NavigationItem[] }) {
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const hasOpenedRef = useRef(false);

  useEffect(() => {
    if (open) {
      hasOpenedRef.current = true;
      closeRef.current?.focus();
    } else if (hasOpenedRef.current) {
      triggerRef.current?.focus({ preventScroll: true });
    }
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => { if (event.key === "Escape") setOpen(false); };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [open]);

  return (
    <div className="mobile-nav">
      <button ref={triggerRef} className="menu-trigger" type="button" aria-expanded={open} aria-controls="mobile-navigation" onClick={() => setOpen((value) => !value)}>
        <span>{open ? "Close" : "Menu"}</span>
      </button>
      {open ? <div className="mobile-nav-panel" id="mobile-navigation">
        <button ref={closeRef} className="sr-only" type="button" onClick={() => setOpen(false)}>Close navigation</button>
        <nav aria-label="Mobile primary navigation"><ul className="mobile-nav-list">
          {items.map((item) => <li key={item.href}>{item.external ? <a href={item.href} rel="noreferrer" target="_blank" onClick={() => setOpen(false)}>{item.label}</a> : <Link href={item.href} onClick={() => setOpen(false)}>{item.label}</Link>}</li>)}
          <li><a href="https://github.com/KayzenRoot" rel="noreferrer" target="_blank" onClick={() => setOpen(false)}>GitHub<span className="sr-only"> (opens in a new tab)</span></a></li>
        </ul></nav>
      </div> : null}
    </div>
  );
}
