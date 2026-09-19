import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/react";
import { MobileNav } from "@/components/layout/MobileNav";
import { ThemeController } from "@/components/system/ThemeController";
import { VisualSlot } from "@/components/media/VisualSlot";

describe("CP-02 design-system boundaries", () => {
  beforeEach(() => window.localStorage.clear());

  it("keeps mobile navigation keyboard reachable and restores trigger focus", async () => {
    const user = userEvent.setup();
    render(<MobileNav items={[{ label: "Home", href: "/" }]} />);
    const trigger = screen.getByRole("button", { name: "Menu" });
    await user.click(trigger);
    expect(screen.getByRole("navigation", { name: "Mobile primary navigation" })).toBeInTheDocument();
    await user.keyboard("{Escape}");
    expect(trigger).toHaveFocus();
    expect(screen.queryByRole("navigation", { name: "Mobile primary navigation" })).not.toBeInTheDocument();
  });

  it("exposes an explicit theme choice without analytics or page-wide client state", async () => {
    const user = userEvent.setup();
    render(<ThemeController />);
    const select = screen.getByRole("combobox", { name: "Color theme" });
    await user.selectOptions(select, "light");
    expect(document.documentElement.dataset.theme).toBe("light");
    expect(window.localStorage.getItem("nexlabs-theme")).toBe("light");
  });

  it("supports accessible and decorative visual slot modes", () => {
    render(<><VisualSlot /><VisualSlot decorative label="Hidden slot" /></>);
    expect(screen.getByRole("img", { name: "Provisional visual system slot" })).toBeInTheDocument();
    expect(screen.queryByRole("img", { name: "Hidden slot" })).not.toBeInTheDocument();
  });
});
