from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *

User = get_user_model()


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'
        read_only_fields = ['id', 'imgSrc']


class MMSerializer(serializers.ModelSerializer):
    component = ComponentSerializer(read_only=True)

    class Meta:
        model = MM
        fields = ['component', 'count']


class AssemblySerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.username', read_only=True)
    moder = serializers.CharField(source='moder.username', default=None,
                                  read_only=True)

    class Meta:
        model = Assembly
        fields = ['id', 'satelliteName', 'flyDate', 'status', 'creator',
                  'moder',
                  'dateCreated', 'dateModerated', 'dateSaved', 'total_price']
        read_only_fields = ['id', 'status', 'dateCreated', 'dateModerated',
                            'dateSaved']


class AssemblyDetailSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.username', read_only=True)
    moder = serializers.CharField(source='moder.username', default=None,
                                  read_only=True)
    components = serializers.SerializerMethodField()

    class Meta:
        model = Assembly
        fields = ['id', 'satelliteName', 'flyDate', 'status', 'creator',
                  'moder',
                  'dateCreated', 'dateModerated', 'dateSaved', 'components',
                  'total_price']
        read_only_fields = ['id', 'status', 'dateCreated', 'dateModerated',
                            'dateSaved']

    def get_components(self, obj):
        mm_objects = MM.objects.filter(idAssembly=obj)
        return MMSerializer(mm_objects, many=True).data


class AssemblyStatusSerializer(serializers.Serializer):
    status = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff', 'is_superuser']
        read_only_fields = ['is_staff', 'is_superuser']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance
