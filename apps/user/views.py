import bcrypt
import jwt

from django.shortcuts import render

# Create your views here.
from django.db.models.query import RawQuerySet
from django.http import request
from django.shortcuts import render
from django.db import connection

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from collections import namedtuple


def namedtuplefetchall(cursor):
    desc = cursor.description
    fields = [col[0] for col in desc]
    nt_result = namedtuple('Result', fields)
    return [nt_result(*row) for row in cursor.fetchall()]


@api_view(['POST'])
def SignUp(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            body['password'] = (bcrypt.hashpw(body['password'].encode(
                'utf-8'), bcrypt.gensalt(8))).decode('utf-8')
            arr = [body['user_id'], body['password'], body['user_name'],
                   body['birth'], body['gender'], body['email']]
            cursor.execute(
                "insert into user(user_id, password, user_name, birth, gender, email) values(%s, %s, %s, %s, %s, %s)", arr)
            return JsonResponse({"result": "success"}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def CheckId(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            cursor.execute(
                'select * from user where user_id = %s LIMIT 1', [body['user_id']])
            rows = namedtuplefetchall(cursor)
            if (!rows[0].user_id):
                return JsonResponse({"result": False}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"result": True}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def SignIn(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            cursor.execute(
                "select * from user where user_id = %s", [body['user_id']])
            rows = namedtuplefetchall(cursor)
            if (bcrypt.checkpw(body['password'].encode('utf-8'), rows[0].password.encode('utf-8'))):
                access_token = jwt.encode(
                    {'user_id': rows[0].user_id}, 'secretkey', algorithm='HS256')
                return JsonResponse({"token": access_token}, status=status.HTTP_200_OK)
            return JsonResponse({"result": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def UserInfo(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            cursor.execute(
                "select * from user where user_id = %s LIMIT 1", [decoded['user_id']])
            rows = namedtuplefetchall(cursor)
            if (rows[0] != None):
                return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
            return JsonResponse({"error": "data is incorrect"}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def MemberInfo(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            cursor.execute(
                "select * from user where user_name=%s LIMIT 1", [body['user_name']])
            rows = namedtuplefetchall(cursor)
            if (rows[0] != None):
                return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
            return JsonResponse({"error": "data is incorrect"}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()
