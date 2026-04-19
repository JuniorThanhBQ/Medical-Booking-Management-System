FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
COPY public/ ./public/
COPY src/ ./src/
COPY index.html vite.config.js eslint.config.js ./
RUN npm run build

FROM nginx:1.30-alpine
RUN apk update && apk upgrade --no-cache
RUN apk add --no-cache curl
RUN rm -rf /usr/share/nginx/html/* /etc/nginx/conf.d/*
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder --chmod=555 /app/dist /usr/share/nginx/html
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /var/run/nginx.pid
USER nginx
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]