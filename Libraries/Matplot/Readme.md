## برخی از **توابع معروف کتابخانه Matplotlib** به همراه مثال‌های ساده در پایتون به شرح زیر است:

- **plt.plot()**  
  رسم نمودار خطی (Line Plot)  
  مثال:  
  ```python
  import matplotlib.pyplot as plt
  import numpy as np

  x = np.linspace(0, 10, 100)
  y = np.sin(x)
  plt.plot(x, y)
  plt.show()
  ```
  این کد نمودار تابع سینوس را رسم می‌کند[3].

- **plt.subplot()**  
  تقسیم صفحه رسم به چند بخش برای رسم چند نمودار در یک شکل  
  مثال:  
  ```python
  plt.subplot(2, 2, 1)
  plt.plot(x, x)
  plt.subplot(2, 2, 2)
  plt.plot(x, np.sin(x))
  plt.subplot(2, 2, 3)
  plt.plot(x, x**2)
  plt.subplot(2, 2, 4)
  plt.plot(x, np.cos(x))
  plt.show()
  ```
  این کد چهار نمودار مختلف را در یک پنجره 2 در 2 رسم می‌کند[2].

- **plt.bar()**  
  رسم نمودار میله‌ای (Bar Chart)  
  مثال:  
  ```python
  categories = ['A', 'B', 'C']
  values = [5, 7, 3]
  plt.bar(categories, values, color='lightblue')
  plt.show()
  ```
  این تابع برای نمایش مقایسه مقادیر دسته‌ای کاربرد دارد[6][7].

- **plt.pie()**  
  رسم نمودار دایره‌ای (Pie Chart)  
  مثال:  
  ```python
  slices = [3, 5, 2, 1]
  labels = ['Ali', 'Mohammad', 'Javad', 'Kaveh']
  colors = ['DeepPink', 'Crimson', 'MediumSeaGreen', 'Coral']
  plt.pie(slices, labels=labels, colors=colors)
  plt.show()
  ```
  این کد سهم هر نفر را در یک نمودار دایره‌ای نمایش می‌دهد[6].

- **plt.scatter()**  
  رسم نمودار پراکندگی (Scatter Plot) برای نمایش رابطه بین دو متغیر  
  مثال:  
  ```python
  x = np.random.rand(50)
  y = np.random.rand(50)
  plt.scatter(x, y)
  plt.show()
  ```
  این نمودار نقاط داده را به صورت پراکنده نمایش می‌دهد[4].

- **plt.boxplot()**  
  رسم نمودار جعبه‌ای (Box Plot) برای نمایش توزیع داده‌ها و شناسایی نقاط دورافتاده  
  مثال:  
  ```python
  data = [np.random.normal(size=100), np.random.normal(loc=1, size=100)]
  plt.boxplot(data)
  plt.show()
  ```
  این نمودار خلاصه‌ای از توزیع داده‌ها را نشان می‌دهد[7].

- **plt.style.use()**  
  انتخاب سبک ظاهری نمودار  
  مثال:  
  ```python
  plt.style.use('fivethirtyeight')
  plt.plot(x, y)
  plt.show()
  ```
  این کد سبک نمودار را به حالت fivethirtyeight تغییر می‌دهد[1].

این توابع پایه‌ای و پرکاربرد Matplotlib هستند که برای مصورسازی داده‌ها در پایتون استفاده می‌شوند و می‌توان با ترکیب آن‌ها نمودارهای متنوع و پیچیده‌تری ساخت.

[1] https://kiaraacademy.com/drawing-statistical-graphs-with-python/
[2] https://howsam.org/matplotlib-tutorial/
[3] https://7learn.com/blog/matplotlib-and-seaborn-library-tutorial
[4] https://blog.faradars.org/%D8%B1%D8%B3%D9%85-%D9%86%D9%85%D9%88%D8%AF%D8%A7%D8%B1-%D8%AF%D8%B1-%D9%BE%D8%A7%DB%8C%D8%AA%D9%88%D9%86-%D8%A8%D8%A7-matplotlib/
[5] https://rasanegaar.com/blog/%D8%AA%D8%AC%D8%B3%D9%85-%D8%AF%D8%A7%D8%AF%D9%87-%D9%87%D8%A7%DB%8C-%D9%BE%D8%A7%DB%8C%D8%AA%D9%88%D9%86-%D8%A8%D8%A7-matplotlib/
[6] https://sabzlearn.ir/blog/%D8%B1%D8%B3%D9%85-%D9%86%D9%85%D9%88%D8%AF%D8%A7%D8%B1-%D8%AF%D8%B1-%D9%BE%D8%A7%DB%8C%D8%AA%D9%88%D9%86/
[7] https://deeptip.ir/python-plotting-with-matplotlib/
[8] https://backendbaz.ir/python-drawing-intro-to-matplotlib-part-1/
[9] https://maktabkhooneh.org/mag/draw-functions-in-python/
[10] https://www.sourcebaran.com/learn/matplotlib_figure_class/
