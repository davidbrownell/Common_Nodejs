/** @type {import("snowpack").SnowpackUserConfig } */
module.exports = {
  extends: "@snowpack/app-scripts-svelte",
  mount: {
    public: "/",
    src: "/_dist_",
  },
  plugins: [
    "@snowpack/plugin-dotenv",
    "@snowpack/plugin-sass",
    "@snowpack/plugin-svelte",
    "@snowpack/plugin-typescript",
    "@snowpack/plugin-webpack",
  ],
  install: [
    /* ... */
  ],
  installOptions: {
    installTypes: true,
    /* ... */
  },
  devOptions: {
    /* ... */
  },
  buildOptions: {
    /* ... */
  },
  proxy: {
    /* ... */
  },
  alias: {
    /* ... */
  },
};
