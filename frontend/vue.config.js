// vue.config.js
module.exports = {
  devServer: {
    allowedHosts: "all",
    proxy: {
      '^/flask-api': {
        target: 'http://backend:5000',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/flask-api': '/'
        }
      }
    }
  },

  transpileDependencies: true
}
