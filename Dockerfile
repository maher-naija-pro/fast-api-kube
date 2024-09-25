FROM python:3.9.20-slim

# Set environment variables (default is 'dev')
ARG ENVIRONMENT=dev
ENV ENVIRONMENT=$ENVIRONMENT

RUN echo "I'm building for $ENVIRONMENT"

LABEL maintainer="Maher NAIJA <maher.naija@gmail.com>"

WORKDIR /app/

COPY requirements/ /app

# Install Python dependencies
RUN if [ "$ENVIRONMENT" = "prod" ]; then \
  pip install  --no-cache-dir -r /app/prod.txt; \
elif [ "$ENVIRONMENT" = "staging" ]; then \
  pip install  --no-cache-dir -r /app/staging.txt; \
else \
  pip install  --no-cache-dir -r /app/dev.txt; \
fi

COPY ./src /app/

COPY ./scripts/entrypoint.sh /app/

RUN chmod +x  /app/entrypoint.sh

EXPOSE 3000
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
