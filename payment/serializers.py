from django.contrib.auth.models import User, Group
from rest_framework import serializers
from payment.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class WxUserSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.username')
	class Meta:
		model = WxUser
		fields = ['id', 'user', 'nick_name', 'avatarUrl', 'city', 'gender']


class OrderSerializer(serializers.ModelSerializer):
    wxuser = serializers.ReadOnlyField(source='wxuser.nick_name')
    class Meta:
        model = Order
        fields = ['id', 'wxuser', 'title', 'created', 'end']


class OrderDataSerializer(serializers.ModelSerializer):
    order_id = serializers.ReadOnlyField(source='order.id')
    class Meta:
        model = OrderData
        fields = ['order_id', 'sequence', 'name', 'price', 'comments', 'disabled']