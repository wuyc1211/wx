from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class WxUser(models.Model):
	user = models.OneToOneField(User, related_name='WxUser', verbose_name='用户')
	open_id = models.CharField(max_length=30, null=False)
	nick_name = models.CharField(max_length=30, null=False, verbose_name='昵称')
	city = models.CharField(max_length=30, null=True, blank=True, verbose_name='城市')
	gender = models.IntegerField(default=1, verbose_name='性别')
	province = models.CharField(max_length=20, blank=True, null=True, verbose_name='省份')
	avatarUrl = models.CharField(max_length=150, null=True, blank=True, verbose_name='头像URL')

	def __str__(self):
		return self.user.username + '-wxuser'
		

class Order(models.Model):
	wxuser = models.ForeignKey(WxUser, related_name='orders', to_field='user', verbose_name='微信用户')
	title = models.CharField(max_length=40, null=False, blank=False)
	# end = models.DateTimeField(verbose_name='截止时间')
	created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	end = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')

	def __str__(self):
		return self.title


class OrderData(models.Model):
	order = models.ForeignKey(Order, related_name='order_data', to_field='id', verbose_name='订单')
	sequence = models.IntegerField(verbose_name='数据编号')
	name = models.CharField(max_length=40, verbose_name='名称')
	price = models.FloatField(verbose_name='价格')
	comments = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注')
	disabled = models.BooleanField(default=False)

	class Meta:
		unique_together = ('order', 'sequence')

	def __str__(self):
		return str(self.sequence) + '_' + self.name + '_' + str(self.price)
