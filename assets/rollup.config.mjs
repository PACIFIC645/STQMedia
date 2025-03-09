import path from "path";
import { fileURLToPath } from "url";
import resolvePlugin from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import terser from "@rollup/plugin-terser";
import postcss from "rollup-plugin-postcss";
import { defineConfig } from "rollup";

// Setup __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const isProduction = process.env.NODE_ENV === "production"; // Determine build mode

export default defineConfig({
  input: path.resolve(__dirname, "../stqpictures/static/stqpictures/js/main.js"), // ✅ Ensure input path is correct
  output: {
    file: path.resolve(__dirname, "../theme/static_src/dist/bundle.js"), // ✅ Verify output path
    format: "iife", // Immediate Invoked Function Expression for browser use
    name: "Bundle", // Global variable name for the IIFE
    sourcemap: true, // Enable sourcemaps for debugging
    globals: {
      swiper: "Swiper",
      "swiper/modules": "SwiperModules",
      gsap: "gsap", // External modules referenced as globals
    },
  },
  external: ["swiper", "swiper/modules", "gsap"], // External libraries excluded from the bundle
  plugins: [
    resolvePlugin(), // Resolves `node_modules` dependencies
    commonjs(), // Converts CommonJS modules to ES modules
    postcss({
      extract: true, // ✅ Output CSS as a separate file
      modules: false, // Avoid treating CSS as modules unless needed
      autoModules: true, // Automatically enable CSS modules when filename matches *.module.*
      use: ["sass"], // ✅ Process SCSS files
    }),
    isProduction &&
      terser({
        compress: { drop_console: true }, // ✅ Removes console.logs in production
        mangle: true, // Obfuscates variable names
      }),
  ].filter(Boolean), // Remove `false` values (like `isProduction` in development mode)
});
