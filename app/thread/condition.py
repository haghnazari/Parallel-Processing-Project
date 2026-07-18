import threading
import time
from datetime import datetime
import random
from threading import Thread


# سناریو 1: producer/consumer با buffer محدود
def condition_scenario1():
    output = []
    explanation = []

    items = []
    condition = threading.Condition()
    log_lock = threading.Lock()

    def log(msg):
        with log_lock:
            thread_name = threading.current_thread().name
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}   {thread_name:<10s} {msg}")

    class Consumer(Thread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def consume(self):
            with condition:
                if len(items) == 0:
                    log("no items to consume")
                    condition.wait()
                items.pop()
                log("consumed 1 item")
                condition.notify()

        def run(self):
            for i in range(20):
                time.sleep(2)
                self.consume()

    class Producer(Thread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def produce(self):
            with condition:
                if len(items) == 10:
                    log(f"items produced {len(items)}. Stopped")
                    condition.wait()
                items.append(1)
                log(f"total items {len(items)}")
                condition.notify()

        def run(self):
            for i in range(20):
                time.sleep(0.5)
                self.produce()

    start_time = time.time()

    t1 = Producer(name="Producer")
    t2 = Consumer(name="Consumer")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    exec_time = time.time() - start_time

    output.append("")
    output.append(f"Execution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 1: Producer/Consumer با Condition (طبق کتاب)")
    explanation.append("")
    explanation.append("Condition برای هماهنگی دو نخ بر اساس یک شرط استفاده می‌شود.")
    explanation.append("")
    explanation.append("شرط‌های این سناریو:")
    explanation.append("• اگر buffer خالی بود: Consumer منتظر می‌ماند")
    explanation.append("• اگر buffer پر بود (10 آیتم): Producer منتظر می‌ماند")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append(
        "1- condition.wait() قفل را موقتاً آزاد می‌کند و نخ را به حالت انتظار می‌برد"
    )
    explanation.append("2- condition.notify() یک نخ منتظر را بیدار می‌کند")
    explanation.append("3- نخ بیدار شده دوباره قفل را می‌گیرد و ادامه می‌دهد")
    explanation.append("")
    explanation.append("تفاوت با Semaphore:")
    explanation.append("• Semaphore: تعداد دسترسی همزمان را محدود می‌کند")
    explanation.append("• Condition: منتظر برقرار شدن یک شرط منطقی می‌ماند")
    explanation.append("")
    explanation.append("نکته داخلی از کتاب:")
    explanation.append("Condition به صورت خودکار یک RLock داخلی می‌سازد.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: ایستگاه هواشناسی با Condition
def condition_scenario2():
    output = []
    explanation = []

    TEMP_THRESHOLD = 35.0
    READINGS = 5

    condition = threading.Condition()
    log_lock = threading.Lock()

    alerts_queue = []
    active_sensors = 5

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    class Sensor(Thread):
        def __init__(self, city, base_temp):
            Thread.__init__(self)
            self.city = city
            self.name = f"Sensor-{city}"
            self.base_temp = base_temp

        def run(self):
            nonlocal active_sensors

            for i in range(READINGS):
                time.sleep(1)
                new_temp = round(
                    random.uniform(self.base_temp - 4, self.base_temp + 4), 1
                )

                log(f"{self.name:<20s}[{self.city}] ---> Temp: {new_temp}C")
                if new_temp > TEMP_THRESHOLD:
                    with condition:
                        alerts_queue.append((self.city, new_temp))
                        condition.notify_all()

            with condition:
                active_sensors -= 1
                if active_sensors == 0:
                    log("All sensors finished updates.")
                    condition.notify_all()

    class Monitor(Thread):
        def __init__(self, name, threshold):
            Thread.__init__(self)
            self.name = name
            self.threshold = threshold
            self.alerts = []

        def run(self):
            while True:
                is_alert, city, temp = False, None, None
                with condition:
                    while len(alerts_queue) == 0 and active_sensors > 0:
                        log(
                            f"{self.name:<20s}No Alert!. Monitor going to sleep..."
                        )
                        condition.wait()

                    if len(alerts_queue) == 0 and active_sensors == 0:
                        log(
                            f"{self.name:<20s}No sensors active and queue empty. Shutting down."
                        )
                        break

                    if alerts_queue:
                        city, temp = alerts_queue.pop(0)
                        is_alert = True

                if is_alert:
                    msg = f"{self.name:<20s}HIGH TEMP ALERT for {city}: {temp}C ----> Send SMS... "
                    self.alerts.append((city, temp))
                    log(msg)
                    time.sleep(random.uniform(0.1, 0.5))

    cities = [
        ("Aleshtar", 31),
        ("Shiraz", 35),
        ("Ahvaz", 38),
        ("Yazd", 36),
        ("Tehran", 32),
    ]

    output.append("=" * 70)
    output.append("WEATHER STATION - Condition")
    output.append("=" * 70)

    monitors = [
        Monitor("Monitor-A", TEMP_THRESHOLD),
        Monitor("Monitor-B", TEMP_THRESHOLD),
    ]
    sensors = [Sensor(city, base_temp) for city, base_temp in cities]

    all_threads = monitors + sensors

    for t in all_threads:
        t.start()
    for t in all_threads:
        t.join()

    output.append("\n" + "=" * 70)
    output.append("FINAL REPORT")
    output.append("=" * 70)
    output.append(f"  Monitor-A total alerts: {len(monitors[0].alerts)}")
    output.append(f"  Monitor-B total alerts: {len(monitors[1].alerts)}")

    explanation.append("سناریو 2: ایستگاه هواشناسی با Condition")
    explanation.append("")
    explanation.append("5 سنسور دما را اندازه می‌گیرند.")
    explanation.append("2 مانیتور منتظر هشدارهای دمای بالا می‌مانند.")
    explanation.append("")
    explanation.append("شرط این سناریو:")
    explanation.append(
        f"  new_temp > {TEMP_THRESHOLD}C  ->  هشدار به صف اضافه می‌شود و مانیتورها notify می‌شوند"
    )
    explanation.append(
        f"  new_temp <= {TEMP_THRESHOLD}C ->  فقط لاگ می‌شود، notify نمی‌شود"
    )
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append(
        "1- مانیتورها از ابتدا منتظرند: صف خالی است پس condition.wait() می‌زنند"
    )
    explanation.append(
        "2- سنسور دمای بالا اندازه می‌گیرد، هشدار را به alerts_queue اضافه می‌کند"
    )
    explanation.append("3- condition.notify_all() هر دو مانیتور را بیدار می‌کند")
    explanation.append("4- مانیتوری که اول قفل می‌گیرد هشدار را از صف برمی‌دارد")
    explanation.append(
        "5- مانیتور دوم بیدار می‌شود، صف را خالی می‌بیند، دوباره می‌خوابد"
    )
    explanation.append("")
    explanation.append("حل مشکل Missed Signal:")
    explanation.append(
        "اگر مانیتور دیر بیدار شود، هشدار در alerts_queue محفوظ مانده است."
    )
    explanation.append(
        "برخلاف روش ساده notify که اگر هیچ نخی منتظر نبود signal از دست می‌رفت."
    )
    explanation.append("")
    explanation.append("چرا از while به جای if در wait استفاده شد؟")
    explanation.append(
        "notify_all() هر دو مانیتور را بیدار می‌کند ولی فقط یک هشدار در صف است."
    )
    explanation.append(
        "مانیتور دوم بعد از بیدار شدن دوباره شرط را بررسی می‌کند و می‌بیند صف خالی است."
    )
    explanation.append("")
    explanation.append("پایان کار:")
    explanation.append(
        "وقتی آخرین سنسور تمام می‌کند active_sensors=0 می‌شود و notify_all می‌زند."
    )
    explanation.append(
        "مانیتورها بیدار می‌شوند، می‌بینند صف خالی و سنسوری فعال نیست، خاموش می‌شوند."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: سیستم رزرو بلیط
def condition_scenario3():
    output = []
    explanation = []

    TOTAL_SEATS = 5
    TOTAL_USERS = 10

    condition = threading.Condition()
    log_lock = threading.Lock()

    available_seats = TOTAL_SEATS
    active_users = TOTAL_USERS
    seat_counter = [0]
    system_open = True

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    class User(Thread):

        def __init__(self, name, hold_duration, will_cancel):
            Thread.__init__(self)
            self.name = name
            self.hold_duration = hold_duration
            self.will_cancel = will_cancel
            self.seat = None
            self.status = "waiting"

        def run(self):
            nonlocal available_seats, active_users, system_open

            with condition:
                while available_seats == 0 and system_open:
                    log(f"{self.name:<20s}No seats available. Waiting ...")
                    condition.wait()

                if not system_open:
                    self.status = "rejected"
                    log(f"{self.name:<20s}System closed. Could not get a ticket.")
                    active_users -= 1
                    return

                available_seats -= 1
                seat_counter[0] += 1
                self.seat = seat_counter[0]
                self.status = "booked"
                log(
                    f"{self.name:<20s}Booked seat #{self.seat:<2d} "
                    f"(remaining: {available_seats}/{TOTAL_SEATS})"
                )

            time.sleep(self.hold_duration)

            with condition:
                if self.will_cancel:
                    available_seats += 1
                    self.status = "cancelled"
                    log(
                        f"{self.name:<20s}Cancelled seat #{self.seat:<2d} "
                        f"(remaining: {available_seats}/{TOTAL_SEATS})"
                    )
                    
                    condition.notify()
                else:
                    self.status = "used"
                    log(f"{self.name:<20s}Used seat #{self.seat:<2d} and left.")

                active_users -= 1

                booked_count = len([u for u in users if u.status == "booked"])
                if available_seats == 0 and booked_count == 0 and active_users > 0:
                    system_open = False
                    log(
                        "No active ticket-holders left to release seats. Closing system."
                    )
                    condition.notify_all()

                if active_users == 0:
                    system_open = False
                    log("All users processed. System closed.")
                    condition.notify_all()

    cancel_flags = [random.random() < 0.3 for _ in range(TOTAL_USERS)]

    users = [
        User(
            name=f"User-{i:02d}",
            hold_duration=round(random.uniform(1.0, 2.5), 1),
            will_cancel=cancel_flags[i - 1],
        )
        for i in range(1, TOTAL_USERS + 1)
    ]

    output.append("=" * 70)
    output.append("TICKET BOOKING SYSTEM - Condition")
    output.append("=" * 70)
    output.append(f"  Total seats    : {TOTAL_SEATS}")
    output.append(f"  Total users    : {TOTAL_USERS}")
    output.append("  Cancel chance  : 30%")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    for u in users:
        u.start()

    for u in users:
        u.join()

    exec_time = time.time() - start_time

    booked = [u for u in users if u.status in ("booked", "used", "cancelled")]
    cancelled = [u for u in users if u.status == "cancelled"]
    used = [u for u in users if u.status == "used"]
    rejected = [u for u in users if u.status == "rejected"]

    output.append("")
    output.append("=" * 70)
    output.append("FINAL REPORT")
    output.append("=" * 70)
    output.append(f"  Total booked   : {len(booked)}")
    output.append(f"  Used           : {len(used)}")
    output.append(f"  Cancelled      : {len(cancelled)}")
    output.append(f"  Rejected       : {len(rejected)}")
    output.append(f"  Execution time : {exec_time:.3f} seconds")
    output.append("=" * 70)


    explanation.append("=" * 70)
    explanation.append(
        "سناریو ۳: سیستم رزرو بلیط با condition"
    )
    explanation.append("=" * 70)
    explanation.append(
        "۱. شبیه‌سازی الگوی تولیدکننده/مصرف‌کننده با منبع محدود (Bounded Resource):"
    )
    explanation.append(
        "   صندلی‌ها (TOTAL_SEATS) به عنوان یک شمارنده محدود رفتار می‌کنند. هر نخ قبل از مصرف"
    )
    explanation.append(
        "   باید وضعیت منبع را بررسی کند. متغیر شرطی (Condition) نقش ناظر صف را"
    )
    explanation.append(
        "   بازی می‌کند تا از ورود غیرمجاز نخ‌ها در زمان پُر بودن ظرفیت جلوگیری کند."
    )
    explanation.append("-" * 70)
    explanation.append(
        "   * در زمان کنسل شدن بلیط: از notify() استفاده شده است؛ چرا که دقیقاً 'یک' صندلی"
    )
    explanation.append(
        "     آزاد شده است. بیدار کردن تمام کاربران صف (notify_all) منجر به وقوع پدیده"
    )
    explanation.append(
        "     Thundering Herd (هجوم گله‌ای نخ‌ها) و اتلاف شدید سیکل‌های CPU برای قفل و خواب مجدد می‌شد."
    )
    explanation.append(
        "   * در زمان بسته شدن سیستم: از notify_all() استفاده می‌شود تا تمام کاربرانِ جا مانده"
    )
    explanation.append(
        "     در صف انتظار، همزمان بیدار شده، شرط خروج (system_open == False) را لمس کرده و خارج شوند."
    )
    explanation.append("-" * 70)
    explanation.append("۳. کالبدشکافی و پیشگیری از بن‌بست نهایی (Deadlock Prevention):")
    explanation.append(
        "   یکی از پیچیده‌ترین باگ‌های این سناریو، گیر افتادن کاربرانِ صف در صورت عدم کنسل شدن"
    )
    explanation.append(
        "   بلیط‌های اولیه بود. با تعبیه شرط داینامیک خروج امن، سیستم به طور خودکار تشخیص می‌دهد"
    )
    explanation.append(
        "   که چه زمانی دیگر هیچ نخ بیداری در فضای کاربری وجود ندارد تا قفل صندلی‌ها را باز کند؛"
    )
    explanation.append(
        "   در نتیجه با شلیک یک notify_all عمومی، صف انتظار را به طور امن پاکسازی (Flush) می‌کند."
    )
    explanation.append("=" * 70)

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_condition_scenario(scenario_id: int):
    scenarios = {
        1: condition_scenario1,
        2: condition_scenario2,
        3: condition_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
