import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

import { fileURLToPath, URL } from "url";
import { createHash } from "crypto";
import fs from "fs";
import path from "path";

const getHash = (distDir: string) => {
  const files = fs.readdirSync(distDir);
  const hash = createHash("sha256");

  files.sort();
  for (const file of files) {
    const filePath = path.join(distDir, file);

    if (fs.statSync(filePath).isFile()) {
      const fileContent = fs.readFileSync(filePath);
      hash.update(fileContent);
    }
  }

  return hash.digest("hex");
};

export default defineConfig(() => {
  const hash = getHash(path.resolve(process.cwd(), ".")).slice(1, 16);

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    define: {
      __BUILD_VERSION__: `"${hash}"`,
    },
    server: {
      host: "0.0.0.0",
      port: 5001,
    },
    envDir: "../../",
    css: {
      preprocessorOptions: {
        scss: {
          api: "modern-compiler",
          quietDeps: true,
          silenceDeprecations: ["import"],
          additionalData: `@import "@/assets/scss/_variables.scss";@import "@/assets/scss/_mixins.scss";`,
        },
      },
    },
  };
});
