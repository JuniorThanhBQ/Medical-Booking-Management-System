FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY public/ ./public/
COPY src/ ./src/
COPY index.html vite.config.js eslint.config.js .eslintrc.json ./
RUN npm run build

FROM nginx:1.28.2-alpine
RUN apk add --no-cache curl
RUN rm -rf /usr/share/nginx/html/* /etc/nginx/conf.d/*
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder --chmod=555 /app/dist /usr/share/nginx/html
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /var/run/nginx.pid
USER nginx
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]