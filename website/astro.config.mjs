// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import tailwindcss from "@tailwindcss/vite";
import { viteStaticCopy } from "vite-plugin-static-copy";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const pyodideDir = dirname(fileURLToPath(import.meta.resolve("pyodide")));

export default defineConfig({
  site: "https://arkadii-semenov.github.io",
  base: "/python_training",
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
  vite: {
    logLevel: "error",
    plugins: [
      // @ts-expect-error Tailwind's Vite peer currently resolves a different Vite type version.
      tailwindcss(),
      // @ts-ignore Static copy targets Vite 6 while the package types resolve Vite 7.
      viteStaticCopy({
        targets: [{
          src: [join(pyodideDir, "*"), "!**/*.{md,html}", "!**/*.d.ts", "!**/*.whl"],
          dest: "assets",
        }],
      }),
    ],
    optimizeDeps: { exclude: ["pyodide"] },
    worker: { format: "es" },
  },
});
