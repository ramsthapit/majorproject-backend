from rest_framework import serializers
from .models import Geolocation, User

class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Geolocation
    fields = '__all__'

class UserSerilaizer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','name','email','password']
        extra_kwargs = {
          'password': {'write_only': True}
        }
    def get__id(self, obj):
      return obj.id

    def get_name(self, obj):
      name = obj.name
      if name == '':
        name= obj.email
      return name