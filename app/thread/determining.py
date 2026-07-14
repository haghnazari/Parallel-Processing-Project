import threading
import time
import random


# سناریو 1: نمایش نام نخ جاری
def determining_scenario1():
    output = []
    explanation = []

    def function_A():
        # threading.current_thread().name
        output.append(threading.currentThread().getName() + "--> starting \n")
        time.sleep(2)
        output.append(threading.currentThread().getName() + "--> exiting \n")

    def function_B():
        output.append(threading.currentThread().getName() + "--> starting \n")
        time.sleep(2)
        output.append(threading.currentThread().getName() + "--> exiting \n")

    def function_C():
        output.append(threading.currentThread().getName() + "--> starting \n")
        time.sleep(2)
        output.append(threading.currentThread().getName() + "--> exiting \n")

    t1 = threading.Thread(name="function_A", target=function_A)
    t2 = threading.Thread(name="function_B", target=function_B)
    t3 = threading.Thread(name="function_C", target=function_C)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    explanation.append("سناریو 1: نمایش نام نخ جاری")
    explanation.append("")
    explanation.append(
        "استفاده از آرگومان‌ها برای شناسایی یا نام‌گذاری نخ، دشوار و غیرضروری است."
    )
    explanation.append(
        "هر نمونه از کلاس Thread یک نام با مقدار پیش‌فرض(Thread-1, Thread-2, ...) دارد که می‌تواند هنگام ایجاد نخ تغییر کند."
    )
    explanation.append("")
    explanation.append(
        "این سناریو نحوه تشخیص و نمایش نام نخ در حال اجرا را نشان می‌دهد:"
    )
    explanation.append("")
    explanation.append("1. هر نخ با یک نام سفارشی ایجاد می‌شود (name='function_A')")
    explanation.append(
        "2.  در داخل تابع، با threading.currentThread().getName() نام نخ جاری را می‌گیریم"
    )
    explanation.append("3.  سپس این نام در خروجی نمایش داده می‌شود")
    explanation.append("4. همه نخ‌ها به صورت همزمان شروع می‌شوند")
    explanation.append("")
    explanation.append("نکته مهم:")
    explanation.append(
        "threading.currentThread().getName() نام نخ جاری را برمی‌گرداند."
    )
    explanation.append("البته این متد در نسخه های جدید پایتون deprecate شده است.")
    explanation.append(
        "در نسخه‌های جدیدتر پایتون، threading.current_thread().name توصیه می‌شود"
    )
    explanation.append("")
    explanation.append(
        "توجه: ترتیب شروع و پایان نخ‌ها ممکن است در هر بار اجرا متفاوت باشد"
    )
    explanation.append("زیرا زمان‌بندی نخ‌ها توسط سیستم عامل انجام می‌شود.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: ثبت لاگ در برنامه‌های چندنخی
def determining_scenario2():
    output = []
    explanation = []

    def process_request(user_id):
        thread_name = threading.current_thread().name
        output.append(f"[{thread_name}] Processing request for User-{user_id}")
        time.sleep(random.uniform(0.5, 1.5))
        output.append(f"[{thread_name}] Request completed")

    threads = []
    for i in range(5):
        t = threading.Thread(
            target=process_request, args=(i + 1,), name=f"Request-{i+1}"
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    explanation.append("سناریو 2: ثبت لاگ در برنامه‌های چندنخی")
    explanation.append("")
    explanation.append(
        "در سرورها و برنامه‌های شبکه‌ای چندین درخواست به طور همزمان پردازش می‌شوند."
    )
    explanation.append(
        "برای اشکال‌زدایی و ثبت لاگ باید بدانیم هر پیام متعلق به کدام نخ است."
    )
    explanation.append("")
    explanation.append("1. هر نخ نماینده یک درخواست کاربر است")
    explanation.append("2. نام نخ در لاگ ثبت می‌شود")
    explanation.append(
        "3. در صورت بروز خطا می‌توان فهمید مشکل مربوط به کدام درخواست بوده است"
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: پردازش موازی تعدادی تصویر توسط چند نخ
def determining_scenario3():
    output = []
    explanation = []

    tasks = ["Image_1.jpg", "Image_2.jpg", "Image_3.jpg", "Image_4.jpg", "Image_5.jpg"]

    def worker(task):
        worker_name = threading.current_thread().name
        output.append(f"{worker_name} started processing {task}")
        time.sleep(random.uniform(0.1, 1.0))
        output.append(f"{worker_name} finished processing {task}")

    threads = []
    for i, task in enumerate(tasks):
        t = threading.Thread(target=worker, args=(task,), name=f"Worker-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    explanation.append("سناریو 3: پردازش موازی تعدادی تصویر توسط چند نخ")
    explanation.append("")
    explanation.append(
        "1- برای هر تصویر یک نخ با نام مشخص (Worker-1 ،Worker-2 و ...) ایجاد می‌شود."
    )
    explanation.append(
        "هر Worker هنگام شروع کار، نام خود را با استفاده از threading.current_thread().name دریافت می‌کند."
    )
    explanation.append(
        "3- سپس در لاگ ثبت می‌شود که کدام Worker مسئول پردازش کدام تصویر بوده است."
    )
    explanation.append("4- پس از پایان پردازش نیز نام Worker دوباره در خروجی نمایش داده می‌شود.")
    explanation.append("")
    explanation.append("مزیت استفاده از نام نخ‌ها:")
    explanation.append("• در سیستم‌های بزرگ ممکن است ده‌ها یا صدها نخ همزمان فعال باشند.")
    explanation.append("• با ثبت نام نخ در لاگ‌ها می‌توان فهمید هر وظیفه توسط کدام Worker انجام شده است.")
    explanation.append("• در صورت بروز خطا یا کاهش کارایی، شناسایی نخ مسئول بسیار ساده‌تر خواهد بود.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_determining_scenario(scenario_id: int):
    scenarios = {
        1: determining_scenario1,
        2: determining_scenario2,
        3: determining_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
