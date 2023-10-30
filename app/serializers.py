import json

from rest_framework import serializers

from .models import *


class UserSerializers(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        return obj.get_role_display()

    class Meta:
        model = User
        exclude = ('password',)


class LogSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Log
        fields = "__all__"


class OperatingAccountSerializers(serializers.ModelSerializer):

    class Meta:
        model = OperatingAccount
        fields = "__all__"


class ProductSerializers(serializers.ModelSerializer):
    stock_quantity = serializers.SerializerMethodField()

    def get_stock_quantity(self, obj):
        try:
            return Stock.objects.filter(product_code=obj.product_code).first().stock_quantity
        except:
            return 0

    class Meta:
        model = Product
        fields = "__all__"


class PurchaseOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class StockSerializers(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = "__all__"

class BroadcasterSerializers(serializers.ModelSerializer):

    class Meta:
        model = Broadcaster
        fields = "__all__"

class LiveBroadcastSerializers(serializers.ModelSerializer):

    class Meta:
        model = LiveBroadcast
        fields = "__all__"


class BroadcastPerformanceSerializers(serializers.ModelSerializer):

    class Meta:
        model = BroadcastPerformance
        fields = "__all__"

class LiveBroadcastPlanSerializers(serializers.ModelSerializer):

    class Meta:
        model = LiveBroadcastPlan
        fields = "__all__"

class AfterSalesSerializers(serializers.ModelSerializer):

    class Meta:
        model = AfterSales
        fields = "__all__"
