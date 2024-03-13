// vue.config.js
module.exports = {
  configureWebpack : {
    devtool: 'source-map',
    entry: "./src/main.js",
    devServer: {
        allowedHosts: 'all',
        proxy: {
          '^/flask-api': {
            target: 'http://backend:5000',
            ws: true,
            changeOrigin: true,
            pathRewrite: {
              '^/flask-api': '/'
            }
          }
        },
        // hot reload windows issue https://stackoverflow.com/questions/71817054/dockerized-vue-app-hot-reload-does-not-work
        hot: true
    },
    watch: true,
    watchOptions: {
        ignored: /node_modules/,
        poll: 1000,
    },
  },
  transpileDependencies: true
}
