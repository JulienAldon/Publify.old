module.exports = {
  devServer: {
      disableHostCheck: true,
      proxy: 'http://127.0.0.1:2000',
      // port: 4000,
      public: 'front.localhost',
      sockHost: 'front.localhost'
  },
  // publicPath: "/"
}