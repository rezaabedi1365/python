برای **دریافت و بارگذاری دیتاست با pandas** معمولاً از توابع زیر استفاده می‌شود:

- **pd.read_csv()**: بارگذاری فایل CSV به دیتافریم  
  ```python
  import pandas as pd
  df = pd.read_csv('file.csv')
  ```
  این تابع بسیار انعطاف‌پذیر است و می‌توانید پارامترهایی مثل جداکننده، اندیس، ستون‌های خاص و ... را تنظیم کنید[10].

- **pd.read_excel()**: بارگذاری فایل Excel  
  ```python
  df = pd.read_excel('file.xlsx')
  ```

- **pd.read_json()**: بارگذاری فایل JSON  
  ```python
  df = pd.read_json('file.json')
  ```

- **pd.read_sql_query()**: بارگذاری داده‌ها از دیتابیس SQL با ارسال کوئری  
  ```python
  import sqlite3
  conn = sqlite3.connect('database.db')
  df = pd.read_sql_query('SELECT * FROM table_name', conn)
  ```
  این روش برای استخراج داده‌های خاص از دیتابیس بسیار کاربردی است[3].

- **pd.read_table()**: بارگذاری فایل متنی با جداکننده دلخواه (مثلاً تب)  
  ```python
  df = pd.read_table('file.txt', sep='\t')
  ```

همچنین برای مشاهده سریع داده‌ها پس از بارگذاری می‌توانید از متدهای زیر استفاده کنید:  
- `df.head()` برای نمایش چند سطر اول  
- `df.info()` برای مشاهده اطلاعات کلی دیتافریم  
- `df.describe()` برای آمار توصیفی ستون‌های عددی[2][5].

