# This is Mogul Open Sourced

BTW best if done in a virtualenv

`pip install -r requirements.txt`

Adjust settings.py in mogul_os if needed. It should mostly work out of the box.. no promises though

`cd frontend`, `npm install`

run `docker-compose up` on a second terminal tab

dont use these anymore, use docker-compose
~~Some docker containers are needed:
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
docker run -d --name=mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mogul -e MYSQL_DATABASE=mogul_os  -e MYSQL_USER=mogul_os -e MYSQL_PASSWORD=mogul_os mysql/mysql-server:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci~~

Go back to main folder, run:
`./manage.py migrate`
`./manage.py eveuniverse_load_data map`
`./manage.py eveuniverse_load_data ships`
`./manage.py eveuniverse_load_data structures`
`./manage.py mogulos_backend_load_types`

This builds up the database

For development:
`cd frontend/` & `npm run serve`
`./manage.py runserver`

Run celery + celerybeat with watchdog:
`watchmedo auto-restart --directory="." --recursive -- celery -A mogul_os worker --beat --scheduler django --loglevel=info`

Now you should have frontend running on :3000 and backend on :8000.

Go ahead and create a superuser
`./manage.py createsuperuser`
Access admin page at: [http://localhost:8000/admin](http://localhost:8000/admin)
Access frontend at: [http://localhost:3000](http://localhost:3000)