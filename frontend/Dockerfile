FROM node:10.16.3-alpine

WORKDIR /app

COPY package.json ./
COPY yarn.lock ./

RUN yarn

COPY . ./

RUN yarn build

CMD ["yarn", "start"]
