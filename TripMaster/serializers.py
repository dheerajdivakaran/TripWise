from django.contrib.auth.models import User
from rest_framework import serializers
from TripMaster.models import TripDb, TripMemberDb

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password","email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TripSerializers(serializers.ModelSerializer):
    class Meta:
        model = TripDb
        fields = "__all__"
        read_only_fields = ["id","created_by","created_at","updated_at"]

class TripMemberSerializers(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    member_username = serializers.CharField(source = 'user.username',read_only=True)
    member_user_id = serializers.IntegerField(source = 'user.id',read_only=True)

    class Meta:
        model = TripMemberDb
        fields = ["id", "username", "member_username", "member_user_id", "joined_at"]
        read_only_fields = ['id','joined_at']

    def validate_username(self,value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("this user is not registered")
        trip =self.context['trip']
        if user == trip.created_by:
            raise serializers.ValidationError("the creator is alredy the trip owner")
        if TripMemberDb.objects.filter(trip=trip,user=user).exists():
            raise serializers.ValidationError("this user is already a member")
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        user = User.objects.get(username=username)
        trip =self.context['trip']
        return TripMemberDb.objects.create(trip=trip,user=user)

