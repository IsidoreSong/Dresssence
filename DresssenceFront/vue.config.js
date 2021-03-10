module.exports = {
  outputDir: './dist',
  publicPath: './',
  assetsDir: './static',
  devServer: { //跨域
    port: "8080", //端口号
    host: "http://10.206.16.185/",
    open: true, //配置自动启动浏览器
    proxy: { // 配置跨域处理 可以设置多个
      '/colorClassifier': {
        target: 'http://localhost:7999',//跨域请求头信息
        changeOrigin: true,
        ws: false,
        secure: true, // 如果是https接口，需要配置这个参数
        // pathRewrite: {
        //   '^/colorClassifier': '/colorClassifier'
        // }

      }
    }
  }
}