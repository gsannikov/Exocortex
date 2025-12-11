import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  safelist: [
    {
      pattern: /(text|from|to)-(emerald|amber|red|rose)-(400|500|700)/,
    },
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

export default config;
