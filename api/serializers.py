from rest_framework import serializers
from home import models as homeModels

# serializer marbot be khane
class HomeViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = homeModels.Home
        fields = "__all__"


class physicsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = homeModels.TimeOfDevice
        fields = "__all__"

class deviceSerializer(serializers.ModelSerializer):
    device = serializers.IntegerField(source= 'id')
    class Meta:
        model = homeModels.device
        fields = "__all__"