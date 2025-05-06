FROM ubuntu:latest
LABEL authors="akbaralizonov"

ENTRYPOINT ["top", "-b"]