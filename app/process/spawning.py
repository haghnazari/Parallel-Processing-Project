import multiprocessing
import time
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


def myFunc(i, q):
    pid = multiprocessing.current_process().pid
    q.put(f"{timestamp()}    {'[PID ' + str(pid) + ']':<15}calling myFunc from process n°: {i}")
    for j in range(i):
        q.put(f"{timestamp()}    {'[PID ' + str(pid) + ']':<15}output from myFunc is: {j}")


def download_file(file_name, size, speed, q):
    pid = multiprocessing.current_process().pid
    duration = size / speed
    q.put(f"{timestamp()}    {'[PID ' + str(pid) + ']':<15}Started   --> {file_name:<15s} {size}MB @ {speed}MB/s  est:{size/speed:.1f}s")
    time.sleep(duration)
    q.put(f"{timestamp()}    {'[PID ' + str(pid) + ']':<15}Finished  --> {file_name}")


# سناریو 1: ساخت فرایندها و اجرای ترتیبی (طبق کتاب)
def spawning_scenario1():
    output = []
    explanation = []

    q = multiprocessing.Queue()

    output.append("SPAWNING PROCESSES — Sequential")
    output.append("=" * 65)
    output.append(f"Parent PID: {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    start_time = time.time()

    for i in range(6):
        process = multiprocessing.Process(target=myFunc, args=(i, q))
        process.start()
        process.join()

        while not q.empty():
            output.append(q.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 65)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 65)

    explanation.append("سناریو 1: ساخت فرایند به ترتیب (طبق کتاب)")
    explanation.append("")
    explanation.append(
        "6 فرایند مستقل ساخته می‌شوند که هر کدام تابع myFunc را اجرا می‌کند."
    )
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- process = Process(target=myFunc, args=(i, q))")
    explanation.append("   یک فرایند جدید تعریف می‌شود ولی هنوز اجرا نشده")
    explanation.append("2- process.start()  فرایند فرزند را راه‌اندازی می‌کند")
    explanation.append("3- process.join()   فرایند اصلی منتظر پایان فرزند می‌ماند")
    explanation.append("4- بعد از join پیام‌های فرزند از Queue خوانده و لاگ می‌شوند")
    explanation.append("")
    explanation.append("چون join داخل حلقه است، فرایندها ترتیبی اجرا می‌شوند.")
    explanation.append("مراحل اجرا:")
    explanation.append("1- در هر تکرار حلقه یک شیء Process ساخته می‌شود.")
    explanation.append("2- با start() یک فرآیند جدید از فرآیند اصلی (Parent) ایجاد می‌شود.")
    explanation.append("3- تابع myFunc در فضای حافظه همان فرآیند اجرا می‌شود.")
    explanation.append("4- بلافاصله join() فراخوانی می‌شود؛ بنابراین Parent منتظر پایان همان فرآیند می‌ماند.")
    explanation.append("5- بعد از پایان فرآیند، فرآیند بعدی ساخته می‌شود.")
    explanation.append("")
    explanation.append("چرا از Queue برای انتقال خروجی استفاده می‌کنیم؟")
    explanation.append("هر فرایند حافظه مستقل دارد.")
    explanation.append("print() در فرایند فرزند فقط در terminal آن فرایند دیده می‌شود.")
    explanation.append("Queue یک کانال ارتباطی امن بین فرایندها فراهم می‌کند.")
    explanation.append("")
    explanation.append("تفاوت مهم با Thread:")
    explanation.append("در Thread حافظه مشترک بود و output مستقیم نوشته می‌شد.")
    explanation.append("در Process حافظه جداست — باید داده را صریحاً منتقل کرد.")
    explanation.append("")
    explanation.append("نتیجه:")
    explanation.append("هیچ اجرای همزمانی اتفاق نمی‌افتد.")
    explanation.append("در هر لحظه فقط یک فرآیند در حال اجرا است.")
    explanation.append("زمان کل تقریباً برابر مجموع زمان اجرای تمام فرآیندها است.")
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: تعریف و اجرای همزمان فرآیند ها
def spawning_scenario2():
    output = []
    explanation = []

    q = multiprocessing.Queue()

    output.append("SPAWNING PROCESSES — Concurrent")
    output.append("=" * 65)
    output.append(f"Parent PID: {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    start_time = time.time()
    processes = []

    for i in range(6):
        process = multiprocessing.Process(target=myFunc, args=(i, q))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 65)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 65)

    explanation.append("سناریو 2: اجرای همزمان فرایندها")
    explanation.append("")
    explanation.append("برخلاف سناریو 1، اینجا ابتدا همه start می‌شوند سپس همه join.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("حلقه اول: همه فرایندها start می‌شوند")
    explanation.append("حلقه دوم: فرایند اصلی منتظر پایان همه می‌ماند")
    explanation.append("بعد از join همه: پیام‌های Queue یکجا خوانده می‌شوند")
    explanation.append("")
    explanation.append("مقایسه با سناریو 1:")
    explanation.append("سناریو 1 — ترتیبی : زمان = مجموع زمان همه فرایندها")
    explanation.append("سناریو 2 — همزمان : زمان = بیشترین زمان بین فرایندها")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: دانلود همزمان فایل‌ها با Process
def spawning_scenario3():
    output = []
    explanation = []

    files = [
        ("movie.mp4", 30, 5),
        ("music.mp3", 20, 4),
        ("software.iso", 25, 4),
        ("photo.jpg", 10, 3),
        ("backup.zip", 25, 5),
    ]

    q = multiprocessing.Queue()

    output.append("MULTI-FILE DOWNLOADER — Spawning Processes")
    output.append("=" * 65)
    output.append(f"Parent PID: {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    start_time = time.time()
    processes = []

    for name, size, speed in files:
        p = multiprocessing.Process(target=download_file, args=(name, size, speed, q))
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
    output.append(f"Concurrent time : {exec_time:.3f} seconds")
    output.append(f"Sequential time : {total_sequential:.3f} seconds")
    output.append(f"Speed-up        : {total_sequential / exec_time:.1f}x")
    output.append("=" * 65)

    explanation.append("سناریو 3: دانلود همزمان فایل‌ها با Process")
    explanation.append("")
    explanation.append("5 فرایند مستقل هر کدام یک فایل را دانلود می‌کنند.")
    explanation.append("PID متفاوت هر فرایند نشان می‌دهد که واقعاً فرآیندها مستقلند.")
    explanation.append("")
    explanation.append("مقایسه با Thread در همین سناریو:")
    explanation.append("Thread — حافظه مشترک — output مستقیم نوشته می‌شد")
    explanation.append("Process — حافظه جدا  — خروجی از Queue خوانده می‌شود")
    explanation.append("")
    explanation.append("چه زمانی Process بهتر از Thread است؟")
    explanation.append("وقتی کار CPU-bound باشد.")
    explanation.append(
        "Thread ها به خاطر GIL نمی‌توانند واقعاً موازی روی CPU اجرا شوند."
    )
    explanation.append("Process ها GIL ندارند و روی چند هسته CPU واقعاً موازی می‌شوند.")
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_spawning_scenario(scenario_id: int):
    scenarios = {
        1: spawning_scenario1,
        2: spawning_scenario2,
        3: spawning_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
