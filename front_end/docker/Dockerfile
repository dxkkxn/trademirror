FROM node:20-bookworm
WORKDIR /home/app
EXPOSE 4500
COPY package.json package-lock.json ./
RUN npm i
COPY . ./
CMD ["npm", "run", "dev"]
