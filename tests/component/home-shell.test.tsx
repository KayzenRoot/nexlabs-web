import { render, screen } from "@testing-library/react";
import { HomeShell } from "@/components/sections/HomeShell";

describe("home semantic shell", () => {
  it("renders factual NexLabs and HIVE content", () => {
    render(<HomeShell />);
    expect(screen.getByRole("heading", { name: /Build with AI/i })).toBeInTheDocument();
    expect(screen.getByText(/NexLabs builds developer infrastructure/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Explore HIVE/i })).toHaveAttribute("href", "https://github.com/KayzenRoot/hive");
  });
});
