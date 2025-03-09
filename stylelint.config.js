module.exports = {
    // Extend the standard configuration (you can add more if needed)
    extends: [
      "stylelint-config-standard",
      // Optionally, if you're using Prettier:
      // "stylelint-config-prettier"
    ],
    // Optionally add plugins—for example, for ordering properties
    plugins: [
      "stylelint-order"
    ],
    rules: {
      // Enable the rule, but ignore Tailwind-specific at-rules
      "at-rule-no-unknown": [
        true,
        {
          ignoreAtRules: [
            "tailwind",   // Tailwind's base declarations
            "apply",      // For @apply directives
            "variants",   // For variant generation
            "responsive", // For responsive utilities
            "screen",     // For media queries with Tailwind
            "function",   // If using @function in PostCSS
            "if",         // If using conditional at-rules
            "each",       // For loops in your CSS (if applicable)
            "include",    // For mixins (if using a preprocessor)
            "mixin"       // For defining mixins
          ],
        },
      ],
      // You can add additional custom rules here:
      // e.g., property ordering, no invalid hex colors, etc.
    },
    // If you use SCSS syntax in your CSS files, you may specify custom syntax:
    // customSyntax: "postcss-scss",
  };