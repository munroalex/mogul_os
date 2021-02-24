# This is Mogul Open Sourced

BTW best if done in a virtualenv

pip install requirements.txt

Adjust settings.py in mogul_os if needed

Go into frontend, npm install

run `docker-compose up` on a second terminal tab

##dont use these anymore, use docker-compose
Some docker containers are needed:
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
docker run -d --name=mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mogul -e MYSQL_DATABASE=mogul_os  -e MYSQL_USER=mogul_os -e MYSQL_PASSWORD=mogul_os mysql/mysql-server:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

Go back to main folder, run:
./manage.py migrate
./manage.py eveuniverse_load_data map
./manage.py eveuniverse_load_data ships
./manage.py eveuniverse_load_data structures
./manage.py mogulos_backend_load_types


For development:
	cd ./frontend/ & npm run serve
	./manage.py runserver


#database


I will eventually move these to a docker-compose.yml file once I understand how django/python work inside docker