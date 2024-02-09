module.exports = {
    env: {
      node: true,
    },
    extends: [
      'eslint:recommended',
      "plugin:vue/vue3-recommended"
    ],
    rules: {
      // override/add rules settings here, such as:
      // 'vue/no-unused-vars': 'error'
  
      // these rules should allow console and debugger in development, but warn in production
      "no-console": 1,
      "no-debugger": 1
    }
  }