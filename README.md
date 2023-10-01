# Django-project
Django-project

# Run this Project
git checkout master
pip install -r requirements.txt
/env/Scripts/activate
cd .\movie_api\
python manage.py migrate
python manage.py runserver




# API

Token Generation

curl --location --request GET 'http://localhost:8000/token/generateToken' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"******@gmail.com",
    "secret_key":"ksefwefjlemvDRC$%"
}'


Movie List

curl --location 'http://localhost:8000/api/movies' \
--header 'Authorization: Bearer <Token>'

-----------------------------

curl --location 'http://localhost:8000/api/movies/10' \
--header 'Authorization: Bearer <Token>'

---------------------

POST /api/movies HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer <Token>
Content-Length: 168

{
    "original_title":"title",
    "overview":"overview",
    "release_date":"2021-01-01",
    "title":"title",
    "genre":"genre",
    "director":"director"
}


-----------------------------------------------

PUT /api/movies/1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer <Token>
Content-Length: 31

{
    "title":"Toy Story 1"
}


----------------------------------------------


DELETE /api/movies/1 HTTP/1.1
Host: localhost:8000


------------------------------------------------


GET /api/movies HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer <Token>
Content-Length: 38

{
    "rowCount":20,
    "page":2
}



-------------------------------------------------------------


