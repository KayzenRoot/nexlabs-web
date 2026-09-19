import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/react";
import { SiteHeader } from "@/components/layout/SiteHeader";
import { SkipLink } from "@/components/layout/SkipLink";

describe("accessibility foundation", () => {
  it("provides a keyboard-reachable skip link and labeled navigation", async () => {
    const user = userEvent.setup();
    render(<><SkipLink /><SiteHeader /></>);
    await user.tab();
    expect(screen.getByRole("link", { name: "Skip to content" })).toHaveFocus();
    expect(screen.getByRole("navigation", { name: "Primary navigation" })).toBeInTheDocument();
  });
});
