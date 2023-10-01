import datetime
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST, require_GET, require_safe
from rest_framework.decorators import api_view
from movie_api.model.helper import encode, decode
from movie_api.model.dbconnection import mysql_select, mysql_insert, mysql_update

import jwt
import json
# using time module
import time

# Opening JSON file
# f = open('app/helperModel/config.json')
  
# returns JSON object as 
# a dictionary
# config = json.load(f)

def is_authorization(get_response, id = None):
    # One-time configuration and initialization.

    def Authentication(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        try:
            if request.headers['Authorization']:
                resp_token = decode(request.headers['Authorization'].split()[1])
                if resp_token['email'] : 
                    response = get_response(request)
                    return response
                else:
                    return None
            else: 
                return None
            
        except Exception as e:
            return e

    return Authentication

# def middle_ware(headers):
#     try:
#         if headers['Authorization']:
#             return True
#         else: 
#             raise Exception("Server Error. Access not authorized for app.")
        
#     except Exception as e:
#         return JsonResponse({'message': 'Server Error. Access not authorized for app.' + e}, status=429)
    


@csrf_exempt
@require_GET
@require_safe
def generateToken(request):
    try:
        req_data = request.body.decode('utf-8')
        json_req = json.loads(req_data)
        bear_token = encode(json_req)
        data = {
            'token' : bear_token
        }
        return JsonResponse(data, status=200)
    except (jwt.DecodeError, KeyError):
        return JsonResponse({'message': 'Server Error. Access not authorized for app.' + KeyError}, status=429)
    

@csrf_exempt
@api_view(['GET','POST'])
@is_authorization
def getMovieList(request):
    try: 
        if request.method == 'GET':
            query = 'SELECT id, title, release_date, genre, director FROM movie.movies_metadata;'
            val = ()
            try:
                req_data = request.body.decode('utf-8')
                json_req = json.loads(req_data)
                print((json_req['page'] - 1) * json_req['rowCount'] )
                if json_req['rowCount'] and json_req['page']:
                    countdata = (json_req['page'] - 1) * json_req['rowCount']
                    query = 'SELECT id, title, release_date, genre, director FROM movie.movies_metadata LIMIT %s, %s;'
                    val = (countdata, json_req['rowCount'])
            except Exception as e:
                print(e)

            data = mysql_select(query, val)
            response = {
                'message':'Success',
                'status':200,
                'data':data
            }
            return JsonResponse(response, status=200)
        elif request.method == 'POST':
            req_data = request.body.decode('utf-8')
            json_req = json.loads(req_data)
            if json_req['original_title'] and json_req['overview'] and json_req['release_date'] and json_req['title'] and json_req['genre'] and json_req['director']:
                date_format = '%Y-%m-%d'

                # using try-except blocks for handling the exceptions
                try:
                    dateObject = datetime.datetime.strptime(json_req['release_date'] , date_format)
                    query = "INSERT INTO movies_metadata (original_title, overview, release_date, title, genre, director) VALUES (%s, %s, %s, %s, %s, %s);"
                    val = (json_req['original_title'] , json_req['overview'] , json_req['release_date'] , json_req['title'] , json_req['genre'] , json_req['director'] )
                    data = mysql_insert(query, val)
                    response = {
                        'message':'Success',
                        'status':200,
                        'data':data
                    }
                    return JsonResponse(response, status=200)
                except ValueError:
                    # printing the appropriate text if ValueError occurs
                    raise Exception("Validation Error")

            else:
                return JsonResponse({'message': 'Internal Server Error / Parameter Missing'}, status=402)
    except Exception as e:
        return JsonResponse({'message': 'Server Error..' + str(e)}, status=429)
    

@csrf_exempt
@api_view(['GET','PUT','DELETE']) 
def getMovieById(request, id):
    try:
        if request.method == 'GET':
            query = 'SELECT id, title, release_date FROM movie.movies_metadata where id = ' + id + ';'
            data = mysql_select(query)
            response = {
                'message':'Success',
                'status':200,
                'data':data
            }
            return JsonResponse(response, status=200)
        elif request.method == 'PUT':
            req_data = request.body.decode('utf-8')
            json_req = json.loads(req_data)
            if json_req['title']:
                query = "UPDATE movies_metadata SET title = '" + json_req['title'] + "' WHERE id = " + id +  ";"
                data = mysql_update(query)
                response = {
                    'message':'Success',
                    'status':200,
                    'data':data
                }
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'message': 'Internal Server Error / Parameter Missing'}, status=402)
        elif request.method == 'DELETE':
            query = 'DELETE FROM movie.movies_metadata where id = ' + id + ';'
            data = mysql_update(query)
            response = {
                'message':'Success',
                'status':200,
                'data':data
            }
            return JsonResponse(response, status=200)
    except Exception as e:
        return JsonResponse({'message': 'Server Error..' + str(e)}, status=429)
    



