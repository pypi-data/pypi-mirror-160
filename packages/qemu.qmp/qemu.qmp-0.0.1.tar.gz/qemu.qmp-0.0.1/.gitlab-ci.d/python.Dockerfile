# Python library build & testing environment.

# Fedora is convenient, as it allows us to easily access multiple
# versions of the python interpreter, which is great for tox testing.
FROM fedora:latest

# 「はじめまして！」
MAINTAINER John Snow <jsnow@redhat.com>

# Please keep the packages sorted alphabetically.
RUN dnf --setopt=install_weak_deps=False install -y \
        gcc \
        git \
        make \
        pipenv \
        python3 \
        python3-pip \
        python3-sphinx \
        python3-tox \
        python3-virtualenv \
        python3.10 \
        python3.11 \
        python3.6 \
        python3.7 \
        python3.8 \
        python3.9 \
    && python3 -m pip install --upgrade \
        build \
        pip \
        requests \
        setuptools_scm \
        sphinx-rtd-theme \
        twine \
        xmltodict \
    && dnf clean all \
    && rm -rf ~/.cache/pip \
    && rm -rf /var/cache/dnf \
    ;
