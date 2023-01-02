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
        fields = ['id','name','email','password','is_staff','is_superuser']
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
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
          instance.set_password(password)
        instance.save()
        return instance