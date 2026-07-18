import threading
import time
import random


# سناریو 1: producer/consumer با سمافور
def semaphore_scenario1():
    output = []
    explanation = []

    semaphore = threading.Semaphore(0)
    item = 0
    log_lock = threading.Lock()

    def log(msg):
        with log_lock:
            thread_name = threading.current_thread().name
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S,%MS")
            output.append(f"{timestamp}   {thread_name:<10s} INFO   {msg}")

    def consumer():
        log("Consumer is waiting")
        semaphore.acquire()
        log(f"Consumer notify: item number {item}")

    def producer():
        nonlocal item
        time.sleep(3)
        item = random.randint(0, 1000)
        log(f"Producer notify: item number {item}")
        semaphore.release()

    start_time = time.time()

    for i in range(5):
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    exec_time = time.time() - start_time

    output.append(f"\nExecution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 1: Producer/Consumer با سمافور (طبق کتاب)")
    explanation.append("")
    explanation.append("سمافور با مقدار اولیه 0 برای هماهنگی دو نخ استفاده می‌شود.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- سمافور با مقدار 0 شروع می‌کند")
    explanation.append("2- Consumer منتظر می‌ماند: semaphore.acquire()")
    explanation.append("   چون مقدار 0 است، نخ مسدود (block) می‌شود")
    explanation.append("3- Producer آیتم تولید می‌کند: semaphore.release()")
    explanation.append("   مقدار سمافور 1 می‌شود")
    explanation.append("4- Consumer از حالت انتظار خارج می‌شود و آیتم را مصرف می‌کند")
    explanation.append("")
    explanation.append(
        "این نوع سمافور Semaphore(0) نام دارد و برای سیگنال‌دهی بین نخ‌ها استفاده می‌شود."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: پارکینگ با ظرفیت محدود
def semaphore_scenario2():
    output = []
    explanation = []

    CAPACITY = 3

    class Parking:
        def __init__(self, capacity):
            self.capacity = capacity
            self.semaphore = threading.Semaphore(capacity)
            self.log_lock = threading.Lock()
            self.parked_count = 0
        
        def log(self, msg):
            with self.log_lock:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                output.append(f"{timestamp}   {msg}")
                
        def park(self, car_name, duration):
            self.log(f"{car_name} arrived and waiting for parking...")

            self.semaphore.acquire()

            with self.log_lock:
                self.parked_count += 1
            
            self.log(f"{car_name} entered parking.  --->  {self.parked_count}/{self.capacity} spots used")

            time.sleep(duration)

            with self.log_lock:
                self.parked_count -= 1
            
            self.log(f"{car_name} left.             --->  {self.parked_count}/{self.capacity} spots used")

            self.semaphore.release()

    class Car(threading.Thread):

        def __init__(self, name, parking, duration):
            threading.Thread.__init__(self)
            self.car_name = name
            self.parking = parking
            self.duration = duration

        def run(self):
            self.parking.park(self.car_name, self.duration)

    cars = [
        ("Car-A", 2.0),
        ("Car-B", 1.5),
        ("Car-C", 3.0),
        ("Car-D", 1.0),
        ("Car-E", 2.5),
        ("Car-F", 1.0),
        ("Car-G", 2.0),
        ("Car-H", 1.5),
    ]

    output.append("=" * 60)
    output.append(f"PARKING - Semaphore({CAPACITY})")
    output.append(f"Capacity: {CAPACITY} spots | Cars waiting: {len(cars)}")
    output.append("=" * 60)

    p = Parking(CAPACITY)
    start_time = time.time()

    threads = []
    for name, duration in cars:
        t = Car(name, p, duration)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    exec_time = time.time() - start_time
    output.append(f"Execution time  : {exec_time:.3f} seconds")

    explanation.append("سناریو 2: پارکینگ با ظرفیت محدود - Semaphore(n)")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- سمافور با مقدار 3 شروع میکند (3 جای خالی)")
    explanation.append(
        "2- هر ماشینی که وارد میشود acquire() صدا میزند -> مقدار منهای 1"
    )
    explanation.append("3- وقتی مقدار 0 شود، بقیه ماشینها باید منتظر بمانند")
    explanation.append(
        "4- هر ماشینی که خارج میشود release() صدا میزند -> مقدار مثبت 1"
    )
    explanation.append("5- یک ماشین منتظر میتواند وارد شود")
    explanation.append("")
    explanation.append("چرا وجود Lock در کنار Semaphore حیاتی است؟")
    explanation.append(
        "- کنترل ظرفیت کلی: سمافور اجازه ورود همزمان 3 نخ را میدهد."
    )
    explanation.append(
        "- جلوگیری از مسابقه نخها (Race Condition): چون 3 نخ همزمان داخل متد هستند، "
        "تغییر متغیر parked_count و اضافه کردن به لیست خروجی (output) باید توسط Lock محافظت شود "
        "تا از تداخل داده ها و خرابی متون چاپ شده جلوگیری به عمل آید."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: خط تولید کارخانه با چند مرحله
def semaphore_scenario3():
    output = []
    explanation = []

    class ProductionLine:
        def __init__(self):
            self.sem_raw_material = threading.Semaphore(4)  # 4 خط مواد خام
            self.sem_assembly = threading.Semaphore(2)  # 2 دستگاه مونتاژ
            self.sem_quality = threading.Semaphore(1)  # 1 بازرس کیفیت
            self.log_lock = threading.RLock()
            self.completed = 0
            self.rejected = 0

        def log(self, msg):
            with self.log_lock:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                output.append(f"{timestamp}   {msg}")
    
        def process(self, product_name):
            self.sem_raw_material.acquire()
            self.log(f"[{product_name}] Stage 1: Collecting raw materials...")
            time.sleep(random.uniform(0.3, 0.6))
            self.sem_raw_material.release()

            self.sem_assembly.acquire()
            self.log(f"[{product_name}] Stage 2: Assembly in progress...")
            time.sleep(random.uniform(0.5, 1.0))
            self.sem_assembly.release()

            self.sem_quality.acquire()
            self.log(f"[{product_name}] Stage 3: Quality check...")
            time.sleep(random.uniform(0.3, 0.5))
            passed = random.random() > 0.2  # 80% قبول می‌شوند

            with self.log_lock:
                if passed:
                    self.completed += 1
                    self.log(
                        f"[{product_name}] Passed QC → Shipped! (Total: {self.completed})"
                    )
                else:
                    self.rejected += 1
                    self.log(
                        f"[{product_name}] Failed QC → Rejected! (Rejected: {self.rejected})"
                    )
            self.sem_quality.release()

    class Product(threading.Thread):
        def __init__(self, name, line):
            threading.Thread.__init__(self)
            self.product_name = name
            self.line = line

        def run(self):
            self.line.process(self.product_name)

    products = [f"P-{i:02d}" for i in range(1, 13)]  # 12 محصول

    output.append("=" * 65)
    output.append("FACTORY PRODUCTION LINE — Multi Semaphore")
    output.append("=" * 65)
    output.append("  Stage 1 — Raw Materials : Semaphore(4)  capacity")
    output.append("  Stage 2 — Assembly      : Semaphore(2)  capacity")
    output.append("  Stage 3 — Quality Check : Semaphore(1)  capacity")
    output.append(f"  Total products          : {len(products)}")
    output.append("=" * 65)
    output.append("")

    line = ProductionLine()
    start_time = time.time()

    threads = []
    for name in products:
        t = Product(name, line)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    exec_time = time.time() - start_time
    output.append("")
    output.append(f"Shipped items : {line.completed}")
    output.append(f"Rejected items: {line.rejected}")
    output.append(f"Execution time: {exec_time:.3f} seconds")


    explanation.append("سناریو 3: خط تولید کارخانه — چند سمافور همزمان")
    explanation.append("هر منبع اشتراکی می‌تواند سمافور مخصوص خودش را داشته باشد.")
    explanation.append("")
    explanation.append("هر مرحله ی تولید، یک سمافور با ظرفیت متفاوت دارد:")
    explanation.append("")
    explanation.append("مرحله 1: 4 محصول همزمان")
    explanation.append("مرحله 2: 2 محصول همزمان")
    explanation.append("مرحله 3: 1 محصول همزمان")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- هر محصول برای ورود به هر مرحله acquire() می‌زند")
    explanation.append("2- اگر ظرفیت مرحله پر باشد، محصول منتظر می‌ماند")
    explanation.append("3- بعد از اتمام هر مرحله release() می‌زند")
    explanation.append("4- محصول بعدی می‌تواند وارد آن مرحله شود")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_semaphore_scenario(scenario_id: int):
    scenarios = {1: semaphore_scenario1, 2: semaphore_scenario2, 3: semaphore_scenario3}
    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")
    return scenarios[scenario_id]()
