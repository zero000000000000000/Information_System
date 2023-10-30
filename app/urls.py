from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/init/', views.api_init, name='api_init'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('find_password/', views.find_password, name='find_password'),
    path('user_info/', views.user_info, name='user_info'),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_manage/', views.user_manage, name='user_manage'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('del_user/', views.del_user, name='del_user'),
    path('page/welcome/', views.welcome, name='welcome'),
    path('log_table/', views.log_table, name='log_table'),

    path('operating_account_table/', views.operating_account_table, name='operating_account_table'),
    path('add_operating_account/', views.add_operating_account, name='add_operating_account'),
    path('edit_operating_account/', views.edit_operating_account, name='edit_operating_account'),
    path('del_operating_account/', views.del_operating_account, name='del_operating_account'),

    path('product_table/', views.product_table, name='product_table'),
    path('see_supplier/', views.see_supplier, name='see_supplier'),

    path('purchase_order_table/', views.purchase_order_table, name='purchase_order_table'),
    path('add_purchase_order/', views.add_purchase_order, name='add_purchase_order'),
    path('edit_purchase_order/', views.edit_purchase_order, name='edit_purchase_order'),
    path('del_purchase_order/', views.del_purchase_order, name='del_purchase_order'),

    path('stock_table/', views.stock_table, name='stock_table'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('edit_stock/', views.edit_stock, name='edit_stock'),
    path('del_stock/', views.del_stock, name='del_stock'),

    path('broadcaster_table/', views.broadcaster_table, name='broadcaster_table'),
    path('add_broadcaster/', views.add_broadcaster, name='add_broadcaster'),
    path('edit_broadcaster/', views.edit_broadcaster, name='edit_broadcaster'),
    path('del_broadcaster/', views.del_broadcaster, name='del_broadcaster'),

    path('live_broadcaster_table/', views.live_broadcaster_table, name='live_broadcaster_table'),
    path('add_live_broadcaster/', views.add_live_broadcaster, name='add_live_broadcaster'),
    path('edit_live_broadcaster/', views.edit_live_broadcaster, name='edit_live_broadcaster'),
    path('del_live_broadcaster/', views.del_live_broadcaster, name='del_live_broadcaster'),

    # 主播绩效
    path('broadcaster_pf_table/', views.broadcaster_pf_table, name='broadcaster_pf_table'),
    path('add_broadcaster_pf/', views.add_broadcaster_pf, name='add_broadcaster_pf'),
    path('edit_broadcaster_pf/', views.edit_broadcaster_pf, name='edit_broadcaster_pf'),
    path('del_broadcaster_pf/', views.del_broadcaster_pf, name='del_broadcaster_pf'),

    # 直播计划
    path('live_broadcaster_pl_table/', views.live_broadcaster_pl_table, name='live_broadcaster_pl_table'),
    path('add_live_broadcaster_pl/', views.add_live_broadcaster_pl, name='add_live_broadcaster_pl'),
    path('edit_live_broadcaster_pl/', views.edit_live_broadcaster_pl, name='edit_live_broadcaster_pl'),
    path('del_live_broadcaster_pl/', views.del_live_broadcaster_pl, name='del_live_broadcaster_pl'),

    # 售后
    path('after_sales_table/', views.after_sales_table, name='after_sales_table'),
    path('add_after_sales/', views.add_after_sales, name='add_after_sales'),
    path('edit_after_sales/', views.edit_after_sales, name='edit_after_sales'),
    path('del_after_sales/', views.del_after_sales, name='del_after_sales'),

    path('review/', views.review, name='review'),

    # 实时看板
    path('kanban/', views.kanban, name='kanban'),
    path('kanban_tu/', views.kanban_tu, name='kanban_tu')

]
