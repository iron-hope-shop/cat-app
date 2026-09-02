FROM nginx:alpine

# Copy web files
COPY Quarry/www /usr/share/nginx/html

# Copy custom nginx configuration with PWA headers & health checks
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Cloud Run defaults to PORT environment variable (default 8080)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
