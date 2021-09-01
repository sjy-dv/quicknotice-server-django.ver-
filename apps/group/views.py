import bcrypt
import jwt

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
def CreateGroup(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [body['group_name'], decoded['user_id']]
            cursor.execute(
                "insert into group_collection(group_name, manager) values(%s, %s)", arr)
            rows = namedtuplefetchall(cursor)
            arr2 = [rows[0].idx, decoded['user_id']]
            cursor.execute(
                'insert into group_member(group_code, member) values(%s, %s)', arr2)
            return JsonResponse({"result": "success"}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def List(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [decoded['user_id']]
            query = "select * from group_collection inner join group_member " +
            "on group_collection.idx = group_member.group_code " +
            "where group_member.member = %s"
            cursor.execute(query, arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def GroupName(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            arr = [body['idx']]
            cursor.execute(
                'select * from group_collection where idx = %s', arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def GroupList(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            arr = [body['idx']]
            query = "select * from user inner join group_member " +
            "on user.user_id = group_member.member" +
            "where group_member.group_code = %s"
            cursor.execute(query, arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()
