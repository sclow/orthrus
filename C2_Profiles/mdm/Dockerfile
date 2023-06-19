FROM itsafeaturemythic/mythic_python_base:latest
RUN pip3 install defusedxml
RUN pip3 install sanic==23.3.0
RUN pip3 install requests

RUN apt update && apt install -y unzip wget
#RUN wget https://github.com/micromdm/micromdm/releases/download/v1.8.0/micromdm_v1.8.0.zip && unzip micromdm_v1.8.0.zip && mkdir /pkg
RUN wget https://github.com/micromdm/micromdm/releases/download/v1.11.0/micromdm_v1.11.0.zip && unzip micromdm_v1.11.0.zip && mkdir /pkg

RUN mkdir -p /var/db/micromdm/
RUN mkdir -p /Mythic
RUN touch /Mythic/micromdm.db
RUN ln -s  /Mythic/micromdm.db /var/db/micromdm/micromdm.db

RUN if [ -f /Mythic/mdm/certs/apn.key ] ; then \
	WEBHOOK_PORT=$(grep webhook_port /Mythic/mdm/c2_code/config.json  | cut -d ":" -f 2  | tr -dc 0-9); \
	MYTHIC_MDM_BIND_ADDRESS=$(grep mythic_mdm_bind_address /Mythic/mdm/c2_code/config.json  | cut -d ":" -f 2  | tr -dc 0-9); \
	/build/linux/micromdm serve \
	-server-url=https://localhost \
	-api-key mythic \
	-filerepo /pkg \
	-http-addr :${MYTHIC_MDM_BIND_ADDRESS} \
	-tls-cert /Mythic/mdm/certs/mdm.crt \
	-tls-key /Mythic/mdm/certs/mdm.key \
	-command-webhook-url http://localhost:${WEBHOOK_PORT}/webhook & sleep 1 && \
    /build/linux/mdmctl config set -name c2 -api-token mythic -server-url https://localhost -skip-verify true && \
    /build/linux/mdmctl config switch -name c2 && \
    /build/linux/mdmctl mdmcert upload -cert /Mythic/mdm/certs/apn.pem -private-key /Mythic/mdm/certs/apn.key ; else echo "No APNS Key found" ; fi

WORKDIR /Mythic/

CMD ["python3", "main.py"]