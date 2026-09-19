import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const sourcePath = path.join(repoRoot, "design", "tokens", "source.json");
export const cssPath = path.join(repoRoot, "design", "tokens", "generated.css");
export const typesPath = path.join(repoRoot, "design", "tokens", "generated.ts");
export const manifestPath = path.join(repoRoot, "public", "brand", "tokens.json");

export async function readTokenSource() {
  return JSON.parse(await readFile(sourcePath, "utf8"));
}

function kebab(value) {
  return value.replace(/([a-z])([A-Z])/g, "$1-$2").replace(/[^a-zA-Z0-9]+/g, "-").replace(/^-|-$/g, "").toLowerCase();
}

export function tokenName(group, key) {
  const prefix = group === "primitive" ? "" : `${kebab(group)}-`;
  return `--nx-${prefix}${key.split(".").map(kebab).join("-")}`;
}

function isThemeValue(value) {
  return value && typeof value === "object" && !Array.isArray(value) && "dark" in value && "light" in value;
}

function collectLeaves(value, prefix = []) {
  const leaves = [];
  if (isThemeValue(value) || typeof value !== "object" || value === null || Array.isArray(value)) {
    leaves.push({ key: prefix.join("."), value });
    return leaves;
  }
  for (const [key, child] of Object.entries(value)) leaves.push(...collectLeaves(child, [...prefix, key]));
  return leaves;
}

function primitiveLeaves(source) {
  return collectLeaves(source.primitives).map(({ key, value }) => ({ group: "primitive", key, value }));
}

function mappedLeaves(source) {
  return [
    ...Object.entries(source.semantic).map(([key, value]) => ({ group: "semantic", key, value })),
    ...Object.entries(source.components).map(([key, value]) => ({ group: "component", key, value })),
    ...Object.entries(source.bridge).map(([key, value]) => ({ group: "bridge", key, value })),
  ];
}

function cssValue(value) {
  if (typeof value !== "string") return String(value);
  const reference = value.match(/^\{(.+)\}$/);
  if (!reference) return value;
  const key = reference[1];
  const first = key.split(".")[0];
  const mappedGroups = new Set(["surface", "text", "action", "signal", "state", "diagram"]);
  const componentGroups = new Set(["button", "nav", "card", "hero"]);
  const group = mappedGroups.has(first) ? "semantic" : componentGroups.has(first) ? "component" : first === "three" ? "bridge" : "primitive";
  return `var(${tokenName(group, key)})`;
}

function declarations(leaves, theme, includeThemeOnly = false) {
  return leaves
    .filter(({ value }) => !includeThemeOnly || isThemeValue(value))
    .map(({ group, key, value }) => {
      const selected = isThemeValue(value) ? value[theme] : value;
      return `  ${tokenName(group, key)}: ${cssValue(selected)};`;
    });
}

function semanticDeclarations(source, theme) {
  return mappedLeaves(source).map(({ group, key, value }) => {
    const selected = isThemeValue(value) ? value[theme] : value;
    return `  ${tokenName(group, key)}: ${cssValue(selected)};`;
  });
}

export function compileCss(source) {
  const leaves = primitiveLeaves(source);
  const constants = declarations(leaves.filter(({ value }) => !isThemeValue(value)), "dark", false);
  const themedPrimitives = leaves.filter(({ value }) => isThemeValue(value));
  const dark = [...declarations(themedPrimitives, "dark", true), ...semanticDeclarations(source, "dark")];
  const light = [...declarations(themedPrimitives, "light", true), ...semanticDeclarations(source, "light")];
  return [
    `/* Generated from design/tokens/source.json. Status: ${source.status}. Do not edit manually. */`,
    ":root {",
    ...constants,
    "}",
    ":root, :root[data-theme=\"dark\"] {",
    ...dark,
    "}",
    ":root[data-theme=\"light\"] {",
    ...light,
    "}",
    "@media (prefers-color-scheme: light) {",
    "  :root:not([data-theme]), :root[data-theme=\"system\"] {",
    ...light.map((line) => `  ${line.trim()}`),
    "  }",
    "}",
    "",
  ].join("\n");
}

export function compileTypes(source) {
  const primitiveNames = primitiveLeaves(source).map(({ key }) => tokenName("primitive", key));
  const semanticNames = mappedLeaves(source).map(({ key, group }) => tokenName(group, key));
  return [
    `// Generated from design/tokens/source.json. Status: ${source.status}. Do not edit manually.`,
    `export const tokenStatus = ${JSON.stringify(source.status)} as const;`,
    `export const primitiveTokenNames = ${JSON.stringify(primitiveNames)} as const;`,
    `export const mappedTokenNames = ${JSON.stringify(semanticNames)} as const;`,
    "export type PrimitiveTokenName = (typeof primitiveTokenNames)[number];",
    "export type MappedTokenName = (typeof mappedTokenNames)[number];",
    "",
  ].join("\n");
}

export function compileManifest(source) {
  return `${JSON.stringify(source, null, 2)}\n`;
}

export { collectLeaves, isThemeValue };
