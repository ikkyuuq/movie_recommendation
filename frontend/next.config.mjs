/** @type {import('next').NextConfig} */

const nextConfig = {
  env: {
    BASE_URL: process.env.BASE_URL,
    MOVIE_URL: process.env.MOVIE_URL,
    LIKE_URL: process.env.LIKE_URL,
    FAVOUR_URL: process.env.FAVOUR_URL,
    COMMENT_URL: process.env.COMMENT_URL,
    UPDATEDB_URL: process.env.UPDATEDB_URL,
  },
  images: {
    domains: ["img.clerk.com"],
  },
};

export default nextConfig;
