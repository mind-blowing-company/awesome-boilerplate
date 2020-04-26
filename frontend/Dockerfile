FROM node:10.16.3-alpine

WORKDIR /app

COPY --chown=1000:1000 . /app

RUN \
 yarn &&\
 yarn build &&\
 chown 1000:1000 -R /app

USER 1000

EXPOSE 3000
ENTRYPOINT [ "yarn" ]
CMD [ "start" ]
