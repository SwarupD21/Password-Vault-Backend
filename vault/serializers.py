from rest_framework import serializers
from .models import *

class VaultCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = VaultEntry
        fields = [
            'service_name',
            'login_identifier',
            'password',
            'notes',
        ]

class VaultReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultEntry
        fields = [
            'id',
            'service_name',
            'login_identifier',
            'notes',
            'created_at',
            'updated_at',
        ]

