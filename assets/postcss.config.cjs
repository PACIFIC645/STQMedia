module.exports = {
  plugins: [
    require("postcss-import"),
    require("autoprefixer"),
    require('postcss-url')({
      url: 'copy', // Or use 'inline' if you want to base64 encode images
      assetsPath: '/static/', // Specify the static path
    }), 
  ], 
};
