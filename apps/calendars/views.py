import jwt

from django.http import request
from django.shortcuts import render
from django.db import connection

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
from collections import namedtuple


def namedtuplefetchall(cursor):
    desc = cursor.description
    fields = [col[0] for col in desc]
    nt_result = namedtuple('Result', fields)
    return [nt_result(*row) for row in cursor.fetchall()]


@api_view(['POST'])
def CreateCalendar(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [body['title'], decoded['user_id'], body['category'], body['category_color'],
                   body['desc'], body['schedule'], body['date'], body['alarm'], body['group_idx']]
            cursor.execute(
                "insert into calendar(title, user_id, category, color, content, time, event_day, alarm, group_code) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", arr)
            return JsonResponse({"result": "success"}, statis=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def AllCalendar(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [decoded['user_id'], body['group_idx']]
            cursor.execute(
                "select * from group_member inner join calendar on group_member.group_code = calendar.group_code where group_member.member = %s and calendar.group_code = %s", arr)
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def DetailCalendar(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            cursor.execute(
                "select * from calendar where idx = %s", [body['idx']])
            rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def UpdateCalendar(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=["HS256"])
            if (decoded['user_id'] == None):
                return JsonResponse({"result": "jwtwebtoken Error"}, status=status.HTTP_200_OK)
            arr = [body['title'], body['category'], body['category_color'],
                   body['desc'], body['schedule'], body['alarm']]
            cursor.execute(
                "update calendar set title=%s, category=%s, color=%s, content=%s, time=%s, alarm=%s where idx=%s and group_idx=%s and user_id=%s",
                arr
            )
            #rows = namedtuplefetchall(cursor)
            return JsonResponse({"result": "success"}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(["POST"])
def DeleteCalendar(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=['HS256'])
            arr = [body['idx'], body['group_code'], decoded['user_id']]
            cursor.execute(
                "delete from calendar where idx=%s and group_idx=%s and user_id=%s", arr)
            return JsonResponse({"result": "success"}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()


@api_view(['POST'])
def AlarmCard(request):
    with connection.cursor() as cursor:
        try:
            body = JSONParser().parse(request)
            decoded = jwt.decode(
                body['token'], 'secretkey', algorithms=['HS256'])
            arr = [decoded['user_id'], body['group_idx'], 'On']
            query = "select * from group_member inner join calendar " +
            "on group_member.group_code = calendar.group_code " +
            "where (calendar.event_day > curdate() or " +
            "(calendar.event_day = curdate() and " +
            "calendar.time >= date_format(now(), '%H:%i'))) and group_member.member = %s and calendar.group_code = %s " +
            "and calendar.alarm = %s " +
            "order by calendar.event_day,calendar.time ASC"
            cursor.exectue(query, arr)
            rows = namedtuplefetchall
            return JsonResponse({"result": rows}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({"error": Exception}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            cursor.close()
