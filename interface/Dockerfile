# Build stage
FROM node:18-alpine AS build
WORKDIR /src

COPY interface/package*.json ./
RUN npm ci --silent
COPY interface/ .
# Make sure interface/.env exists (REACT_APP_* values) before build
RUN npm run build

# Production stage: nginx
FROM nginx:alpine
COPY --from=build /src/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]