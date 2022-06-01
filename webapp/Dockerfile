FROM node:16

RUN npm install -g serve

COPY chatapp .

RUN npm install
RUN npm run build

CMD serve -s build
