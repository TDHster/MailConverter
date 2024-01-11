FROM x11docker/lxde-wine
#FROM x11docker/xserver

#will broke: RUN winecfg
#RUN winetricks

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

#ENV DISPLAY=:0
#ENV WINEARCH=win32

RUN mkdir temp
# COPY API /app/API
COPY MailConverter /app/MailConverter

COPY mailconverter-api.py .

#RUN wine /app/MailConverter/15-MailConverterX.32.exe  /app/MailConverter/mail.eml  /app/MailConverter/mail.eml.pdf
#RUN wine /app/MailConverter/15-MailConverterX.32.exe /app/MailConverter/mail.eml /app/MailConverter/mail.eml.pdf > /tmp/wine_output.log 2>&1
#RUN wine 15-MailConverterX.32.exe  mail.eml  mail.eml.pdf

#CMD ["MailConverterProX.exe", "mail.eml", "mail.eml.pdf", "-c", "PDF"]

# Expose port 8000 from the container
EXPOSE 8000

# CMD ["/bin/bash"]
#uvicorn API.mailconverter-api:app --host 0.0.0.0 --port 8000
# CMD ["uvicorn", "API.mailconverter-api:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "mailconverter-api:app", "--host", "0.0.0.0", "--port", "8000"]
# uvicorn mailconverter-api:app --host 0.0.0.0 --port 8000 --reload
