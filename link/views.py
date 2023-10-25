import uuid
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from link.models import Link
from news.models import News
from news.serializers import NewsSerializer

class LinkAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request) -> Response:
        try:
            news_id = request.data.get('news_id', None)
            news_get = News.objects.get(id=news_id)

            current_url = request.build_absolute_uri()
            token = str(uuid.uuid4())[:12]
            link = f'{current_url}{token}'
            expiration_date = timezone.now() + timedelta(hours=1)
            Link.objects.create(token=token, news=news_get, expiration_date=expiration_date)
        except (ValueError,  News.DoesNotExist) as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'link': link}, status=status.HTTP_201_CREATED)

    def get(self, request, token=None) -> Response:
        if token:
            try:
                link = Link.objects.get(token=token)
                if not link.expiration_date:
                    return Response({'message': 'link invalid'}, status=status.HTTP_400_BAD_REQUEST)
                if link.expiration_date < timezone.now():
                    return Response({'message': 'link expired'}, status=status.HTTP_400_BAD_REQUEST)
                serializer = NewsSerializer(link.news, many=False).data
            except Link.DoesNotExist as e: 
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer, status=status.HTTP_200_OK)