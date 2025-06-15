FROM node:20-alpine

WORKDIR /app

COPY public ./public
COPY src ./src
COPY package.json ./

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "public", "-l", "3000"]