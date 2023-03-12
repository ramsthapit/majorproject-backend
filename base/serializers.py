from rest_framework import serializers
from .models import Geolocation, User, BusStopLoc, OccupancyCount

class LocationSerializer(serializers.ModelSerializer):
  user = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = Geolocation
    fields = '__all__'

  def get_user(self, obj):
    # print(self.id)
    return obj.user

class UserSerilaizer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','name','email','password','is_driver','license_no','vechile_no','is_staff','is_superuser']
        # fields = '__all__'
        extra_kwargs = {
          'password': {'write_only': True}
        }
    def get_id(self, obj):
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
    
class BSLSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = BusStopLoc
        fields = "__all__"

class CountSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = OccupancyCount
        fields = "__all__"