<<<<<<< HEAD
FROM node:20-alpine

WORKDIR /app

COPY public ./public
COPY src ./src
COPY package.json ./
=======
FROM node:20-alpine AS build

WORKDIR /app
COPY . .
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4

RUN npm install -g serve

EXPOSE 3000
<<<<<<< HEAD

=======
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4
CMD ["serve", "public", "-l", "3000"]