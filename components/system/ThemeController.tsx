"use client";

import { useEffect, useState } from "react";

export type ThemeMode = "dark" | "light" | "system";
const storageKey = "nexlabs-theme";

export function ThemeController() {
  const [mode, setMode] = useState<ThemeMode>("system");

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const stored = window.localStorage.getItem(storageKey);
      if (stored === "dark" || stored === "light" || stored === "system") setMode(stored);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = mode;
    try { window.localStorage.setItem(storageKey, mode); } catch { /* privacy-safe best effort */ }
  }, [mode]);

  return (
    <label className="theme-control">
      <span className="sr-only">Color theme</span>
      <select aria-label="Color theme" value={mode} onChange={(event) => setMode(event.target.value as ThemeMode)}>
        <option value="system">System</option>
        <option value="dark">Dark</option>
        <option value="light">Light</option>
      </select>
    </label>
  );
}
