FROM nginx:latest
COPY nginx.conf.template /etc/nginx/conf.d/mysite.template
COPY nginx-entrypoint.sh /nginx-entrypoint.sh
COPY wait-for-it.sh /wait-for-it.sh