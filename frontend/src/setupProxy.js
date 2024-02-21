const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/weather',
    createProxyMiddleware({
      target: 'http://ec2-3-76-103-42.eu-central-1.compute.amazonaws.com',
      changeOrigin: true,
    })
  );
};