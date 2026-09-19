import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

const projectRoot = fileURLToPath(new URL("./", import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": projectRoot,
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setup.ts"],
    include: ["tests/**/*.test.{ts,tsx}"],
    css: true,
    pool: "threads",
    // Vitest 5 supports this runtime setting; its published InlineConfig type is behind.
    // @ts-expect-error Vitest 5 singleThread runtime option
    singleThread: true,
    isolate: false,
    fileParallelism: false,
    maxWorkers: 1,
    minWorkers: 1,
    testTimeout: 15000,
  },
});
