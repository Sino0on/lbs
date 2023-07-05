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


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class DriverDocumentViewSet(viewsets.ModelViewSet):
    queryset = DriverDocument.objects.all()
    serializer_class = DriverDocumentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDocViewSet(viewsets.ModelViewSet):
    queryset = MessageDoc.objects.all()
    serializer_class = MessageDocSerializer


class CompanyFeedbackViewSet(viewsets.ModelViewSet):
    queryset = CompanyFeedback.objects.all()
    serializer_class = CompanyFeedbackSerializer


class FeedbackImageViewSet(viewsets.ModelViewSet):
    queryset = FeedbackImage.objects.all()
    serializer_class = FeedbackImageSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer


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
