import multiprocessing
import time
import random
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


class MyProcess(multiprocessing.Process):
    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.q = q

    def run(self):
        self.q.put(f"{timestamp()}    called run method by {self.name}")


class DownloadTask(multiprocessing.Process):
    def __init__(
        self, file_name, file_size, speed, speed_variation, delay, shared_state, q
    ):
        multiprocessing.Process.__init__(self)
        self.file_name = file_name
        self.file_size = file_size
        self.base_speed = speed
        self.speed_variation = speed_variation
        self.delay = delay
        self.shared_state = shared_state
        self.q = q
        self.name = f"DL-{file_name}"

    def get_current_speed(self):
        variation_range = self.base_speed * self.speed_variation
        min_speed = self.base_speed - variation_range
        max_speed = self.base_speed + variation_range
        return random.uniform(min_speed, max_speed)

    def run(self):
        time.sleep(self.delay)
        start_time = time.time()
        remaining_size = self.file_size
        downloaded = 0
        current_speed = self.base_speed
        remaining_time = self.file_size / self.base_speed

        self.q.put(
            f"{timestamp()}    [{self.name}] Started downloading "
            f"(Size: {self.file_size}MB, Speed: {self.base_speed:.2f}MB/s, ETA: {remaining_time:.1f}s)"
        )


        last_report_time = time.time()
        while remaining_size > 0:
            time.sleep(0.2)
            current_speed = self.get_current_speed()
            current_time = time.time()
            chunk_size = current_speed * (current_time - last_report_time)
            last_report_time = current_time
            download_now = min(chunk_size, remaining_size)
            downloaded += download_now
            remaining_size = self.file_size - downloaded
            remaining_time = remaining_size / current_speed
            elapsed_time = current_time - start_time

            self.shared_state[self.file_name] = {
                "progress": (downloaded / self.file_size) * 100,
                "downloaded": downloaded,
                "current_speed": current_speed,
                "elapsed_time": elapsed_time,
                "remaining_time": remaining_time,
                "is_running": True,
            }

        state = self.shared_state[self.file_name]
        state["is_running"] = False
        self.shared_state[self.file_name] = state

        self.q.put(f"{timestamp()}    [{self.name}] Download complete")


class TemperatureSensor(multiprocessing.Process):
    def __init__(self, city, base_temp, interval, shared_state, q):
        multiprocessing.Process.__init__(self)
        self.city = city
        self.base_temp = base_temp
        self.interval = interval
        self.shared_state = shared_state
        self.q = q
        self.name = f"Sensor-{city}"

    def temp_sense(self, current_temp, running):
        if random.random() > 0.95:
            return current_temp, False
        new_temp = round(random.uniform(self.base_temp - 3, self.base_temp + 3), 1)
        return new_temp, running

    def run(self):
        self.q.put(f"{timestamp()}    {self.name} started monitoring {self.city}")
        time.sleep(self.interval)

        current_temp = self.base_temp
        max_temp = self.base_temp
        min_temp = self.base_temp
        readings_count = 0
        running = True

        for _ in range(5):
            time.sleep(self.interval)
            current_temp, running = self.temp_sense(current_temp, running)
            if not running:
                self.q.put(f"{timestamp()}    {self.name} failed!")
                break
            readings_count += 1
            max_temp = max(max_temp, current_temp)
            min_temp = min(min_temp, current_temp)
            self.q.put(
                f"{timestamp()}    {self.city:8} | Reading #{readings_count:3} | T = {current_temp}C"
            )

        self.shared_state[self.city] = {
            "max_temp": max_temp,
            "min_temp": min_temp,
            "readings_count": readings_count,
        }

        self.q.put(f"{timestamp()}    {self.name} finished monitoring {self.city}")


# سناریو 1: تعریف فرآیند در یک زیرکلاس
def subclass_scenario1():
    output = []
    explanation = []
    q = multiprocessing.Queue()

    output.append("Defining processes in a subclass")
    output.append("=" * 65)
    output.append("")

    for i in range(10):
        p = MyProcess(q)
        p.start()
        p.join()
    while not q.empty():
        output.append(q.get())

    output.append("")
    output.append("=" * 65)

    explanation.append("سناریو 1: تعریف فرآیند در یک زیرکلاس")
    explanation.append("")
    explanation.append(
        "• یک کلاس سفارشی به نام MyProcess از multiprocessing.Process ارث‌بری می‌کند."
    )
    explanation.append(
        "• متد run() بازنویسی (Override) شده و وظیفه اصلی فرآیند در آن تعریف می‌شود."
    )
    explanation.append(
        "• در برنامه اصلی، با صدا زدن متد .start()، سیستم‌عامل فرآیند جدید را"
    )
    explanation.append(
        "  مستقلاً ایجاد کرده و به طور خودکار متد .run() را درون آن فرآیند اجرا می‌کند."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: شبیه‌سازی دانلود همزمان فایل‌ها با Process Subclass
def subclass_scenario2():
    output = []
    explanation = []

    manager = multiprocessing.Manager()
    shared_state = manager.dict()
    q = multiprocessing.Queue()

    files = [
        ("movie.mp4", 30, 5, 0.05, 0.6),
        ("music.mp3", 20, 4, 0.08, 0.4),
        ("software.iso", 25, 4, 0.1, 0.5),
        ("photo.jpg", 10, 3, 0.05, 0.0),
        ("Backup.zip", 25, 5, 0.1, 0.3),
    ]

    output.append("*** INTERNET DOWNLOAD MANAGER — Process Subclass ***\n")

    start_time = time.time()

    processes = []
    for file_name, size, speed, variation, delay in files:
        p = DownloadTask(file_name, size, speed, variation, delay, shared_state, q)
        processes.append(p)
        p.start()

    monitoring = True
    while monitoring:
        time.sleep(1)
        monitoring = False
        output.append("=" * 40 + timestamp())
        output.append("")
        for file_name, _, _, _, _ in files:
            state = shared_state.get(file_name)
            if state is None:
                monitoring = True
                continue

            if state["is_running"]:
                monitoring = True

            progress = state["progress"]
            bar_length = 30
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)

            output.append(f"{file_name[:20]:20s} {bar} {progress:5.1f}%")
            output.append(
                f"Speed: {state['current_speed']:5.1f}MB/s | "
                f"Downloaded: {state['downloaded']:.1f}MB | "
                f"{state['elapsed_time']:.1f}s Elapsed / {state['remaining_time']:.1f}s Remaining\n"
            )

    for p in processes:
        p.join()

    output.append("=" * 40 + "Processes log")
    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time
    total_sequential = sum(size / speed for _, size, speed, _, _ in files)

    output.append("")
    output.append("DOWNLOAD SUMMARY REPORT")
    output.append("=" * 80)
    output.append(f"Total time(concurrent): {exec_time:.3f} seconds")
    output.append(f"Total time(sequential): {total_sequential:.3f} seconds")
    output.append("=" * 80)

    explanation.append("سناریو 2: دانلود همزمان فایل‌ها با Process Subclass")
    explanation.append("")
    explanation.append(
        "هر فایل توسط یک فرایند مستقل از نوع DownloadTask دانلود می‌شود."
    )
    explanation.append("")
    explanation.append("تفاوت با نسخه Thread:")
    explanation.append("در Thread، حلقه مانیتورینگ مستقیم t.get_progress() را می‌خواند")
    explanation.append("چون Thread ها در یک فضای حافظه مشترک هستند.")
    explanation.append("")
    explanation.append("در Process این کار ممکن نیست چون هر فرایند حافظه جدا دارد.")
    explanation.append("راه‌حل: multiprocessing.Manager().dict()")
    explanation.append("این دیکشنری به صورت واقعی بین فرایندها به اشتراک گذاشته می‌شود")
    explanation.append("")
    explanation.append("چون فرآیندها حافظه مشترک ندارند، برای گرفتن خروجی‌ها از یک دیکشنری سیستمی امن استفاده می‌کنیم")
    explanation.append("")
    explanation.append("پیام‌های شروع و پایان فرآیندهای فرزند از طریق q منتقل می‌شوند")
    explanation.append("چون فقط یک‌بار اتفاق می‌افتند و نیازی به خواندن مکرر ندارند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: مانیتورینگ همزمان دمای شهرهای مختلف با Process Subclass
def subclass_scenario3():
    output = []
    explanation = []

    manager = multiprocessing.Manager()
    shared_state = manager.dict()
    q = multiprocessing.Queue()

    cities = [
        ("Aleshtar", 23, 1.5),
        ("Tehran", 31, 1),
        ("Qom", 34, 1.5),
        ("Yazd", 37, 0.5),
        ("Shiraz", 28, 1),
    ]

    output.append("=" * 70)
    output.append("TEMPERATURE MONITORING SYSTEM — Process Subclass")
    output.append("=" * 70)

    start_time = time.time()

    sensors = []
    for city, temp, interval in cities:
        sensor = TemperatureSensor(city, temp, interval, shared_state, q)
        sensors.append(sensor)
        sensor.start()

    for sensor in sensors:
        sensor.join()

    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append("FINAL REPORT")
    output.append("=" * 70)

    hottest_city, hottest_temp = None, -100
    coldest_city, coldest_temp = None, 100

    for city, _, _ in cities:
        state = shared_state.get(city)
        if state is None:
            continue

        output.append(
            f"{city:10s} | Max: {state['max_temp']:4.1f}C | "
            f"Min: {state['min_temp']:4.1f}C | Readings: {state['readings_count']}"
        )
        if state["max_temp"] > hottest_temp:
            hottest_temp, hottest_city = state["max_temp"], city
        if state["min_temp"] < coldest_temp:
            coldest_temp, coldest_city = state["min_temp"], city

    output.append("")
    output.append(f"Hottest City : {hottest_city} ({hottest_temp:.1f}C)")
    output.append(f"Coldest City : {coldest_city} ({coldest_temp:.1f}C)")
    output.append(f"Total Sensors : {len(sensors)}")
    output.append(f"Execution Time : {exec_time:.2f} seconds")

    explanation.append("سناریو 3: مانیتورینگ همزمان دما با Process Subclass")
    explanation.append("")
    explanation.append("هر فرایند نماینده یک سنسور دما در یک شهر است.")
    explanation.append("")
    explanation.append("شهرهای تحت مانیتورینگ:")
    explanation.append("Aleshtar، Tehran، Qom، Yazd و Shiraz")
    explanation.append("")
    explanation.append(" اینجا Manager().dict() ساده‌تر از سناریو 2 استفاده می‌شود؛")
    explanation.append(
        "در سناریو 2 وضعیت مکرراً در حین اجرا خوانده می‌شد(مانیتورینگ زنده)."
    )
    explanation.append("اینجا فقط بعد از join نتیجه نهایی هر سنسور خوانده می‌شود؛")
    explanation.append("")
    explanation.append("تفاوت اصلی با Thread Subclass:")
    explanation.append("در نخ ها sensor.max_temp مستقیم قابل خواندن بود.")
    explanation.append("در Process، این مقدار در حافظه فرایند فرزند از بین می‌رود")
    explanation.append("مگر اینکه صریحاً از طریق Manager به اشتراک گذاشته شود.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_subclass_scenario(scenario_id: int):
    scenarios = {
        1: subclass_scenario1,
        2: subclass_scenario2,
        3: subclass_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
