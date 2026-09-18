# FastPrep practice — 3,533 reported interview problems, an editor, and a
# sandboxed runner, served from one small Python process.
#
# The problem bank is baked in (fastprep/fastprep.db, ~17 MB), so the container
# needs no network at all unless you ask it to fetch source screenshots.

FROM python:3.12-alpine

LABEL org.opencontainers.image.title="FastPrep practice" \
      org.opencontainers.image.description="Browse, filter and solve 3,533 reported \
interview problems offline: rendered statements, source screenshots, a Python/SQL editor \
with Vim keys, and a test runner that executes your code in a bubblewrap sandbox."

# bubblewrap is what isolates user code. Without it the app still runs, but it
# says so on startup and falls back to resource limits only.
RUN apk add --no-cache bubblewrap

WORKDIR /app
COPY fastprep/practice/ /app/practice/
COPY fastprep/fastprep.py /app/fastprep.py
COPY fastprep/fastprep.db /app/fastprep.db

# progress.db, the image cache and any solutions you add live here
VOLUME /data
ENV FP_DATA=/data
# Set FP_BASE_PATH (e.g. /site) only if a reverse proxy forwards its mount
# prefix verbatim; serve.py reads it and strips the prefix from every route.
ENV FP_BASE_PATH=""

EXPOSE 8900
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD wget -qO- http://127.0.0.1:8900/api/health >/dev/null || exit 1

WORKDIR /app/practice
CMD ["python", "serve.py", "--host", "0.0.0.0", "--port", "8900", \
     "--progress-db", "/data/progress.db", "--image-cache", "/data/images"]
