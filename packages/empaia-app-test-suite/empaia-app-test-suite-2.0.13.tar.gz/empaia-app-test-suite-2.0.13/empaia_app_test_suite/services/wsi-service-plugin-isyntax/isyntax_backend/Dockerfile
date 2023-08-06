FROM registry.gitlab.com/empaia/integration/ci-docker-images/test-runner:0.1.31@sha256:d378f2e3f8237d12967b919338f0c9ea1eadc8a1ce2651074ea10a3287cc65ab AS build0

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY isyntax_backend /isyntax/isyntax_backend
COPY pyproject.toml /isyntax/pyproject.toml

WORKDIR /isyntax

RUN python3 -m venv .venv
RUN poetry build

FROM ubuntu:18.04@sha256:478caf1bec1afd54a58435ec681c8755883b7eb843a8630091890130b15a79af

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3-pip python3-wheel unzip

COPY philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip /isyntax/philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip

WORKDIR /isyntax

RUN unzip philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip \
    && cd philips-pathologysdk-2.0-ubuntu18_04_py36_research \
    && chmod 777 InstallPathologySDK.sh \
    && ./InstallPathologySDK.sh py3 -y \
    && cd .. \
    && rm -r philips-pathologysdk-2.0-ubuntu18_04_py36_research

COPY --from=build0 /isyntax/dist/*.whl /tmp
RUN pip3 install /tmp/*.whl

RUN mkdir /data

CMD ["python3", "-m", "isyntax_backend"]
