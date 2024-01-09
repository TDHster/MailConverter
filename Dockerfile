FROM x11docker/lxde-wine
#FROM x11docker/xserver


RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

COPY API /app/API
COPY MailConverter /app/MailConverter

#COPY mail.eml .

#RUN wine 15-MailConverterX.32.exe  mail.eml  mail.eml.pdf

#RUN ls -lah

#CMD ["MailConverterProX.exe", "mail.eml", "mail.eml.pdf", "-c", "PDF"]

# Expose port 8000 from the container
EXPOSE 8000

#CMD ["/bin/bash"]
CMD ["uvicorn", "API.mailconverter-api:app"]





#CMD ["CoolUtils/TotalMailConverterProX/MailConverterProX.exe", "mail.eml", "mail.eml.pdf", "-c", "PDF"]
