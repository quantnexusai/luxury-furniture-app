/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    output: 'export',
    distDir: 'build',
    assetPrefix: './',
    images: {
      unoptimized: true,
    },
    webpack: (config) => {
      // Add support for GLB files
      config.module.rules.push({
        test: /\.(glb|gltf)$/,
        use: {
          loader: 'file-loader',
          options: {
            publicPath: '/_next/static/files',
            outputPath: 'static/files',
            name: '[name].[hash].[ext]',
          },
        },
      });
      return config;
    },
  };
  
  module.exports = nextConfig;