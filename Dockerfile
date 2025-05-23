FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV TZ=Asia/Bangkok

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update \
    && apt install -y --no-install-recommends \
        curl \
        git \
        locales \
        sudo \
        tar \
        xz-utils \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN sed --in-place '/en_US.UTF-8/s/^#//' /etc/locale.gen  \
    &&  sed --in-place '/th_TH.UTF-8/s/^#//' /etc/locale.gen \
    && locale-gen

# Install ffmpeg static build
RUN ARCH=$(uname -m) \
    && case "$ARCH" in \
        x86_64) FFMPEG_URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz" ;; \
        aarch64) FFMPEG_URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz" ;; \
        *) echo "Unsupported architecture: $ARCH" && exit 1 ;; \
    esac \
    && curl -L "$FFMPEG_URL" | tar -xJ \
    && cp ffmpeg-*-static/ffmpeg /usr/local/bin/ \
    && cp ffmpeg-*-static/ffprobe /usr/local/bin/ \
    && chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe \
    && rm -rf ffmpeg-*-static

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
ENV PROJECT_WORKSPACE=/workspaces/aiforthai-linebot-workshop-space


ARG USERNAME=aiforthai
ARG USER_UID=1000
ARG USER_GID=${USER_UID}


RUN echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME}

USER ${USERNAME}


#ENV VIRTUAL_ENV=${PROJECT_WORKSPACE}/.venv
ENV UV_LINK_MODE=copy

ENV ZSH_CUSTOM=/home/${USERNAME}/.oh-my-zsh/custom
#ENV PATH="${VIRTUAL_ENV}/bin:/home/${USERNAME}/.local/share/uv/tools:${PATH}"
ENV PATH="/home/${USERNAME}/.local/share/uv/tools:${PATH}"

#WORKDIR ${PROJECT_WORKSPACE}

#ENV PYTHONPATH=${PROJECT_WORKSPACE}/app

EXPOSE 8000
