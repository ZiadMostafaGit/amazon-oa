# Amazon OA practice — a static site with an in-browser Python runtime.
#
# Stage 1 fetches CodeMirror, JetBrains Mono and Pyodide and rewrites the two
# files that reference them, so the running container needs no network at all.
# Stage 2 is just nginx serving the result.

FROM alpine:3.20 AS vendor
RUN apk add --no-cache curl
WORKDIR /src
COPY scripts/vendor.sh scripts/
COPY site/   site/
COPY images/ images/
COPY video/  video/
RUN sh scripts/vendor.sh /dist \
 && rm -f /dist/site/_*.html

FROM nginx:1.27-alpine
LABEL org.opencontainers.image.title="Amazon OA practice" \
      org.opencontainers.image.description="41 transcribed Amazon OA problems with worked \
solutions, an in-browser Python editor, and a test runner that executes CPython via Pyodide. \
No backend; works offline." \
      org.opencontainers.image.licenses="NOASSERTION"

COPY --from=vendor /dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- http://127.0.0.1/site/index.html >/dev/null || exit 1
