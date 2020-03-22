const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "development",
  entry: { 
    app: "./src/main/index.js",
    "editor.worker": "monaco-editor/min/vs/editor/editor.worker.js",
    "json.worker": "monaco-editor/min/vs/language/json/json.worker",
    "css.worker": "monaco-editor/min/vs/language/css/css.worker",
    "html.worker": "monaco-editor/min/vs/language/html/html.worker",
    "ts.worker": "monaco-editor/min/vs/language/typescript/ts.worker"
  },
  resolve: {
    extensions: [".ts", ".js"]
  },
  // target: 'electron', // can also be -renderer or electron main (based on https://github.com/webpack/webpack/issues/3012)
  output: {
    globalObject: "self",
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "dist")
  },
  module: {
    rules: [
      {
        test: /\.ts?$/,
        use: "ts-loader",
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: ['file-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
        title: "Figure Generator"
      })
  ]
};