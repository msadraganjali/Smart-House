# smart-city
## api/create_home
### شما باید سه مقدار user_nid, password, locate رو وارد کنید
### user_nid = کدملی
### password = رمز
### locate = ناحیه کشوری

## api/get_home
### باید رمز رو اینطوری وارد کنید
### api/get_home/<password\>

## api/get_obj
### ایدی شعی رو وارد کنید
### api/get_obj/<id\>

## post_status_to_home/
### uuid که خانه وارد شود
### usage مقدار استفاده منابع (عدد دلخواه)
### is_accident در صورت حریق خودکار وارد می‌شود.
### is_end در صورت تمایل به قطع شعی ترو باشد.
### is_end_forever در صورت قطع دایم ترو باشد
### is_end_start در صورت قطع زمان دار زمان و تاریخ شروع واردشود.
### is_end_end در صورت قطع زمان دار زمان و تاریخ پایان واردشود.
> ~@github/@msadraganjali