FROM node:20-slim
WORKDIR /usr/app
COPY ./ /usr/app
RUN pm install -g @angular/cli
RUN pm install
RUN pm run build
EXPOSE 4200
CMD [ "node", "index.js" ]
