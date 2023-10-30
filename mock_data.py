#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : mock_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()
import random
from datetime import datetime, timedelta
from faker import Faker
from app.models import *

fake = Faker('zh_CN')

data_count = 100

def gender_product_stock_supplier():
    product_ = [
        "洗发水",
        "牙刷",
        "毛巾",
        "肥皂",
        "牙膏",
        "香皂",
        "洗面奶",
        "沐浴露",
        "洗衣液",
        "剃须刀",
        "护发素",
        "洗手液",
        "卫生纸",
        "护手霜",
        "洗洁精",
        "护肤霜",
        "面膜",
        "洗碗刷",
        "洗衣粉",
        "洗衣机",
        "电吹风",
        "衣架",
        "拖把",
        "桶",
        "瓶子",
        "纸巾",
        "口罩",
        "餐具",
        "杯子",
        "电池",
        "钥匙",
    ]
    def generate_random_data(i):
        # Generate Product data
        product_code = "0" * (5 - len(str(i))) + str(i)
        product_name = fake.random_element(product_)
        monthly_sales = random.randint(100, 1000)
        monthly_revenue = random.uniform(1000, 10000)
        monthly_live_count = random.randint(1, 10)
        gross_profit_margin = random.uniform(0.1, 0.9)

        product = Product(
            product_code=product_code,
            product_name=product_name,
            monthly_sales=monthly_sales,
            monthly_revenue=monthly_revenue,
            monthly_live_count=monthly_live_count,
            gross_profit_margin=gross_profit_margin
        )
        product.save()

        # Generate Stock data
        specification = fake.random_element(
            ["10个/包", "5个/包", "15个/包", "5个/箱", "10个/箱", "20个/箱", "50个/袋", "100个/盒", "200个/桶"])
        warehouse_code = fake.random_number(digits=4)
        stock_quantity = random.randint(100, 1000)
        warehouse_manager = fake.name()

        stock = Stock(
            product_code=product_code,
            product_name=product_name,
            specification=specification,
            warehouse_code=warehouse_code,
            stock_quantity=stock_quantity,
            warehouse_manager=warehouse_manager
        )
        stock.save()

        # Generate Supplier data
        supplier_code = fake.random_number(digits=5)
        supplier_name = fake.company()
        contact_number = fake.phone_number()
        supply_price = random.uniform(10, 100)
        total_purchases = random.randint(100, 1000)

        supplier = Supplier(
            supplier_code=supplier_code,
            supplier_name=supplier_name,
            contact_number=contact_number,
            product_code=product_code,
            supply_price=supply_price,
            total_purchases=total_purchases
        )
        supplier.save()
    for i in range(1, 400):
        generate_random_data(i)


def gender_operating_account():
    def generate_random_data():
        account_number = fake.random_number(digits=6)
        platform = random.choice(['抖音', '淘宝', '快手', '小红书'])
        account_homepage = fake.url()
        fan_count = random.randint(100, 1000)
        establishment_date = fake.date_between(start_date='-1y', end_date='today')
        operator_number = fake.random_number(digits=6)
        account_content = fake.random_element(['美妆', '时尚', '电商', '游戏'])
        total_videos = random.randint(1, 100)
        total_views = random.randint(1000, 1000000)

        operating_account = OperatingAccount(
            account_number=account_number,
            platform=platform,
            account_homepage=account_homepage,
            fan_count=fan_count,
            establishment_date=establishment_date,
            operator_number=operator_number,
            account_content=account_content,
            total_videos=total_videos,
            total_views=total_views
        )
        operating_account.save()

    # Generate 100 random data entries
    for _ in range(100):
        generate_random_data()


def gender_live_boardcast():
    def generate_random_data():
        # Generate Broadcaster data
        broadcaster_code = fake.random_number(digits=5)
        broadcaster_name = fake.name()
        gender = random.choice(['男', '女'])
        age = random.randint(18, 60)
        signed_platform = random.choice(['抖音', '淘宝', '快手', '小红书'])
        operating_company = fake.company()
        personal_homepage = fake.url()
        expertise = fake.random_element(['美妆', '时尚', '电商', '游戏'])

        broadcaster = Broadcaster(
            broadcaster_code=broadcaster_code,
            broadcaster_name=broadcaster_name,
            gender=gender,
            age=age,
            signed_platform=signed_platform,
            operating_company=operating_company,
            personal_homepage=personal_homepage,
            expertise=expertise
        )
        broadcaster.save()

        # Generate BroadcastPerformance data
        monthly_broadcasts = random.randint(1, 10)
        monthly_featured_products = random.randint(10, 50)
        revenue = random.uniform(1000, 10000)
        tips_income = random.uniform(100, 1000)
        standard_salary = random.uniform(2000, 5000)
        reward_weight = random.uniform(0.1, 1.0)

        broadcast_performance = BroadcastPerformance(
            broadcaster_code=broadcaster_code,
            monthly_broadcasts=monthly_broadcasts,
            monthly_featured_products=monthly_featured_products,
            revenue=revenue,
            tips_income=tips_income,
            standard_salary=standard_salary,
            reward_weight=reward_weight
        )
        broadcast_performance.save()

        # Generate LiveBroadcast data
        broadcast_code = fake.random_number(digits=5)
        broadcast_time = fake.date_time_this_year()
        working_minutes = random.randint(30, 180)
        product_code = fake.random_number(digits=6)
        product_order = random.randint(1, 5)

        live_broadcast = LiveBroadcast(
            broadcaster_code=broadcaster_code,
            broadcast_code=broadcast_code,
            broadcast_time=broadcast_time,
            working_minutes=working_minutes,
            product_code=product_code,
            product_order=product_order
        )
        live_broadcast.save()

    # Generate random data
    for _ in range(data_count):
        generate_random_data()


def gender_live_plan_info():
    def generate_random_data():
        # Generate LiveBroadcastPlan data
        # broadcast_code = fake.random_number(digits=6)
        broadcast_code = fake.random_element([str(i) for i in range(10000, 19999)])
        broadcast_name = fake.random_element(['双11夜间场', '618活动', '双十二活动', '双11白天场', '618活动夜场', '618活动白天', '双十二活动夜场'])
        broadcast_platform = random.choice(['抖音', '淘宝', '快手', '小红书'])
        broadcast_link = fake.url()
        broadcast_description = fake.text()
        start_time = fake.date_time_between(start_date='-1y', end_date='now')
        end_time = start_time + timedelta(hours=2)

        broadcast_plan = LiveBroadcastPlan(
            broadcast_code=broadcast_code,
            broadcast_name=broadcast_name,
            broadcast_platform=broadcast_platform,
            broadcast_link=broadcast_link,
            broadcast_description=broadcast_description,
            start_time=start_time,
            end_time=end_time
        )
        broadcast_plan.save()

        # Generate LiveBroadcastInfo data
        live_viewers = random.randint(100, 5000)
        average_fan_duration = random.randint(5, 30)
        click_count = random.randint(10, 1000)
        tips_amount = random.uniform(100, 1000)
        interaction_count = random.randint(50, 1000)

        live_info = LiveBroadcastInfo(
            broadcast_code=broadcast_code,
            broadcast_name=broadcast_name,
            live_viewers=live_viewers,
            average_fan_duration=average_fan_duration,
            click_count=click_count,
            tips_amount=tips_amount,
            interaction_count=interaction_count
        )
        live_info.save()

    # Define the number of data entries to generate

    # Generate random data
    for _ in range(data_count):
        generate_random_data()


def gender_sales():
    def generate_random_data():
        # Generate Sales data
        sales_code = fake.random_number(digits=6)
        broadcast_code = fake.random_number(digits=6)
        product_code = fake.random_number(digits=6)
        quantity = random.randint(1, 10000)
        total_price = random.uniform(100, 1000)
        order_info = fake.text()
        order_time = fake.date_time_between(start_date='-1y', end_date='now')

        sales = Sales(
            sales_code=sales_code,
            broadcast_code=broadcast_code,
            product_code=product_code,
            quantity=quantity,
            total_price=total_price,
            order_info=order_info,
            order_time=order_time
        )
        sales.save()

        # Generate PurchaseOrder data
        order_code = fake.random_number(digits=6)
        supplier_code = fake.random_number(digits=6)
        quantity = random.randint(100, 1000)
        purchaser = fake.name()
        warehouse = str(random.randint(100, 1000))
        purchase_time = fake.date_time_between(start_date='-1y', end_date='now')
        arrival_time = purchase_time + timedelta(days=random.randint(1, 30))

        purchase_order = PurchaseOrder(
            order_code=order_code,
            product_code=product_code,
            supplier_code=supplier_code,
            quantity=quantity,
            purchaser=purchaser,
            warehouse=warehouse,
            purchase_time=purchase_time,
            arrival_time=arrival_time
        )
        purchase_order.save()

        # Generate AfterSales data
        after_sales_code = fake.random_number(digits=6)
        user_account = fake.user_name()
        phone_number = fake.phone_number()
        after_sales_type = fake.random_element(['退货', '换货', '退款', '退货退款'])
        reason = fake.text()
        initiation_time = fake.date_time_between(start_date='-1y', end_date='now')
        status = fake.random_element(['已完成', '待审核'])

        after_sales = AfterSales(
            after_sales_code=after_sales_code,
            sales_code=sales_code,
            user_account=user_account,
            phone_number=phone_number,
            after_sales_type=after_sales_type,
            reason=reason,
            initiation_time=initiation_time,
            status=status
        )
        after_sales.save()

    # Define the number of data entries to generate

    # Generate random data
    for _ in range(data_count):
        generate_random_data()


if __name__ == '__main__':
    pass
    # gender_product_stock_supplier()
    # gender_operating_account()
    # gender_live_boardcast()
    # gender_live_plan_info()
    # gender_sales()
