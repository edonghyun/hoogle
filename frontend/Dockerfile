FROM node:14

WORKDIR /frontend

COPY react .
RUN npm install --silent

CMD PORT=18267 npm run start

EXPOSE 18267
