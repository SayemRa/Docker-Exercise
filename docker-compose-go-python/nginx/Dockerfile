FROM nginx:1.19-alpine
RUN apk add --no-cache apache2-utils
WORKDIR /
COPY nginx.conf nginx.conf
COPY run.sh ./
RUN chmod 0755 ./run.sh
CMD [ "./run.sh" ]