import threading
import time
import os
import random
from random import randint
from threading import Thread


# سناریو 1: تعریف نخ با زیرکلاس
def subclass_scenario1():
    output = []
    explanation = []

    class MyThreadClass(Thread):
        def __init__(self, name, duration):
            Thread.__init__(self)
            self.name = name
            self.duration = duration

        def run(self):
            output.append(f" ---> {self.name} running, PID: {os.getpid()}")
            time.sleep(self.duration)
            output.append(f" ---> {self.name} over")

    start_time = time.time()

    threads = []
    for i in range(1, 10):
        t = MyThreadClass(f"Thread#{i}", randint(1, 10))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    exec_time = time.time() - start_time

    output.append(f"\nEnd")
    output.append(f"--- {exec_time:.2f} seconds ---")

    explanation.append("سناریو 1: تعریف نخ با زیرکلاس")
    explanation.append(
        "در این روش به جای استفاده از  target، یک کلاس جدید از Thread ساخته می‌شود."
    )
    explanation.append(
        "یک زیرکلاس تعریف می‌کنیم که از threading.Thread ارث‌بری می‌کند:"
    )
    explanation.append("")
    explanation.append("1. متد __init__ برای مقداردهی اولیه (نام و مدت زمان)")
    explanation.append(
        "2. برای تعریف کاری که نخ باید انجام دهد متد run را بازنویسی(override) می کنیم."
    )
    explanation.append("3. همه نخ‌ها PID یکسانی دارند.(چون در یک فرایند اجرا می‌شوند)")
    explanation.append("")
    explanation.append(
        "با ارث‌بری از Thread می‌توانیم وضعیت(State) و رفتار(Behavior) را داخل خود نخ نگهداری کنیم."
    )
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: شبیه‌سازی دانلود همزمان فایل‌ها
def subclass_scenario2():
    output = []
    explanation = []

    class DownloadTask(Thread):
        def __init__(self, file_name, file_size, speed, speed_variation, delay):
            Thread.__init__(self)
            self.file_name = file_name
            self.file_size = file_size
            self.base_speed = speed
            self.speed_variation = speed_variation
            self.current_speed = speed
            self.downloaded = 0
            self.delay = delay
            self.start_time = None
            self.remaining_time = None
            self.remaining_size = file_size
            self.elapsed_time = 0
            self.is_running = False

        def run(self):
            time.sleep(self.delay)
            self.start_time = time.time()
            self.is_running = True
            thread_name = threading.current_thread().name
            self.remaining_time = self.file_size / self.base_speed

            output.append(
                f" ----> {thread_name}   Started downloading '{self.file_name}'"
            )
            output.append(
                f"       Size: {self.file_size}MB | Speed: {self.base_speed:.2f}MB/s | Remaining time: {self.remaining_time:.1f}s\n"
            )

            output.append("-" * 80)
            last_report_time = time.time()
            while self.remaining_size > 0 and self.is_running:
                time.sleep(0.1)  # Downloading
                self.current_speed = self.get_current_speed()
                current_time = time.time()
                chunk_size = self.current_speed * (current_time - last_report_time)
                last_report_time = current_time
                download_now = min(chunk_size, self.remaining_size)
                self.downloaded += download_now
                self.remaining_size = self.file_size - self.downloaded
                self.remaining_time = self.remaining_size / self.current_speed
                self.elapsed_time = current_time - self.start_time
            self.is_running = False

        def get_current_speed(self):
            variation_range = self.base_speed * self.speed_variation
            min_speed = self.base_speed - variation_range
            max_speed = self.base_speed + variation_range
            new_speed = random.uniform(min_speed, max_speed)
            return new_speed

        def get_progress(self):
            return (self.downloaded / self.file_size) * 100

    files = [
        ("movie.mp4", 30, 5, 0.05, 0.6),
        ("music.mp3", 20, 4, 0.08, 0.4),
        ("software.iso", 25, 4, 0.1, 0.5),
        ("photo.jpg", 10, 3, 0.05, 0.0),
        ("Backup.zip", 25, 5, 0.1, 0.3),
    ]

    output.append("*** INTERNET DOWNLOAD MANAGER ***")
    output.append("=" * 80)
    start_time = time.time()
    threads = []
    for file_name, size, speed, variation, delay in files:
        t = DownloadTask(file_name, size, speed, variation, delay)
        t.name = f"DL-{file_name}"
        threads.append(t)
        t.start()

    monitoring = True
    while monitoring:
        time.sleep(1)
        monitoring = False
        for t in threads:
            if t.is_running:
                monitoring = True
            progress = t.get_progress()
            bar_length = 30
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)

            output.append(f"{t.file_name[:20]:20s} {bar} {progress:5.1f}%")
            output.append(
                f"Speed: {t.current_speed:5.1f}MB/s | "
                f"Downloaded: {t.downloaded:.1f}/{t.file_size}MB | "
                f"{t.elapsed_time:.1f}s Elapsed / {t.remaining_time:.1f}s Remaining\n"
            )
        output.append("=" * 80)

    for t in threads:
        t.join()

    exec_time = time.time() - start_time
    total_sequential = sum([size / speed for _, size, speed, _, _ in files])

    output.append("DOWNLOAD SUMMARY REPORT")
    output.append("=" * 80)
    output.append(f"Total time (concurrent): {exec_time:.3f} seconds")
    output.append(f"If sequential (one by one): {total_sequential:.3f} seconds")
    output.append(f"Total files downloaded: {len(threads)}")
    output.append("=" * 80)
    explanation.append("سناریو 2: شبیه‌سازی دانلود همزمان فایل‌ها")
    explanation.append("")
    explanation.append("ویژگی‌های پیاده‌سازی شده:")
    explanation.append("• نوسان سرعت دانلود (شبیه‌سازی شرایط واقعی شبکه)")
    explanation.append("• نوار پیشرفت گرافیکی با کاراکترهای █ و ░")
    explanation.append("• نمایش سرعت لحظه‌ای، زمان سپری شده و زمان باقیمانده")
    explanation.append("• دانلود همزمان چند فایل با استفاده از نخ‌های جداگانه")
    explanation.append(
        "• مزیت Subclass این است که هر Thread یک شیء مستقل با وضعیت (State) و ویژگی‌های خودش را نگهداری می کند."
    )
    explanation.append("")
    explanation.append("مقایسه عملکرد:")
    explanation.append(f"• زمان واقعی (همزمان): {exec_time:.3f} ثانیه")
    explanation.append(f"• زمان (اگر ترتیبی بود): {total_sequential:.3f} ثانیه")
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: مانیتورینگ همزمان دمای شهرهای مختلف
def subclass_scenario3():
    output = []
    explanation = []

    class TemperatureSensor(Thread):
        def __init__(self, city, base_temp, interval):
            Thread.__init__(self)
            self.city = city
            self.base_temp = base_temp
            self.current_temp = base_temp
            self.max_temp = base_temp
            self.min_temp = base_temp
            self.interval = interval
            self.readings_count = 0
            self.running = True

        def run(self):
            thread_name = threading.current_thread().name
            output.append(f"----> {thread_name} started monitoring {self.city}")
            time.sleep(self.interval)
            for _ in range(5):
                self.temp_sense()
                if not self.running:
                    output.append(f"{thread_name} failed!")
                else:
                    self.readings_count += 1
                    self.max_temp = max(self.max_temp, self.current_temp)
                    self.min_temp = min(self.min_temp, self.current_temp)
                    output.append(
                        f"{self.city:8} | Reading #{self.readings_count:3} | T = {self.current_temp}°C"
                    )
                time.sleep(self.interval)

            output.append(f"{thread_name} finished monitoring {self.city}")

        def get_average_temp(self):
            return (self.max_temp + self.min_temp) / 2

        def temp_sense(self):
            if random.random() > 0.9:
                self.running = False
            else:
                self.current_temp = round(
                    random.uniform(self.base_temp - 3, self.base_temp + 3), 1
                )

    cities = [
        ("Aleshtar", 23, 2),
        ("Tehran", 31, 1),
        ("Qom", 34, 1.5),
        ("Yazd", 37, 3),
        ("Shiraz", 28, 1),
    ]

    output.append("=" * 70)
    output.append("TEMPERATURE MONITORING SYSTEM")
    output.append("=" * 70)

    start_time = time.time()
    sensors = []
    for city, temp, interval in cities:
        sensor = TemperatureSensor(city, temp, interval)
        sensor.name = f"Sensor-{city}"
        sensors.append(sensor)
        sensor.start()

    for sensor in sensors:
        sensor.join()

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append("FINAL REPORT")
    output.append("=" * 70)

    hottest_city = None
    hottest_temp = -100
    coldest_city = None
    coldest_temp = 100

    for sensor in sensors:
        output.append(
            f"{sensor.city:10s} | Max: {sensor.max_temp:4.1f}°C | Min: {sensor.min_temp:4.1f}°C | Readings: {sensor.readings_count}"
        )
        if sensor.max_temp > hottest_temp:
            hottest_temp = sensor.max_temp
            hottest_city = sensor.city
        if sensor.min_temp < coldest_temp:
            coldest_temp = sensor.min_temp
            coldest_city = sensor.city

    output.append("")
    output.append(f"Hottest City : {hottest_city} ({hottest_temp:.1f}°C)")
    output.append(f"Coldest City : {coldest_city} ({coldest_temp:.1f}°C)")
    output.append(f"Total Sensors : {len(sensors)}")
    output.append(f"Execution Time : {exec_time:.2f} seconds")

    explanation.append("سناریو 3: مانیتورینگ همزمان دمای شهرهای مختلف")
    explanation.append("")
    explanation.append("در این سناریو هر نخ نماینده یک سنسور دما در یک شهر است.")
    explanation.append("")
    explanation.append("شهرهای تحت مانیتورینگ:")
    explanation.append("Aleshtar ، Tehran ، Qom ، Yazd و Shiraz")
    explanation.append("")
    explanation.append("سنسورها به صورت مستقل و همزمان اجرا می‌شود.")
    explanation.append(
        "سنسورها با فواصل زمانی مخصوص به خود، دمای جدید را تولید و ثبت می‌ کنند."
    )
    explanation.append("با احتمال 10 درصد ممکن است سنسور خراب شود")
    explanation.append("")
    explanation.append("ویژگی‌های ذخیره شده در هر نخ:")
    explanation.append("• نام شهر")
    explanation.append("• دمای فعلی")
    explanation.append("• بیشترین دما")
    explanation.append("• کمترین دما")
    explanation.append("• تعداد اندازه‌گیری‌ها")
    explanation.append("")
    explanation.append("این اطلاعات داخل خود شیء نخ نگهداری می‌شوند؛")
    explanation.append("به همین دلیل استفاده از Thread Subclass منطقی و مفید است.")

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
