from django.db import models


# Create your models here.


class User(models.Model):
    """用户"""

    GENDER = (("0", "女"), ("1", "男"), ("2", "未知"))
    ROLE = (("1", "工作人员"), ("2", "主播"))
    username = models.CharField(max_length=128, unique=True)
    nickname = models.CharField("昵称", max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=264)
    phone = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField("出生日期", null=True, blank=True)
    gender = models.CharField(max_length=1, default="2", choices=GENDER)
    img = models.ImageField(upload_to="uploads/", null=True, blank=True)
    role = models.CharField("角色", max_length=1, default="3", choices=ROLE)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = "platform_user"
        verbose_name = "平台用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def menu(self):
        if self.role == "1":
            return {
                "homeInfo": {"title": "首页", "href": "page/welcome/"},
                "logoInfo": {
                    "title": "直播电商管理",
                    "image": "static/images/logo.png",
                    "href": "#",
                },
                "menuInfo": [
                    {
                        "title": "常规管理",
                        "icon": "fa fa-address-book",
                        "href": "",
                        "target": "_self",
                        "child": [
                            {
                                "title": "用户管理",
                                "href": "/user_manage/",
                                "icon": "fa fa-user",
                                "target": "_self",
                            },
                            {
                                "title": "运营管理",
                                "href": "",
                                "icon": "fa fa-asterisk",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "账号运营",
                                        "href": "/operating_account_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "招商选品",
                                        "href": "/product_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "数据分析",
                                        "href": "page/welcome/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "商品管理",
                                "href": "",
                                "icon": "fa fa-certificate",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "采购管理",
                                        "href": "/purchase_order_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "库存管理",
                                        "href": "/stock_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "主播管理",
                                "href": "",
                                "icon": "fa fa-diamond",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "主播信息",
                                        "href": "/broadcaster_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "主播排期",
                                        "href": "/live_broadcaster_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "主播绩效",
                                        "href": "/broadcaster_pf_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "直播管理",
                                "href": "",
                                "icon": "fa fa-lemon-o",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "直播计划",
                                        "href": "/live_broadcaster_pl_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "实时看板",
                                        "href": "/kanban/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "直播复盘",
                                        "href": "/review/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "售后管理",
                                "href": "/after_sales_table/",
                                "icon": "fa fa-life-saver",
                                "target": "_self",
                            },
                            {
                                "title": "操作记录",
                                "href": "/log_table/",
                                "icon": "fa fa-history",
                                "target": "_self",
                            },

                        ],
                    },
                ],
            }
        elif self.role == "2":
            return {
                "homeInfo": {"title": "首页", "href": "page/welcome/"},
                "logoInfo": {
                    "title": "直播电商管理",
                    "image": "static/images/logo.png",
                    "href": "#",
                },
                "menuInfo": [
                    {
                        "title": "常规管理",
                        "icon": "fa fa-address-book",
                        "href": "",
                        "target": "_self",
                        "child": [
                            {
                                "title": "运营管理",
                                "href": "",
                                "icon": "fa fa-asterisk",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "账号运营",
                                        "href": "/operating_account_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "招商选品",
                                        "href": "/product_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "数据分析",
                                        "href": "page/welcome/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "商品管理",
                                "href": "",
                                "icon": "fa fa-certificate",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "采购管理",
                                        "href": "/purchase_order_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "库存管理",
                                        "href": "/stock_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "主播管理",
                                "href": "",
                                "icon": "fa fa-diamond",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "主播信息",
                                        "href": "/broadcaster_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "主播排期",
                                        "href": "/live_broadcaster_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "主播绩效",
                                        "href": "/broadcaster_pf_table/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "直播管理",
                                "href": "",
                                "icon": "fa fa-lemon-o",
                                "target": "_self",
                                "child": [
                                    {
                                        "title": "直播计划",
                                        "href": "/live_broadcaster_pl_table/",
                                        "icon": "fa fa-list-alt",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "实时看板",
                                        "href": "/kanban/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    },
                                    {
                                        "title": "直播复盘",
                                        "href": "/review/",
                                        "icon": "fa fa-navicon",
                                        "target": "_self"
                                    }
                                ]
                            },
                            {
                                "title": "售后管理",
                                "href": "/after_sales_table/",
                                "icon": "fa fa-life-saver",
                                "target": "_self",
                            },
                            {
                                "title": "操作记录",
                                "href": "/log_table/",
                                "icon": "fa fa-history",
                                "target": "_self",
                            },

                        ],
                    },
                ],
            }


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "日志"
        verbose_name_plural = verbose_name


class OperatingAccount(models.Model):
    account_number = models.CharField(max_length=20, verbose_name='运营账号编号')
    platform = models.CharField(max_length=50, verbose_name='账号平台')
    account_homepage = models.URLField(verbose_name='账号主页')
    fan_count = models.IntegerField(verbose_name='粉丝数')
    establishment_date = models.DateField(verbose_name='建立日期')
    operator_number = models.CharField(max_length=50, verbose_name='运营主播编号')
    account_content = models.CharField(max_length=50, verbose_name='账号内容')
    total_videos = models.IntegerField(verbose_name='总视频数')
    total_views = models.BigIntegerField(verbose_name='总播放量')

    def __str__(self):
        return self.account_number

    class Meta:
        verbose_name = "运营账号表"
        verbose_name_plural = verbose_name


class Product(models.Model):
    product_code = models.CharField(max_length=20, verbose_name='商品编号')
    product_name = models.CharField(max_length=100, verbose_name='商品名称')
    monthly_sales = models.IntegerField(verbose_name='本月销量')
    monthly_revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='本月销售额')
    monthly_live_count = models.IntegerField(verbose_name='月参与直播数')
    gross_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='毛利率')
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='商品记录时间')

    def __str__(self):
        return self.product_code

    class Meta:
        verbose_name = "商品信息表"
        verbose_name_plural = verbose_name


class Stock(models.Model):
    product_code = models.CharField(max_length=20, verbose_name='商品编号')
    product_name = models.CharField(max_length=100, verbose_name='商品名称')
    specification = models.CharField(max_length=50, verbose_name='规格')
    warehouse_code = models.CharField(max_length=20, verbose_name='仓库编码')
    stock_quantity = models.IntegerField(verbose_name='库存数量')
    warehouse_manager = models.CharField(max_length=50, verbose_name='仓库管理员')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "库存信息表"
        verbose_name_plural = verbose_name


class Supplier(models.Model):
    supplier_code = models.CharField(max_length=20, verbose_name='供应商编号')
    supplier_name = models.CharField(max_length=100, verbose_name='供应商名称')
    contact_number = models.CharField(max_length=20, verbose_name='联系电话')
    product_code = models.CharField(max_length=20, verbose_name='商品编号')
    supply_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='供应价格')
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')
    total_purchases = models.IntegerField(verbose_name='累计采购')

    def __str__(self):
        return self.supplier_code

    class Meta:
        verbose_name = "供应商信息表"
        verbose_name_plural = verbose_name


class Broadcaster(models.Model):
    broadcaster_code = models.CharField(max_length=20, verbose_name='主播编号')
    broadcaster_name = models.CharField(max_length=100, verbose_name='主播姓名')
    gender = models.CharField(max_length=10, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    signed_platform = models.CharField(max_length=50, verbose_name='签约平台')
    operating_company = models.CharField(max_length=100, verbose_name='运营公司')
    personal_homepage = models.URLField(verbose_name='个人主页')
    expertise = models.CharField(max_length=100, verbose_name='特长')

    def __str__(self):
        return self.broadcaster_code

    class Meta:
        verbose_name = "主播信息表"
        verbose_name_plural = verbose_name


class BroadcastPerformance(models.Model):
    broadcaster_code = models.CharField(max_length=20, verbose_name='主播编号')
    monthly_broadcasts = models.IntegerField(verbose_name='本月直播')
    monthly_featured_products = models.IntegerField(verbose_name='本月推荐商品')
    revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='销售额')
    tips_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='打赏收入')
    standard_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='标准工资')
    reward_weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='奖励权重')
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    def __str__(self):
        return self.broadcaster_code

    class Meta:
        verbose_name = "主播绩效表"
        verbose_name_plural = verbose_name


class LiveBroadcast(models.Model):
    broadcaster_code = models.CharField(max_length=20, verbose_name='主播编号')
    broadcast_code = models.CharField(max_length=20, verbose_name='直播编号')
    broadcast_time = models.DateTimeField(verbose_name='直播时间')
    working_minutes = models.IntegerField(verbose_name='工作时长（分钟）')
    product_code = models.CharField(max_length=20, verbose_name='带货商品编号')
    product_order = models.IntegerField(verbose_name='带货顺序')

    def __str__(self):
        return self.broadcast_code

    class Meta:
        verbose_name = "主播排期表"
        verbose_name_plural = verbose_name


class LiveBroadcastPlan(models.Model):
    broadcast_code = models.CharField(max_length=20, verbose_name='直播编号')
    broadcast_name = models.CharField(max_length=100, verbose_name='直播名称')
    broadcast_platform = models.CharField(max_length=50, verbose_name='直播平台')
    broadcast_link = models.URLField(verbose_name='直播链接')
    broadcast_description = models.TextField(verbose_name='直播简介')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')

    def __str__(self):
        return self.broadcast_code

    class Meta:
        verbose_name = "直播计划表"
        verbose_name_plural = verbose_name


class LiveBroadcastInfo(models.Model):
    broadcast_code = models.CharField(max_length=20, verbose_name='直播编号')
    broadcast_name = models.CharField(max_length=100, verbose_name='直播名称')
    live_viewers = models.IntegerField(verbose_name='实时人数')
    average_fan_duration = models.IntegerField(verbose_name='粉丝平均停留时间（分钟）')
    click_count = models.IntegerField(verbose_name='功能点击数')
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='打赏金额')
    interaction_count = models.IntegerField(verbose_name='互动数')
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='实时记录时间')

    def __str__(self):
        return self.broadcast_code

    class Meta:
        verbose_name = "直播信息表"
        verbose_name_plural = verbose_name


class Sales(models.Model):
    sales_code = models.CharField(max_length=20, verbose_name='销售编号')
    broadcast_code = models.CharField(max_length=20, verbose_name='所属直播编号')
    product_code = models.CharField(max_length=20, verbose_name='商品编号')
    quantity = models.IntegerField(verbose_name='购买数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='交易总价')
    order_info = models.CharField(max_length=200, verbose_name='销售订单信息')
    order_time = models.DateTimeField(verbose_name='下单时间')

    def __str__(self):
        return self.sales_code

    class Meta:
        verbose_name = "销售信息表"
        verbose_name_plural = verbose_name


class PurchaseOrder(models.Model):
    order_code = models.CharField(max_length=20, verbose_name='采购订单编号')
    product_code = models.CharField(max_length=20, verbose_name='商品编号')
    supplier_code = models.CharField(max_length=20, verbose_name='来源供应商编号')
    quantity = models.IntegerField(verbose_name='采购数量')
    purchaser = models.CharField(max_length=100, verbose_name='采购员')
    warehouse = models.CharField(max_length=100, verbose_name='入库仓库')
    purchase_time = models.DateTimeField(verbose_name='采购时间')
    arrival_time = models.DateTimeField(verbose_name='入库时间')

    def __str__(self):
        return self.order_code

    class Meta:
        verbose_name = "采购信息表"
        verbose_name_plural = verbose_name


class AfterSales(models.Model):
    after_sales_code = models.CharField(max_length=20, verbose_name='售后编号')
    sales_code = models.CharField(max_length=20, verbose_name='销售编号')
    user_account = models.CharField(max_length=100, verbose_name='用户账号')
    phone_number = models.CharField(max_length=20, verbose_name='手机号码')
    after_sales_type = models.CharField(max_length=100, verbose_name='申请售后类型')
    reason = models.TextField(verbose_name='申请原因')
    initiation_time = models.DateTimeField(verbose_name='发起售后时间')
    status = models.CharField(max_length=100, verbose_name='售后状态')

    def __str__(self):
        return self.after_sales_code

    class Meta:
        verbose_name = "售后信息表"
        verbose_name_plural = verbose_name
