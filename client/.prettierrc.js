module.exports = {
  useTabs: false,
  printWidth: 80,
  tabWidth: 2,
  semi: true,
  trailingComma: "none",
  singleQuote: false,
  plugins: [require("prettier-plugin-svelte")],
  overrides: [
    {
      files: "**/*.svx",
      options: { parser: "markdown" }
    },
    {
      files: "**/*.svelte",
      options: { parser: "svelte" }
    },
    {
      files: "**/*.ts",
      options: { parser: "typescript" }
    },
    {
      files: "**/CHANGELOG.md",
      options: {
        requirePragma: true
      }
    }
  ]
};
