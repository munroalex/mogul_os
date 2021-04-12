# This is Mogul Open Sourced

BTW best if done in a virtualenv

`pip install -r requirements.txt`

Adjust settings.py in mogul_os if needed. It should mostly work out of the box.. no promises though

run `docker-compose up` on a second terminal tab

`./manage.py migrate`  
`./manage.py eveuniverse_load_data map`  
`./manage.py eveuniverse_load_data ships`  
`./manage.py eveuniverse_load_data structures`  
`./manage.py mogulos_backend_load_types`  
`./manage.py oscar_accounts_init`  

This builds up the database

For development:
`./manage.py runserver`

Run celery + celerybeat:
`celery -A mogul_os worker --beat --scheduler django --loglevel=info`  

Now you should have frontend running on :3000 and backend on :8000.

Go ahead and create a superuser
Login here: [http://localhost:8000/login](http://localhost:8000/login)
run `./manage.py mogulos_backend_superuser` to upgrade your first login to a superuser
Access admin page at: [http://localhost:8000/admin](http://localhost:8000/admin)

To try out the discord stuff, create a bot add it to a test guild and add the details into django admin



Initial URLs
Add character token: [http://localhost:8000/link/trade_character](http://localhost:8000/link/trade_character)  
Add corp token token: [http://localhost:8000/link/trade_corp](http://localhost:8000/link/trade_corp)  
REst API: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)  
Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  
