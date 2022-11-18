// vue.config.js
module.exports = {
  devServer: {
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
  }
  // css: {
  //   loaderOptions: {
  //     sass: {
  //       additionalData: '@import "./src/scss/custom.scss";'
  //     }
  //   }
  // }
}
