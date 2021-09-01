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
def Write(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            cursor.execute(
                "select * from user where user_id=%s LIMIT 1", [decoded['user_id']])
            rows = namedtuplefetchall(cursor)
            arr = [body['title'], body['desc'], decoded['user_id'], 0,
                   body['group_idx'], body['notice'], rows[0].user_name]
            cursor.execute(
                "insert into board(title, desc, user_id, visit_count, group_idx, notice,writer) values(%s,%s,%s,%s,%s,%s,%s", arr)
            return JsonResponse({"result": True})
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def BoardList(request):
    with connection.cursor() as cursor:
        try:
            page = request.GET.get('page', None)
            body = JSONParser().parse(request)
            limit = 7
            offset = 0
            if (page > 1):
                offset = (page - 1) * limit
            arr = [body['group_idx'], limit, offset]
            cursor.execute(
                "select * from board where group_idx = %s limit %s offset %s", arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def BoardNoticeList(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            arr = [body['group_idx'], 'on']
            cursor.execute(
                "select * from board where group_idx = %s and notice=%s", arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def BoardDetail(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            arr = [body['idx'], body['group_idx']]
            cursor.execute(
                "select * from board where idx = %s, group_idx = %s LIMIT 1", arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def BoardUpdate(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [body['title'], body['desc'], body['notice'],
                   body['idx'], decoded['user_id']]
            cursor.execute(
                "update board set title=%s, desc=%s, notice=%s where idx=%s and user_id=%s", arr)
            return JsonResponse({"result": True}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def BoardDelete(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [body['idx'], decoded['user_id']]
            cursor.execute(
                'delete from board where idx=%s and user_id=%s', arr)
            return JsonResponse({"result": True}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def WriteComment(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=['HS256'])
            arr = [body['idx'], decoded['user_id'],
                   body['comment'], body['user_name']]
            cursor.execute(
                "insert into board_comment(b_idx, user_id, content, user_name) values(%s, %s, %s, %s)", arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def CommentList(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            cursor.execute(
                "select * from board_comment where b_idx=%s", [body['idx']])
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def CommentUpdate(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [body['content'], body['idx'], decoded['user_id']]
            cursor.execute(
                "update board_comment set content=%s where idx=%s and user_id=%s", arr)
            #rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": True}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def CommentDelete(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [body['idx'], decoded['user_id']]
            cursor.execute(
                'delete from board_comment where idx=%s and user_id=%s', arr)
            return JsonResponse({"result": True}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()
