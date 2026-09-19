import { mkdir, writeFile } from "node:fs/promises";
import { compileCss, compileManifest, compileTypes, cssPath, manifestPath, readTokenSource, typesPath } from "./token-utils.mjs";

const source = await readTokenSource();
await mkdir(new URL("../design/tokens/", import.meta.url), { recursive: true });
await mkdir(new URL("../public/brand/", import.meta.url), { recursive: true });
await writeFile(cssPath, compileCss(source));
await writeFile(typesPath, compileTypes(source));
await writeFile(manifestPath, compileManifest(source));
console.log("Design tokens generated: CSS, TypeScript names and public bridge manifest.");
