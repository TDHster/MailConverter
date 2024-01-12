FROM x11docker/lxde-wine
#FROM x11docker/xserver

#will broke: RUN winecfg
#will broke: RUN winetricks

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

RUN mkdir temp

COPY MailConverter /app/MailConverter

COPY mailconverter-api.py .

HEALTHCHECK --interval=5m --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

EXPOSE 8000

CMD ["uvicorn", "mailconverter-api:app", "--host", "0.0.0.0", "--port", "8000"]
