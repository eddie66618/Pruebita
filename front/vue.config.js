module.exports = {
  /*publicPath: process.env.NODE_ENV === 'production'
    ? '/production-sub-path/'
    : '/',*/
  publicPath: '/hisar/',
  /*outputDir: path.join(__dirname, '/dist/hisar/'),
  indexPath: path.join(__dirname, 'dist/hisar/index.html'),*/
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    proxy: {
      '/APICNSR': {
        target: 'http://10.0.52.64:8000/',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/APICNSR': ''
        }
      },
      '/APICENTRAL': {
        target: 'http://10.56.1.127:9087/',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/APICENTRAL': ''
        }
      },
      '/QALOCAL': {
        target: 'http://10.0.54.88:8050/',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/QALOCAL': ''
        }
      }
    },
    port: 90
  },
}
