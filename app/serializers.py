from rest_framework import serializers
from .models import Jiancheng

class JianchengSerializers(serializers.ModelSerializer):
    class Meta:
        model=Jiancheng
        fields='__all__'