# Theme and motion

The default mode is `system`, with dark-first generated values. `ThemeController` allows `System`, `Dark`, and `Light`, persists only the user's choice under `nexlabs-theme`, and does not collect analytics or fingerprinting data. The root layout includes a small pre-hydration local-storage read to avoid a visible theme flash; the CSP documents that this is the existing inline bootstrap and does not broaden third-party script access.

All theme mappings are explicit in `design/tokens/source.json`. Contrast validation covers primary, secondary, and link text plus primary and secondary actions in both dark and light themes. Focus rings use the semantic focus token.

Motion uses instant, fast, standard, deliberate, system, and reserved cinematic durations plus named easing families. The global reduced-motion rule removes non-essential transitions and animation timing. There is no animation framework and no pointer-critical behavior.
