import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';
import eslintConfigPrettier from 'eslint-config-prettier';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    files: ['**/*.{ts,tsx,js,jsx}'],
    ignores: ['dist'],
    rules: {
      '@typescript-eslint/no-unused-vars': 'warn',
    },
  },
  eslintConfigPrettier
);
