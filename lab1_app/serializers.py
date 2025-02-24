from .models import *
from rest_framework import serializers

        
class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'
        #fields = ["pk", "company_name", "price", "is_growing", "date_modified", "url"]
        
class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly
        fields = '__all__'