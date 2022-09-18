docker build -t dash .
docker run --rm --name dash -p 8050:8050 dash
docker run -d --name dash -p 8050:8050 dash

docker run --rm --gpus 'device=0' --name dash -p 8000:8000 dash
docker run -it -d --gpus 'device=0' --name dash -p 8000:8000 dash


docker run -e MY_PASS='8nNcZVs' -e MY_USER='postgres' -e MY_BD='parser' -e MY_HOST='51.250.84.80' -e MY_PORT=32345 --rm --gpus 'device=0' --name dashly -p 8050:8050 dash

docker exec -it <container_id> bash

RUN apt-get install nvidia-container-runtime

docker kill $(docker ps -a -q) 
docker rm $(docker ps -a -q)  
docker rmi $(docker images -a -q)

sudo chmod 666 /var/run/docker.sock

docker login http://docker-ici-cyrm.fdi.group:443
ici
cyrmE3r1x5a1J

docker tag dash docker-ici-cyrm.fdi.group:443/dash:270522
docker push docker-ici-cyrm.fdi.group:443/dash:270522

dbname='parser', user='postgres', password='8nNcZVs', host='51.250.84.80', port=32345

