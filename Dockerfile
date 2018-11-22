# This file is meant to be published as adv-base image

FROM python:3.7-alpine as build

ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apk add --no-cache \
    nodejs \
    nodejs-npm  \
    bash \
    git \
    openssh \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    build-base && \
    mkdir -p /build/wheels

# Install python requirements, collect as wheels and re-install
# later on in the `production` stage
COPY ./requirements.txt /build/wheels/
WORKDIR /build/wheels
RUN pip install -U pip && \
    pip wheel -r requirements.txt

# Install node-based requirements
WORKDIR /build
COPY ./package.json ./
RUN npm install

# Copy assets and build static file bundles
COPY ./webpack.config.js ./
COPY ./assets/ ./assets/
RUN ./node_modules/.bin/webpack --config webpack.config.js --mode production


FROM python:3.7-alpine as production

ENV PYTHONPATH /socialsystem
ENV DJANGO_SETTINGS_MODULE socialsystem.settings
ENV PATH "/home/socialsystem/.local/bin:${PATH}"

# Create custom user to avoid running as a root
RUN addgroup -g 1001 socialsystem && \
    adduser -D -u 1001 -G socialsystem socialsystem && \
    mkdir /socialsystem && \
    chown socialsystem:socialsystem /socialsystem

# Install dependencies
RUN apk add --no-cache \
    bash \
    postgresql-dev \
    build-base \
    jpeg-dev \
    zlib-dev \
    nginx \
    supervisor && \
    rm /etc/nginx/conf.d/default.conf && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    mkdir /run/nginx

# Supervisor and Nginx configs
COPY ./docker/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY ./docker/nginx.conf /etc/nginx/conf.d/socialsystem.conf

# Copy over collected wheels and build artifacts from build stage
COPY --from=build --chown=socialsystem /build/wheels /wheels
COPY --from=build --chown=socialsystem /build/assets /socialsystem/assets
COPY --from=build --chown=socialsystem /build/webpack-stats.json /socialsystem/

# Copy over entrypoint file
COPY --chown=socialsystem docker/entrypoint.sh /socialsystem/

USER socialsystem
WORKDIR /socialsystem

# Install wheels under user priviledges
RUN pip install -r /wheels/requirements.txt -f /wheels --user

# Rest of source files
COPY --chown=socialsystem ./socialsystem ./socialsystem/

# Collect static files
RUN mkdir /socialsystem/static && \
    DEBUG=1 django-admin collectstatic --noinput --verbosity=0

USER root

# Get rid of useless files
RUN rm -rf /wheels && \
    rm -rf /home/socialsystem/.cache/pip

EXPOSE 80

CMD ["sh", "./entrypoint.sh"]
