import { readFile } from "node:fs/promises";
import { compileCss, compileManifest, compileTypes, cssPath, isThemeValue, manifestPath, readTokenSource, typesPath } from "./token-utils.mjs";

const source = await readTokenSource();
const requiredPrimitiveGroups = ["color", "font", "space", "radius", "border", "shadow", "motion", "zIndex", "breakpoint", "container"];
const requiredSemantic = [
  "surface.page", "surface.primary", "surface.raised", "surface.overlay", "surface.inverse",
  "text.primary", "text.secondary", "text.muted", "text.inverse", "text.link",
  "action.primary", "action.primaryHover", "action.secondary", "action.focus", "action.disabled",
  "signal.primary", "signal.secondary", "signal.rare", "state.success", "state.warning", "state.danger", "state.info",
  "diagram.node", "diagram.edge", "diagram.active", "diagram.label",
];

const errors = [];
if (source.schemaVersion !== 1) errors.push("schemaVersion must be 1");
if (source.status !== "provisional-engineering") errors.push("status must remain provisional-engineering");
for (const group of requiredPrimitiveGroups) if (!source.primitives?.[group]) errors.push(`missing primitive group: ${group}`);
for (const key of requiredSemantic) {
  const value = source.semantic?.[key];
  if (!isThemeValue(value) || !value.dark || !value.light) errors.push(`semantic token must have dark/light values: ${key}`);
}

function flatten(value, prefix = []) {
  if (isThemeValue(value) || typeof value !== "object" || value === null || Array.isArray(value)) return [[prefix.join("."), value]];
  return Object.entries(value).flatMap(([key, child]) => flatten(child, [...prefix, key]));
}

const lookup = new Map();
for (const [key, value] of [...flatten(source.primitives), ...Object.entries(source.semantic), ...Object.entries(source.components), ...Object.entries(source.bridge)]) lookup.set(key, value);

function resolve(value, theme, seen = new Set()) {
  if (isThemeValue(value)) return resolve(value[theme], theme, seen);
  if (typeof value !== "string") return value;
  const match = value.match(/^\{(.+)\}$/);
  if (!match) return value;
  if (seen.has(match[1])) throw new Error(`cyclic token reference: ${match[1]}`);
  seen.add(match[1]);
  return resolve(lookup.get(match[1]), theme, seen);
}

function luminance(hex) {
  const normalized = hex.replace("#", "");
  if (!/^[0-9a-f]{6}$/i.test(normalized)) throw new Error(`contrast token is not a six-digit hex color: ${hex}`);
  const channels = [0, 2, 4].map((index) => parseInt(normalized.slice(index, index + 2), 16) / 255).map((channel) => channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4);
  return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
}

function contrast(foreground, background) {
  const a = luminance(foreground);
  const b = luminance(background);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

const contrastPairs = [
  ["text.primary", "surface.page", 4.5],
  ["text.secondary", "surface.page", 4.5],
  ["text.link", "surface.page", 4.5],
  ["button.primary.foreground", "button.primary.background", 4.5],
  ["button.secondary.foreground", "button.secondary.background", 4.5],
];
for (const theme of ["dark", "light"]) {
  for (const [foregroundKey, backgroundKey, minimum] of contrastPairs) {
    try {
      const ratio = contrast(resolve(lookup.get(foregroundKey), theme), resolve(lookup.get(backgroundKey), theme));
      if (ratio < minimum) errors.push(`${theme} contrast ${foregroundKey}/${backgroundKey} is ${ratio.toFixed(2)}; expected >= ${minimum}`);
    } catch (error) {
      errors.push(`${theme} contrast ${foregroundKey}/${backgroundKey}: ${error.message}`);
    }
  }
}

const expected = [
  [cssPath, compileCss(source)],
  [typesPath, compileTypes(source)],
  [manifestPath, compileManifest(source)],
];
for (const [file, contents] of expected) {
  const actual = await readFile(file, "utf8").catch(() => null);
  if (actual !== contents) errors.push(`generated token artifact is stale: ${file}`);
}

if (errors.length > 0) {
  console.error(`Token validation failed:\n- ${errors.join("\n- ")}`);
  process.exitCode = 1;
} else {
  console.log(`Token validation passed: ${requiredSemantic.length} required semantic mappings and dark/light contrast checks are valid.`);
}
