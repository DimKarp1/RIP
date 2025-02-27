import uuid

import redis
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from redis.commands.search.reducers import count
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .minio import add_pic, del_pic
from .serializers import ComponentSerializer, UserSerializer, \
    AssemblySerializer, AssemblyDetailSerializer, MMSerializer, \
    AssemblyStatusSerializer
from .models import Component, Assembly, MM

User = get_user_model()

session_storage = redis.StrictRedis(host=settings.REDIS_HOST,
                                    port=settings.REDIS_PORT)


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator

class ComponentList(APIView):
    model_class = Component
    serializer_class = ComponentSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('component_name', openapi.IN_QUERY,
                              description="Название компонента",
                              type=openapi.TYPE_STRING)
        ],
        responses={200: ComponentSerializer(many=True)}
    )
    def get(self, request, format=None):
        input_name = request.query_params.get('сomponent_name', '')

        result_components = self.model_class.objects.filter(
            title__icontains=input_name,
        )

        cur_user = request.user
        if cur_user.is_authenticated:
            cur_assembly = Assembly.objects.filter(
                status='draft', creator=cur_user
            ).first()
        else:
            cur_assembly = None

        assembly_id = cur_assembly.pk if cur_assembly else 0
        components_in_assembly = MM.objects.filter(
            idAssembly=cur_assembly
        ).count() if cur_assembly else 0

        serializer = self.serializer_class(result_components, many=True)
        return Response({
            'components': serializer.data,
            'assemblyDraft': assembly_id,
            'componentsInAssembly': components_in_assembly
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ComponentSerializer)
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComponentDetail(APIView):
    model_class = Component
    serializer_class = ComponentSerializer

    def get(self, request, pk, format=None):
        component = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(component)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ComponentSerializer)
    def put(self, request, pk, format=None):
        component = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(component, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        component = get_object_or_404(self.model_class, pk=pk)
        component.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def add_image(request, pk, format=None):
    component = get_object_or_404(Component, pk=pk)
    picture = request.FILES.get('picture')
    del_pic(component)
    result = add_pic(component, picture)

    if 'error' in result.data:
        return result

    return Response(result.data, status=status.HTTP_200_OK)


class AddComponentToDraftAPIView(APIView):
    def post(self, request, pk):
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        draft = Assembly.objects.filter(status='draft', creator=user).first()
        component = get_object_or_404(Component, pk=pk)

        if not draft and not MM.objects.filter(idAssembly=draft,
                                               component=component).exists():
            draft = Assembly(creator=user)
            draft.save()

        if not MM.objects.filter(idAssembly=draft, component=component).exists():
            new_position = MM(idAssembly=draft, component=component)
            new_position.save()
            return Response(status=status.HTTP_200_OK)

        existing_position = MM.objects.filter(idAssembly=draft,
                                              component=component).first()
        if existing_position:
            existing_position.count += 1
            existing_position.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_208_ALREADY_REPORTED)


class DraftComponentManagementAPIView(APIView):
    def delete(self, request, pk):
        user = request.user
        draft = Assembly.objects.filter(creator=user, status='draft').first()

        if not draft:
            return Response({'error': 'Черновик не найден'}, status=status.HTTP_404_NOT_FOUND)

        mm = MM.objects.filter(idAssembly=draft, component_id=pk).first()
        if not mm:
            return Response({'error': 'Компонент не найден в черновике'}, status=status.HTTP_404_NOT_FOUND)

        mm.delete()
        return Response({'message': 'Компонент успешно удалён из черновика'})

    @swagger_auto_schema(request_body=MMSerializer)
    def put(self, request, pk, format=None):
        user = request.user
        draft = Assembly.objects.filter(creator=user, status='draft').first()

        if not draft:
            return Response({'error': 'Черновик не найден'}, status=status.HTTP_404_NOT_FOUND)

        mm = MM.objects.filter(idAssembly=draft, component_id=pk).first()
        if not mm:
            return Response({'error': 'Компонент не найден в черновике'}, status=status.HTTP_404_NOT_FOUND)

        mm.count = request.data.get('count')
        mm.save()
        return Response(status=status.HTTP_200_OK)


class AssemblyListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        assemblies = Assembly.objects.exclude(status__in=['deleted', 'draft'])

        if not request.user.is_staff:
            assemblies = assemblies.filter(creator=request.user)

        status_filter = request.query_params.get('status')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if status_filter:
            assemblies = assemblies.filter(status=status_filter)
        if start_date:
            assemblies = assemblies.filter(dateSaved__gte=start_date)
        if end_date:
            assemblies = assemblies.filter(dateSaved__lte=end_date + ' 23:59:00')

        serializer = AssemblySerializer(assemblies, many=True)
        return Response(serializer.data)


class AssemblyDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        assembly = get_object_or_404(Assembly, pk=pk)
        if not (assembly.creator == request.user or request.user.is_staff):
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        serializer = AssemblyDetailSerializer(assembly)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AssemblySerializer)
    def put(self, request, pk):
        assembly = get_object_or_404(Assembly, pk=pk)
        if not (assembly.creator == request.user or request.user.is_staff):
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        if assembly.status == 'deleted':
            return Response({'error': 'Сборка удалена'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssemblySerializer(assembly, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        assembly = get_object_or_404(Assembly, pk=pk)
        if not (assembly.creator == request.user or request.user.is_staff):
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        if assembly.status == 'deleted':
            return Response({'error': 'Сборка уже удалена'}, status=status.HTTP_404_NOT_FOUND)
        assembly.status = 'deleted'
        assembly.save()
        return Response({'message': 'Сборка успешно удалена'})


class AssemblyFormAPIView(APIView):
    def post(self, request, pk):
        assembly = get_object_or_404(Assembly, pk=pk, status='draft')
        if not assembly.creator == request.user:
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        if not assembly.satelliteName or not assembly.flyDate:
            return Response({'error': 'Обязательные поля не заполнены'}, status=status.HTTP_400_BAD_REQUEST)
        assembly.status = 'formed'
        assembly.dateSaved = now()
        assembly.save()
        return Response({'message': 'Сборка успешно сформирована'}, status=status.HTTP_200_OK)


class AssemblyCompleteRejectAPIView(APIView):
    @swagger_auto_schema(request_body=AssemblyStatusSerializer)
    def post(self, request, pk):
        assembly = get_object_or_404(Assembly, pk=pk, status='formed')
        new_status = request.data.get('status')
        if new_status not in ['complete', 'reject']:
            return Response({'error': 'Недопустимый статус'}, status=status.HTTP_400_BAD_REQUEST)
        assembly.dateModerated = now()
        assembly.moder = request.user
        if new_status == 'complete':
            assembly.status = 'completed'
            assembly.total_price = MM.objects.filter(idAssembly=assembly).aggregate(
                total=Sum(F('component__price') * F('count'))
            )['total'] or 0
        elif new_status == 'reject':
            assembly.status = 'rejected'
        assembly.save()
        return Response({'message': f'Сборка {new_status}'}, status=status.HTTP_200_OK)



class UserRegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пользователь зарегистрирован', 'user': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            ssid = request.COOKIES.get("session_id")
            session_storage.set(ssid, serializer.data['username'])
            return Response({'message': 'Данные пользователя обновлены', **serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error": "Неверные данные для входа."},
                            status=status.HTTP_400_BAD_REQUEST)

        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)

        response = Response({
            'id': user.id,
            'username': user.username,
            'is_staff': user.is_staff,
        })
        response.set_cookie(
            "session_id", random_key,
        )

        return response


class UserLogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        session_id = request.COOKIES.get('session_id')
        session_storage.delete(session_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
