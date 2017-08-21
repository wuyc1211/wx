from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
from payment.models import *
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from rest_framework.views import APIView
from payment.serializers import *


wx_from = 'abcljailsfuioweijfjlkj34894jdjfsdffsdfzzz'


def getToken(request):
    if request.method == 'POST':
        data = request.POST.get('data', None)
        fromm = request.POST.get('from', None)
        if fromm != wx_from:
            return HttpResponse(json.dumps({'token': 'invalid'}), content_type='application/json')
        data = json.loads(data)
        # print(data)

        openid = data['openid']
        nick_name = data['userInfo']['nickName']
        city = data['userInfo']['city']
        gender = data['userInfo']['gender']
        province = data['userInfo']['province']
        avatarUrl = data['userInfo']['avatarUrl']

        user, created = User.objects.get_or_create(username=openid + '-' + nick_name , password=openid)
        # print(user)

        if user:
            wxuser, created = WxUser.objects.get_or_create(user=user, open_id=openid, nick_name=nick_name, city=city, gender=gender, province=province, avatarUrl=avatarUrl)
            # wxuser, created = WxUser.objects.get_or_create(user=user, open_id=openid, nick_name=nick_name)
            print(wxuser)
            token, created2 = Token.objects.get_or_create(user=user)
            return HttpResponse(json.dumps({'token': str(token)}), content_type='application/json')

        return HttpResponse(json.dumps({'token': 'invalid'}), content_type='application/json')


class CreateOrderView(APIView):
    def post(self, request, format=None):
        order_data = request.data.get('order_data', None)
        data_list = request.data.get('data_list', None)

        # create order firstly
        order_data = json.loads(order_data)
        order_s = OrderSerializer(data=order_data)
        if order_s.is_valid():
            order = order_s.save(wxuser=request.user.WxUser)
        else:
            return Response('invalid order data', status=status.HTTP_400_BAD_REQUEST)

        # create data list as order data
        data_list = json.loads(data_list)
        for item in data_list:
            #client id is sequence in model
            item['sequence'] = item['id'] 
            s = OrderDataSerializer(data=item)
            if s.is_valid():
                s.save(order=order)
            else:
                return Response('invalid data list', status=status.HTTP_400_BAD_REQUEST)
        
        print(order_s.data)
        return Response(order_s.data, status=status.HTTP_201_CREATED)


class WxUserList(APIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        wxusers = WxUser.objects.all()
        s = WxUserSerializer(wxusers, many=True, context={'request':request})
        return Response(s.data)


class WxUserDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = WxUser.objects.all()
    serializer_class = WxUserSerializer

    def get_queryset(self):
        self.queryset = WxUser.objects.filter(user=self.request.user, id=self.kwargs['pk'])
        return super(WxUserDetail, self).get_queryset()


class OrderList(APIView):
    def get(self, request, format=None):
        user = request.user
        print(user.WxUser)
        orders = Order.objects.filter(wxuser=user.WxUser)
        s = OrderSerializer(orders, many=True, context={'request':request})
        return Response(s.data)

    def post(self, request, format=None):
        # print(request.data)
        s = OrderSerializer(data=request.data)
        if s.is_valid():
            s.save(wxuser=request.user.WxUser)
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Order.objects.filter(id=self.)
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        self.queryset = Order.objects.filter(wxuser=self.request.user.WxUser, id=self.kwargs['pk'])
        return super(OrderDetail, self).get_queryset()


class OrderDataList(APIView):
    def get(self, request, order_id, format=None):
        print(order_id)
        order = Order.objects.get(id=order_id)
        
        if not order:
            return Response('invalid order id', status=status.HTTP_204_NO_CONTENT)
        if order.wxuser == request.user.WxUser:
            data = OrderData.objects.filter(order=order)
            s = OrderDataSerializer(data, many=True, context={'request':request})
            return Response(s.data, status=status.HTTP_200_OK)
    
    def post(self, request, order_id, format=None):
        order = Order.objects.get(id=order_id)
        user = self.request.user

        if not order or order.wxuser != user.WxUser:
            return Response('invalid order id', status=status.HTTP_204_NO_CONTENT)
        s = OrderDataSerializer(data=request.data)

        if s.is_valid():
            s.save(order=order)
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDataDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderDataSerializer
    
    def get_queryset(self):
        order_id = self.kwargs['order_id']
        pk = self.kwargs['pk']
        self.queryset = OrderData.objects.filter(id=pk, order=order_id)
        if self.queryset:
            assert self.queryset[0].order.wxuser == self.request.user.WxUser
        return super(OrderDataDetail, self).get_queryset()
