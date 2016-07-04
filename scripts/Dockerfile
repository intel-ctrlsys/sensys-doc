FROM jagregory/pandoc

ENV http_proxy=http://proxy-chain.intel.com:911
ENV https_proxy=http://proxy-chain.intel.com:911

RUN apt-get install -y --no-install-recommends --fix-missing lmodern pdftk

ENTRYPOINT ["/bin/sh", "-c"]

CMD []
