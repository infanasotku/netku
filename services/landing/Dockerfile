FROM node:lts-alpine

WORKDIR /app

COPY package.json .
RUN npm install

ADD . .

CMD ["npx", "vite", "build", "."]
