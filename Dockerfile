FROM ubuntu:22.04

RUN apt update && apt install bash curl gpg systemd -y

ENV MSSQL_PASSWORD p@ssw0rd!
ENV MSSQL_PID developer

# RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc

RUN curl -fsSL https://packages.microsoft.com/config/ubuntu/22.04/mssql-server-2022.list | tee /etc/apt/sources.list.d/mssql-server-2022.list

RUN apt update && apt install mssql-server -y

# RUN MSSQL_SA_PASSWORD=${MSSQL_PASSWORD} \
#     MSSQL_PID=${MSSQL_PID} \
#     /opt/mssql/bin/mssql-conf -n setup accept-eula
# MSSQL_SA_PASSWORD=p@ssw0rd! MSSQL_PID=developer /opt/mssql/bin/mssql-conf -n setup accept-eula
# RUN ACCEPT_EULA=Y apt install -y mssql-tools unixodbc-dev

# RUN PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bash_profile

# RUN source ~/.bashrc


ENTRYPOINT [ "/bin/bash" ]