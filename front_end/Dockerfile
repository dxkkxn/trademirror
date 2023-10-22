FROM node:20-bookworm
WORKDIR /home/app
EXPOSE 4500
COPY ./front_end/package.json ./front_end/package-lock.json ./
RUN npm i
COPY ./front_end ./
CMD ["npm", "run", "dev"]
