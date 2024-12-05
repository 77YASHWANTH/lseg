FROM amazonlinux:2

RUN yum update -y && \
    yum install -y \
    aws-cli \
    bash \
    && yum clean all

RUN mkdir -p /app/stockdata

COPY stockdata.sh /app/stockdata.sh

RUN chmod +x /app/stockdata.sh

# Set the default entrypoint to run the script
ENTRYPOINT ["/app/stockdata.sh"]
