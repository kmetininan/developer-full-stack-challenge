FROM node:16.16

WORKDIR /app

RUN apt update && apt upgrade -y

COPY package.json .
COPY package-lock.json .

RUN npm install

RUN npm run generate

COPY . .

EXPOSE 3000

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

CMD [ "npm", "start" ]
