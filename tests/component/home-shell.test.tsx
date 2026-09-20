import { render, screen } from "@testing-library/react";
import { HomeShell } from "@/components/sections/HomeShell";

describe("home semantic shell", () => {
  it("renders factual NexLabs and HIVE content", () => {
    render(<HomeShell />);
    expect(screen.getByRole("heading", { name: /Infrastructure for AI-native software/i })).toBeInTheDocument();
    expect(screen.getByText(/NexLabs builds developer infrastructure/i)).toBeInTheDocument();
    expect(screen.getAllByRole("link", { name: /Explore HIVE/i }).some((link) => link.getAttribute("href") === "https://github.com/KayzenRoot/hive")).toBe(true);
    expect(screen.getByRole("heading", { name: /More intelligence does not automatically create more continuity/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /Systems around intelligence/i })).toBeInTheDocument();
  });
});
