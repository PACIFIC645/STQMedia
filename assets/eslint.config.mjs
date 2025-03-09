// eslint.config.mjs
import prettierPlugin from "eslint-plugin-prettier";
import prettierConfig from "eslint-config-prettier";

export default [
    {
        files: ["**/*.js"],
        ignores: ["node_modules/**"],
        languageOptions: {
            ecmaVersion: 2021,
            sourceType: "module",
            globals: {
                browser: true
            }
        },
        plugins: {
            prettier: prettierPlugin
        },
        rules: {
            "prettier/prettier": "error" // Enforce Prettier formatting
        }
    }
];
