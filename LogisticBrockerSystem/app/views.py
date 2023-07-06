from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer


@api_view(['GET'])
def calculate_sum(request):
    # Получение параметров из URL
    param1 = int(request.GET.get('param1', 0))
    param2 = int(request.GET.get('param2', 0))
    param3 = int(request.GET.get('param3', 0))

    # Вычисление суммы
    total_sum = param1 + param2 + param3

    # Создание словаря с результатами
    data = {
        'param1': param1,
        'param2': param2,
        'param3': param3,
        'total_sum': total_sum
    }

    # Возврат API с результатами
    return Response(data)


class DeliveryDocsViewSet(viewsets.ModelViewSet):
    queryset = DeliveryDocs.objects.all()
    serializer_class = DeliveryDocsSerializer


class AllViewSet(viewsets.ViewSet):
    def list(self, request):
        data = {
            'delivery_docs': DeliveryDocsSerializer(DeliveryDocs.objects.all(), many=True).data,
            'deliveries': DeliverySerializer(Delivery.objects.all(), many=True).data,
            'drivers': DriverSerializer(Driver.objects.all(), many=True).data,
            'prices': PriceSerializer(Price.objects.all(), many=True).data,
            'driver_documents': DriverDocumentSerializer(DriverDocument.objects.all(), many=True).data,
            'orders': OrderSerializer(Order.objects.all(), many=True).data,
            'users': UserSerializer(User.objects.all(), many=True).data,
            'feedback': FeedbackSerializer(Feedback.objects.all(), many=True).data,
            'company': CompanySerializer(Company.objects.all(), many=True).data,
            'messages': MessageSerializer(Message.objects.all(), many=True).data,
            'message_docs': MessageDocSerializer(MessageDoc.objects.all(), many=True).data,
            'company_feedback': CompanyFeedbackSerializer(CompanyFeedback.objects.all(), many=True).data,
            'feedback_images': FeedbackImageSerializer(FeedbackImage.objects.all(), many=True).data,
            'chats': ChatSerializer(Chat.objects.all(), many=True).data,
        }
        return Response(data)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailCreateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (IsAuthenticated,)


class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)


class CompanyDetailCreateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)


class FeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAuthenticated,)


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticated,)


class NewAuthView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.validated_data)
            user = User.objects.get(username=request.data['username'])
            serializer.validated_data['user'] = UserSerializer(user).data

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                type_user='sender',
            )
            user.set_password(serializer.validated_data['password'])
            try:
                validate_password(serializer.validated_data['password'], user)
            except ValidationError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            das = user.save()
            token = TokenObtainPairSerializer()
            token = token.validate({'username': user.username, 'password': serializer.validated_data['password']})
            # print(token)
            token["user"] = UserSerializer(user).data
            # das = TokenObtainSerializer(data={
            #     'username': serializer.validated_data['username'],
            #     'password': serializer.validated_data['password']
            # })
            # if das.is_valid():
            #     print(das.validated_data)
            return Response(token, status=status.HTTP_200_OK)
        errors = serializer.errors
        print(errors)
        return Response(errors, status=status.HTTP_403_FORBIDDEN)


class DriverCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                type_user='driver',
            )
            driver = Driver.objects.create(
                user=user,
                orders=0,
                status='NICE',
            )
            user.set_password(serializer.validated_data['password'])
            try:
                validate_password(serializer.validated_data['password'], user)
            except ValidationError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            das = user.save()
            token = TokenObtainPairSerializer()
            token = token.validate({'username': user.username, 'password': serializer.validated_data['password']})
            # print(token)
            token["user"] = UserSerializer(user).data
            # das = TokenObtainSerializer(data={
            #     'username': serializer.validated_data['username'],
            #     'password': serializer.validated_data['password']
            # })
            # if das.is_valid():
            #     print(das.validated_data)
            return Response(token, status=status.HTTP_200_OK)
        errors = serializer.errors
        print(errors)
        return Response(errors, status=status.HTTP_403_FORBIDDEN)

class CheckPriceView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        if data.is_valid():
            data = data.data
            price = PriceSingle.objects.all()[0]
            data2 = requests.get(str(data['start_place']))
            if 'search' not in data2.url:
                start_place = data2.url.split('@')[1].split(',')[:2]
                start_place = ','.join(start_place).replace('+', '')
            else:
                start_place = data2.url.split('/')[-1].split('?')[0].replace('+', '')

            data2 = requests.get(str(data['end_place']))
            if 'search' not in data2.url:
                end_place = data2.url.split('@')[1].split(',')[:2]
                end_place = ','.join(end_place).replace('+', '')
            else:
                end_place = data2.url.split('/')[-1].split('?')[0].replace('+', '')

            url = f'http://router.project-osrm.org/route/v1/driving/{start_place};{end_place}?steps=true&geometries=geojson&overview=full'
            response = requests.get(url=url)
            print(response.json()['routes'][0])
            total_km = int(response.json()['routes'][0]['distance'])//1000*price.km
            if data['insurance']:
                insurance = price.insurance
            else:
                insurance = 0
            if data['express']:
                express = price.express
            else:
                express = 0

            total = total_km + insurance + express
            payload = {
                "duration": response.json()['routes'][0]['duration'],
                "distance": response.json()['routes'][0]['distance'],
                "km": price.km,
                "total_km": total_km,
                "total": total
            }

            return Response(data=payload, status=status.HTTP_200_OK)
        return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    lookup_field = 'pk'
