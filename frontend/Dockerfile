FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./

RUN npm install --legacy-peer-deps # or npm ci

COPY . .

RUN npm run build

FROM alpine:latest

COPY --from=builder /app/build /var/www/frontend