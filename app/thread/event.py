import random
import threading
import time
from datetime import datetime
from threading import Thread


# سناریو 1: سیستم تولیدکننده و مصرف‌کننده با Event
def event_scenario1():
    output = []
    explanation = []

    items = []
    event = threading.Event()
    lock = threading.Lock()
    log_lock = threading.Lock()
    producer_alive = True

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    class Consumer(Thread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def run(self):
            while True:
                time.sleep(1)
                event.wait()

                with lock:
                    item = items.pop(0)
                    log(
                        f"{self.name:<11s}INFO   Consumer notify: {item:<3d} popped by {self.name:<17s} --> (Queue size: {len(items)})"
                    )

                if not producer_alive and len(items) == 0:
                    log(
                        f"\n{self.name:<11s}No more items and Producer finished. Exiting...\n"
                    )
                    break

    class Producer(Thread):
        def run(self):
            nonlocal producer_alive
            for _ in range(5):
                time.sleep(1)
                item = random.randint(10, 99)

                with lock:
                    items.append(item)
                    log(
                        f"{self.name:<11s}INFO   Producer notify: item {item:<3d} appended by {self.name:<10s} --> (Queue size: {len(items)})"
                    )

                event.set()
                event.clear()

            with lock:
                producer_alive = False
                log(f"\n{self.name:<11s}Producer finished all generations.\n")
                event.set()  # اجبارا اضافه کردم تا مصرف کننده به خواب ابدی نره

    output.append("PRODUCER / CONSUMER - Event Signaling")
    output.append("=" * 70)

    t1 = Producer()
    t2 = Consumer()

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    explanation.append("=" * 70)
    explanation.append("سناریو 1: همگام‌سازی با استفاده از Event")
    explanation.append("")
    explanation.append("تحلیل رفتار (Event) در کد کتاب")
    explanation.append(
        "   تولیدکننده با متد set() چراغ را برای عبور نخ مصرف‌کننده باز می‌کند و مصرف‌کننده"
    )
    explanation.append(
        "   توسط متد wait() پشت این چراغ منتظر تغییر وضعیت سیستم می‌ماند."
    )
    explanation.append("")
    explanation.append(
        "   در کد کتاب، بلافاصله پس از متد event.set()، دستور event.clear() صادر شده است."
    )
    explanation.append(
        "   چون سرعت تغییر خطوط توسط پردازنده در حد میکروثانیه است، فرستادن و پاک کردن سیگنال"
    )
    explanation.append(
        "   پشت سر هم رخ می‌دهد؛ در نتیجه اگر زمان‌بندی (Timing) مصرف‌کننده ذره‌ای عقب بیفتد،"
    )
    explanation.append(
        "   سیگنال را از دست داده (Missed Signal) و برنامه در همان گام‌های اول قفل (Deadlock) می‌کند."
    )
    explanation.append("-" * 70)
    explanation.append(
        "   در فاز پایانی، پس از اینکه نخ Producer کل ۵ آیتم خود را تولید کرد و مرد،"
    )
    explanation.append(
        "   نخ Consumer ممکن است همچنان خطِ نهایی wait() را لمس کند و به خواب ابدی برود."
    )
    explanation.append(
        "   با اضافه کردن دستور 'event.set()' در انتهای متد run تولیدکننده،"
    )
    explanation.append(
        "   یک بیدارباش اجباری صادر کردیم تا مصرف‌کننده بیدار شده، شرط خروج را ارزیابی کند و خارج شود."
    )
    explanation.append("-" * 70)
    explanation.append("نقش قفل (lock):")
    explanation.append(
        "   کد اصلی کتاب از یک لیست معمولی پایتون بدون قفل استفاده کرده بود که برای مالتی‌تردینگ امن نیست."
    )
    explanation.append(
        "   در این کد، با تعبیه 'with lock' دور متدهای append و pop، تداخل حافظه (Race Condition)"
    )
    explanation.append("   روی منابع مشترک به طور کامل ریشه‌کن و مهار شده است.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: مدیریت دانلود چندبخشی با Event
def event_scenario2():
    output = []
    explanation = []

    internet_ready = threading.Event()
    log_lock = threading.Lock()

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    class DownloadWorker(Thread):
        def __init__(self, part_name):
            Thread.__init__(self)
            self.name = part_name

        def run(self):
            log(f"{self.name:<15s}Initialized. Waiting for internet...")
            internet_ready.wait()
            log(f"{self.name:<15s}Internet connected! Starting download...")
            download_time = round(random.uniform(0.2, 1), 1)
            time.sleep(download_time)
            log(f"{self.name:<15s}Download finished in {download_time}s.")

    class NetworkMonitor(Thread):
        def run(self):
            log(f"{'Network':<15s}Checking connection status...")
            time.sleep(2)

            log(f"{'Network':<15s}Internet is now STABLE. Signaling all parts.")
            internet_ready.set()

    output.append("=" * 70)
    output.append("MULTI-PART DOWNLOADER - Event Broadcasting")
    output.append("=" * 70)

    downloaders = [
        DownloadWorker("Part-01"),
        DownloadWorker("Part-02"),
        DownloadWorker("Part-03"),
    ]
    monitor = NetworkMonitor()

    for d in downloaders:
        d.start()
    monitor.start()

    for d in downloaders:
        d.join()
    monitor.join()

    output.append("\nDOWNLOAD COMPLETION SUCCESSFUL")

    explanation.append("=" * 70)
    explanation.append("سناریو ۲: سیستم دانلود چندبخشی")
    explanation.append("=" * 70)
    explanation.append("۱. مکانیزم انتشار عمومی (Broadcasting):")
    explanation.append(
        "   این سناریو قدرت واقعی Event را نشان می‌دهد. برعکس ابزار قفل یا Condition"
    )
    explanation.append(
        "   که معمولاً فقط یک نخ را بیدار می‌کردند، متد set() در اینجا به طور همزمان"
    )
    explanation.append(
        "   تمام ۳ نخ دانلودر (Part 1, 2, 3) را که پشت خط wait() خوابیده بودند بیدار می‌کند."
    )

    explanation.append(
        "   در این معماری نیازی به اجرای دستور clear() بلافاصله بعد از set() نیست؛ چرا که"
    )
    explanation.append(
        "   هدف ما این است که وضعیت اینترنت تا پایان دانلودِ همه پارت‌ها 'سبز' (True) باقی بماند."
    )
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: چراغ راهنمایی هوشمند
def event_scenario3():
    output = []
    explanation = []

    green_light = threading.Event()
    log_lock = threading.Lock()

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    class Car(Thread):
        def __init__(self, name, arrival_time):
            Thread.__init__(self)
            self.car_name = name
            self.arrival_time = arrival_time
            self.waited = False

        def run(self):
            time.sleep(self.arrival_time)
            log(f"{self.car_name:<8s} arrived.")

            if not green_light.is_set():
                self.waited = True
                log(f"{self.car_name:<8s} light is RED   -- waiting...")
                green_light.wait()

            log(f"{self.car_name:<8s} light is GREEN -- crossing...")
            time.sleep(0.2)
            log(f"{self.car_name:<8s} passed")

    class TrafficController(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.name = "Controller"

        def run(self):
            log(f"{self.name:<8s} Traffic Light = RED   (phase 1)")
            time.sleep(2)

            log(f"{self.name:<8s} Traffic Light = GREEN (phase 1) -- event.set()")
            green_light.set()
            time.sleep(2)

            log(f"{self.name:<8s} Traffic Light = RED   (phase 2) -- event.clear()")
            green_light.clear()
            time.sleep(2)

            log(f"{self.name:<8s} Traffic Light = GREEN (phase 2) -- event.set()")
            green_light.set()

    cars = [
        Car("Car-1", arrival_time=1),
        Car("Car-2", arrival_time=1.5),
        Car("Car-3", arrival_time=3),
        Car("Car-4", arrival_time=4.5),
        Car("Car-5", arrival_time=5),
        Car("Car-6", arrival_time=6),
    ]

    output.append("SMART TRAFFIC LIGHT - Event")

    controller = TrafficController()
    start_time = time.time()

    controller.start()
    for car in cars:
        car.start()

    controller.join()
    for car in cars:
        car.join()

    exec_time = time.time() - start_time

    waited_cars = [c for c in cars if c.waited]
    instant_cars = [c for c in cars if not c.waited]

    output.append("")
    output.append("=" * 70)
    output.append("FINAL REPORT")
    output.append("=" * 70)
    output.append(f"  Total cars               : {len(cars)}")
    output.append(f"  Waited at red light      : {[c.car_name for c in waited_cars]}")
    output.append(f"  Passed without waiting   : {[c.car_name for c in instant_cars]}")
    output.append(f"  Execution time           : {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 3: چراغ راهنمایی هوشمند با Event")
    explanation.append("")
    explanation.append("TrafficController چراغ را کنترل می‌کند.")
    explanation.append("هر ماشین در زمان مشخصی می‌رسد و وضعیت چراغ را بررسی می‌کند.")
    explanation.append("")
    explanation.append("نحوه عملکرد event:")
    explanation.append(
        "  green_light.set()   : چراغ سبز  -- همه ماشین‌های منتظر همزمان رد می‌شوند"
    )
    explanation.append(
        "  green_light.clear() : چراغ قرمز -- event.wait() از این پس بلاک می‌کند"
    )
    explanation.append(
        "  green_light.wait()  : اگر سبز بود فوری رد می‌شود، اگر قرمز بود منتظر می‌ماند"
    )
    explanation.append("")
    explanation.append("سه حالت مختلف در این سناریو:")
    explanation.append("")
    explanation.append("حالت 1 - Car-1 و Car-2 (قرمز دور اول):")
    explanation.append("  چراغ قرمز است، event.wait() بلاک می‌کند.")
    explanation.append("  با set() هر دو همزمان بیدار و رد می‌شوند.")
    explanation.append("")
    explanation.append("حالت 2 - Car-3 (سبز دور اول):")
    explanation.append("  ماشین در زمان سبز می‌رسد.")
    explanation.append("  event از قبل set شده، wait() اصلاً بلاک نمی‌کند.")
    explanation.append("  بلافاصله رد می‌شود.")
    explanation.append("")
    explanation.append("حالت 3 - Car-4 (بعد از قرمز شدن):")
    explanation.append("  ماشین بعد از لحظه clear() می‌رسد و  دور دوم تا سبز شدن را انتظار می‌کشد.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}



# *************************************************************
def run_event_scenario(scenario_id: int):
    scenarios = {
        1: event_scenario1,
        2: event_scenario2,
        3: event_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
