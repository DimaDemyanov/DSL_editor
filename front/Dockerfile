FROM node:13.12.0-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY .env.production ./
COPY .env ./

ADD src ./src
ADD public ./public

RUN npm install --silent
RUN npm install -g serve
RUN npm run build

EXPOSE 3000

CMD ["serve", "-s", "build"]