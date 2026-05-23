# 🧵⚙️ گزارش پروژه پایانی درس پردازش موازی

# Parallel Processing Project : LU 1404-2


## 📌 اطلاعات کلی

| **نام پروژه** | Parallel Processing Project |
| ------------- | --------------------------- |
| **درس**       | پردازش موازی                |
| **دانشجو**    | سعید حق نظری                |
| **استاد**     | دکتر آرمین رشنو             |
| **دانشگاه**   | دانشگاه لرستان              |
| **ترم**       | بهار 1405                   |

---

## 📌 معرفی پروژه
پروژه **پردازش موازی** یک وب‌اپلیکیشن تعاملی برای آموزش و نمایش مفاهیم **همگام‌سازی(Synchronization)** در برنامه‌نویسی چندنخی و چندفرایندی است.
این پروژه با استفاده از **FastAPI** در بک‌اند و **HTML/CSS/JavaScript** در فرانت‌اند پیاده‌سازی شده است.

## 🎯 اهداف پروژه
1. **آموزش مفاهیم همگام‌سازی** در برنامه‌نویسی
2. **مقایسه ابزارهای مختلف** همگام‌سازی (Lock, RLock, Semaphore, ...)
3. **نمایش Race Condition** و روش‌های جلوگیری از آن
4. **شبیه‌سازی سناریوهای واقعی** مانند سیستم بانکی
5. **ایجاد یک محیط تعاملی** برای تست و یادگیری



## 📋 لیست کامل روش‌ها و ابزارهای همگام‌سازی

---
## 🧵 بخش اول: روش نخ (Thread-Based Parallelism)

### دسته اول: تعریف و مدیریت نخ

|شماره|ابزار|توضیح|
|---|---|---|
|1|**Defining a thread**|تعریف و ایجاد یک نخ ساده|
|2|**Determining the current thread**|تشخیص و نمایش نخ جاری|
|3|**Defining a thread subclass**|تعریف نخ با استفاده از زیرکلاس|

---

### دسته دوم: همگام‌سازی نخ (Synchronization)

|شماره|ابزار|توضیح|
|---|---|---|
|4|**Lock**|قفل ساده - دسترسی انحصاری به منابع|
|5|**RLock**|قفل قابل بازگشت (Reentrant Lock)|
|6|**Semaphore**|سمافور - کنترل تعداد دسترسی‌های همزمان|
|7|**Condition**|شرط - هماهنگی بر اساس رویدادها|
|8|**Event**|رویداد - علامت‌دهی بین نخ‌ها|
|9|**Barrier**|مانع - همگام‌سازی گروهی نخ‌ها|

---
### دسته سوم: ارتباط بین نخ‌ها

|شماره|ابزار|توضیح|
|---|---|---|
|10|**Queue**|صف - تبادل داده بین نخ‌ها|

---

### خلاصه ابزارهای نخ (Thread)

```text

Thread-Based Parallelism
├── Defining a thread
├── Determining the current thread
├── Defining a thread subclass
├── Thread synchronization with a lock
├── Thread synchronization with RLock
├── Thread synchronization with semaphores
├── Thread synchronization with a condition
├── Thread synchronization with an event
├── Thread synchronization with a barrier
└── Thread communication using a queue
```

---

## ⚙️ بخش دوم: روش فرایند (Process-Based Parallelism)

### دسته اول: ایجاد و مدیریت فرایند

|شماره|ابزار|توضیح|
|---|---|---|
|1|**Spawning a process**|ایجاد و اجرای یک فرایند جدید|
|2|**Naming a process**|نام‌گذاری فرایندها|
|3|**Running processes in the background**|اجرای فرایندها در پس‌زمینه|
|4|**Killing a process**|متوقف کردن (کشتن) یک فرایند|
|5|**Defining processes in a subclass**|تعریف فرایند در زیرکلاس|

---

### دسته دوم: ارتباط بین فرایندها

|شماره|ابزار|توضیح|
|---|---|---|
|6|**Using a queue to exchange data**|استفاده از صف برای تبادل داده|
|7|**Using pipes to exchange objects**|استفاده از پایپ برای تبادل اشیاء|

---

### دسته سوم: همگام‌سازی و مدیریت فرایند

|شماره|ابزار|توضیح|
|---|---|---|
|8|**Synchronizing processes**|همگام‌سازی فرایندها با قفل|
|9|**Using a process pool**|استفاده از استخر فرایند (Process Pool)|

---

### خلاصه ابزارهای فرایند (Process)

```text

Process-Based Parallelism
├── Spawning a process
├── Naming a process
├── Running processes in the background
├── Killing a process
├── Defining processes in a subclass
├── Using a queue to exchange data
├── Using pipes to exchange objects
├── Synchronizing processes
└── Using a process pool
```
---

## 📊 جدول مقایسه روش نخ و فرایند

|ویژگی|نخ (Thread)|فرایند (Process)|
|---|---|---|
|**حافظه**|مشترک|جداگانه|
|**ارتباط**|آسان (از طریق حافظه مشترک)|دشوار (نیاز به IPC)|
|**ایجاد**|سریع و سبک|کند و سنگین|
|**GIL**|محدودیت دارد|ندارد|
|**مناسب برای**|I/O-bound|CPU-bound|
|**Race Condition**|❌ خطرناک|✅ ایزوله|
|**همگام‌سازی**|Lock, RLock, Semaphore, ...|Queue, Pipe, Lock|

---

## 📚 ساختار پروژه

```tree
ParallelProcessingProject/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI endpoints
│   ├── lock.py              # سناریوهای Lock
│   ├── rlock.py             # سناریوهای RLock (در آینده)
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js
│   │   ├── tools.js
│   │   ├── scenarios.js
│   │   └── scenario_codes.js
│   └── index.html
├── requirements.txt
├── .gitignore
└── README.md
```





## 🔒 سناریوهای Lock

### سناریو 1: Race Condition

**هدف:** نمایش تداخل نخ‌ها در دسترسی به متغیر مشترک بدون قفل

**کد اصلی:**

```python
def lock_scenario1():
    counter = 0
    class CounterThread(Thread):
        def run(self):
            nonlocal counter
            temp = counter
            time.sleep(0.0001)
            counter = temp + 1
```


**خروجی:** مقدار نهایی counter کمتر از 10 است

**نکته آموزشی:** این سناریو نشان می‌دهد که بدون قفل، نخ‌ها با هم تداخل می‌کنند و برخی افزایش‌ها از دست می‌روند.



### سناریو 2: همگام‌سازی با Lock

**هدف:** حل مشکل Race Condition با استفاده از قفل

**کد اصلی:**
```python
def lock_scenario2():
    threadLock = threading.Lock()
    class CounterThread(Thread):
        def run(self):
	        nonlocal counter
            threadLock.acquire()
            temp = counter
            time.sleep(0.0001)
            counter = temp + 1
            threadLock.release()
```

**خروجی:** مقدار نهایی counter = 10

**نکته آموزشی:** قفل تضمین می‌کند که هر بار فقط یک نخ به متغیر مشترک دسترسی دارد.

### سناریو 3: شبیه‌سازی سیستم بانکی

**هدف:** کاربرد عملی Lock در دنیای واقعی

**کد اصلی:**
```python
def lock_scenario3():
    bank_lock = threading.Lock()
    balance = 1000  # Initial account balance
    output = []
    transaction_count = 0
    failed_transactions = 0
    
    class BankTransaction(Thread):
        def __init__(self, name, amount, transaction_type):
            Thread.__init__(self)
            self.name = name
            self.amount = amount
            self.transaction_type = transaction_type  # "Deposit" or "Withdraw"
        
        def run(self):
            nonlocal balance, transaction_count, failed_transactions
            bank_lock.acquire()
            old_balance = balance
            output.append(f"START    ----> {self.name}: type={self.transaction_type}, amount={self.amount}, balance_before={old_balance}")
            time.sleep(0.01)
            if self.transaction_type == "Deposit":
                balance += self.amount
                output.append(f"DEPOSIT ----> {self.name}: +{self.amount} | new_balance={balance}")
                transaction_count += 1
                
            elif self.transaction_type == "Withdraw":
                if balance >= self.amount:
                    balance -= self.amount
                    output.append(f"WITHDRAW ----> {self.name}: -{self.amount} | new_balance={balance}")
                    transaction_count += 1
                else:
                    output.append(f"REJECTED ----> {self.name}: withdraw {self.amount} FAILED! (insufficient balance: {balance})")
                    failed_transactions += 1       
            time.sleep(0.005)
            output.append(f"END      ----> {self.name}: Final_balance={balance}\n")
            bank_lock.release()
    
    # ایجاد تراکنش‌های تصادفی
    transactions = []
    for i in range(10):
        amount = randint(300, 800)
        ta = ["Deposit", "Withdraw"][randint(0,1)]
        t = BankTransaction(f"{ta}#{i+1}", amount, ta)
        transactions.append(t)
    
    for t in transactions:
        t.start()
    
    for t in transactions:
        t.join()
```

**ویژگی‌ها:**

- ✅ تراکنش‌های همزمان (واریز و برداشت)
    
- ✅ بررسی موجودی قبل از برداشت
    
- ✅ نمایش تراکنش‌های ناموفق
    
- ✅ نمایش موجودی قبل و بعد از هر تراکنش


**خروجی نمونه:**
```text
START    ----> Deposit#1: type=Deposit, amount=350, balance_before=1000
DEPOSIT ----> Deposit#1: +350 | new_balance=1350
END      ----> Deposit#1: Final_balance=1350

START    ----> Withdraw#1: type=Withdraw, amount=500, balance_before=1350
WITHDRAW ----> Withdraw#1: -500 | new_balance=850
END      ----> Withdraw#1: Final_balance=850

START    ----> Withdraw#2: type=Withdraw, amount=700, balance_before=850
REJECTED ----> Withdraw#2: withdraw 700 FAILED! (insufficient balance: 850)
END      ----> Withdraw#2: Final_balance=850
```

**نکته آموزشی:** این سناریو کاربرد واقعی Lock در سیستم‌های بانکی، صف‌های خرید، رزرو بلیط و انبارداری را نشان می‌دهد.
