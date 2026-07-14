import multiprocessing
import time
import random
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

def myFunc(q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(f"{timestamp()}    Starting process name = {name:<20s}[PID {pid}]")
    time.sleep(3)
    q.put(f"{timestamp()}    Exiting  process name = {name:<20s}[PID {pid}]")


def sensor_task(city, base_temp, readings, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(f"{timestamp()}    {'['+name+']':<20}{'[PID' +str(pid)+']':<15}Started monitoring {city}")
    for i in range(readings):
        time.sleep(random.uniform(0.3, 0.7))
        temp = round(random.uniform(base_temp - 3, base_temp + 3), 1)
        q.put(f"{timestamp()}    {'['+name+']':<20}{'[PID' +str(pid)+']':<15}{city}: {temp}C  (#{i+1})")
    q.put(f"{timestamp()}    {'['+name+']':<20}{'[PID' +str(pid)+']':<15}Finished monitoring {city}")


def download_file(file_name, size, speed, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    duration = size / speed
    q.put(f"{timestamp()}    {'['+name+']':<20}{'[PID' +str(pid)+']':<15}Started   -->  {file_name:<15s} {size}MB @ {speed}MB/s  est:{size/speed:.1f}s")
    time.sleep(duration)
    q.put(f"{timestamp()}    {'['+name+']':<20}{'[PID' +str(pid)+']':<15}Finished  -->  {file_name}")


# سناریو 1: نام‌گذاری فرآیندها
def naming_scenario1():
    output = []
    explanation = []

    q = multiprocessing.Queue()

    output.append("NAMING A PROCESS")
    output.append("=" * 65)
    output.append(f"Main process name : {multiprocessing.current_process().name}")
    output.append(f"Main process PID  : {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    process_with_name = multiprocessing.Process(
        name="myFunc process", target=myFunc, args=(q,)
    )
    process_with_default_name = multiprocessing.Process(target=myFunc, args=(q,))

    start_time = time.time()

    process_with_name.start()
    process_with_default_name.start()
    
    process_with_name.join()
    process_with_default_name.join()
    
    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 65)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 65)

    explanation.append("سناریو 1: نام‌گذاری فرایند (طبق کتاب)")
    explanation.append("")
    explanation.append("دو فرایند با همان تابع target ساخته می‌شوند:")
    explanation.append("• فرایند اول با نام دلخواه: name='myFunc process'")
    explanation.append("• فرایند دوم بدون نام: پایتون به صورت خودکار Process-2 می‌دهد")
    explanation.append("")
    explanation.append("نحوه خواندن نام فرایند جاری:")
    explanation.append("  multiprocessing.current_process().name")
    explanation.append("")
    explanation.append("سه نوع نام در multiprocessing:")
    explanation.append("• MainProcess (یا SpawnProcess-X): فرایند اصلی و والد برنامه")
    explanation.append("• Process-X:Y : نام پیش‌فرض فرایندهای فرزند (Yمین مین فرزند فرآیند X)")
    explanation.append("• نام دلخواه     : هر رشته‌ای که به name= بدهیم")
    explanation.append("")
    explanation.append("چرا نام‌گذاری مهم است؟")
    explanation.append("در برنامه‌های بزرگ با ده‌ها فرایند، نام‌های معنادار")
    explanation.append("اشکال‌زدایی و مانیتورینگ را بسیار ساده‌تر می‌کنند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: مانیتورینگ دمای شهرها با فرایندهای نام‌گذاری شده
def naming_scenario2():
    output = []
    explanation = []

    cities = [
        ("Aleshtar", 23, 4),
        ("Tehran", 31, 4),
        ("Ahvaz", 38, 4),
        ("Yazd", 36, 4),
    ]

    q = multiprocessing.Queue()

    output.append("TEMPERATURE MONITORING — Named Processes")
    output.append("=" * 65)
    output.append(f"Main process : {multiprocessing.current_process().name}")
    output.append("=" * 65)
    output.append("")

    start_time = time.time()
    processes = []

    for city, base_temp, readings in cities:
        p = multiprocessing.Process(
            name=f"Sensor-{city}",
            target=sensor_task,
            args=(city, base_temp, readings, q),
        )
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    while not q.empty():
        output.append(q.get())
        
    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 65)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 65)

    explanation.append("سناریو 2: مانیتورینگ دما با فرایندهای نام‌گذاری شده")
    explanation.append("")
    explanation.append("هر فرایند نام شهر مربوطه را دارد:")
    explanation.append("  name=f'Sensor-{city}'")
    explanation.append("")
    explanation.append("مزیت نام‌گذاری در این سناریو:")
    explanation.append("در خروجی بدون نیاز به PID می‌توان فهمید")
    explanation.append("هر پیام از کدام شهر آمده است.")
    explanation.append("")
    explanation.append("مقایسه با Thread subclass سناریوی مشابه:")
    explanation.append(
        "در Thread، نام نخ با threading.current_thread().name خوانده می‌شد."
    )
    explanation.append(
        "در Process، نام فرایند با multiprocessing.current_process().name خوانده می‌شود."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: دانلود فایل با فرایندهای نام‌گذاری شده
def naming_scenario3():
    output = []
    explanation = []

    files = [
        ("movie.mp4", 30, 5),
        ("music.mp3", 20, 4),
        ("software.iso", 25, 4),
        ("photo.jpg", 10, 3),
    ]

    q = multiprocessing.Queue()

    output.append("MULTI-FILE DOWNLOADER — Named Processes")
    output.append("=" * 65)
    output.append(f"Main process name : {multiprocessing.current_process().name}")
    output.append(f"Main process PID  : {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    start_time = time.time()
    processes = []

    for name, size, speed in files:
        p = multiprocessing.Process(
            name=f"DL-{name}", target=download_file, args=(name, size, speed, q)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time
    total_sequential = sum(size / speed for _, size, speed in files)

    output.append("")
    output.append("=" * 65)
    output.append(f"  Concurrent time : {exec_time:.3f} seconds")
    output.append(f"  Sequential time : {total_sequential:.3f} seconds")
    output.append(f"  Speed-up        : {total_sequential / exec_time:.1f}x")
    output.append("=" * 65)

    explanation.append("سناریو 3: دانلود فایل با فرایندهای نام‌گذاری شده")
    explanation.append("")
    explanation.append("هر فرایند نام فایل مربوطه را دارد: name=f'DL-{file_name}'")
    explanation.append("")
    explanation.append("در خروجی سه نوع اطلاعات شناسایی نمایش داده می‌شود:")
    explanation.append("• نام فرایند  : [DL-movie.mp4]  — معنادار و قابل خواندن")
    explanation.append("• PID         : [PID 1234]      — شناسه سیستم‌عاملی")
    explanation.append("")
    explanation.append("ترکیب نام و PID بهترین روش شناسایی فرایند در لاگ‌هاست.")
    explanation.append("نام برای خوانایی انسانی، PID برای ابزارهای سیستم‌عامل.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_naming_scenario(scenario_id: int):
    scenarios = {
        1: naming_scenario1,
        2: naming_scenario2,
        3: naming_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
