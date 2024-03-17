from django.contrib.auth.models import User
from .models import SolMate
from rest_framework import serializers

class SolMateSerializer(serializers.ModelSerializer):
    
    owner = serializers.SerializerMethodField("get_owner")
    
    class Meta:
        model = SolMate
        fields = '__all__'
        read_only_fields = ['serial_number',]
        
    def get_owner(self, obj):
        return obj.owner.username