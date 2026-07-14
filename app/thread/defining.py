import threading
import time
import random


# سناریو 1: تعریف و اجرای ترتیبی نخ ها
def defining_scenario1():
    output = []
    explanation = []

    def my_func(thread_number, duration):
        output.append(f"my_func called by thread N°{thread_number}")
        time.sleep(duration)

    start_time = time.time()
    durations = []
    for i in range(10):
        duration = random.uniform(0.1, 1.0)
        durations.append(duration)
        t = threading.Thread(target=my_func, args=(i + 1, duration))
        t.start()
        t.join()

    exec_time = time.time() - start_time

    output.append(f"\nExecution time: {exec_time:.2f} seconds")
    output.append(f"Sum of threads Execution time: {sum(durations):.2f} seconds")
    output.append(f"Execution mode: Sequential (join inside loop)")

    explanation.append("سناریو 1: تعریف نخ و اجرای ترتیبی")
    explanation.append("")
    explanation.append("=" * 70)
    explanation.append(
        "برای ایجاد یک نخ جدید در پایتون از کلاس threading.Thread استفاده می‌کنیم."
    )
    explanation.append("آرگومان های سازنده (Constructor) کلاس Thread عبارتند از:")
    explanation.append("1. target: تابعی که نخ باید اجرا کند")
    explanation.append("      مثال: t = threading.Thread(target=my_func)")
    explanation.append(
        "      پس از اجرای t.start() تابع my_func() در یک نخ جدید اجرا می‌شود."
    )
    explanation.append("2. args: ارسال آرگومان های ورودی بصورت تاپل")
    explanation.append(
        "3. kwargs(keyword arguments): ارسال آرگومان‌های نام‌دار بصورت دیکشنری"
    )
    explanation.append("4. name: نام‌گذاری نخ")
    explanation.append("     مشاهده نام نخ با threading.current_thread().name")
    explanation.append("5. daemon: مشخص می‌کند نخ از نوع Daemon باشد یا خیر")
    explanation.append("     daemon=False (پیش‌فرض): برنامه تا پایان نخ منتظر می‌ماند.")
    explanation.append(
        "   daemon=True: با پایان یافتن نخ اصلی، این نخ نیز متوقف می‌شود."
    )
    explanation.append("")
    explanation.append("=" * 70)
    explanation.append("")
    explanation.append("این سناریو ساده‌ترین روش تعریف نخ را نشان می‌دهد:")
    explanation.append("")
    explanation.append(
        "1. در این سناریو نخ‌ها با threading.Thread(target = my_func, args = (i+1, duration)) ایجاد می‌شوند"
    )
    explanation.append("2. هر نخ با ()start شروع می‌شود")
    explanation.append("3. ()join باعث می‌شود برنامه منتظر اتمام نخ بماند")
    explanation.append("زمان کل ≈ مجموع زمان خواب همه نخ ها")
    explanation.append("")
    explanation.append(
        "!توجه: در این کد، ()join داخل حلقه قرار دارد، بنابراین نخ‌ها به صورت ترتیبی اجرا می‌شوند."
    )
    explanation.append("- نخ بعدی فقط بعد از اتمام نخ قبلی شروع می‌شود.")
    explanation.append(
        "با وجود استفاده از Thread، به دلیل قرار گرفتن join داخل حلقه، هیچ موازی‌سازی واقعی اتفاق نمی‌افتد."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: تعریف و اجرای همزمان نخ‌ها
def defining_scenario2():
    output = []
    explanation = []

    def my_func(thread_number, duration):
        output.append(f"Thread {thread_number}: started (duration {duration:.2f}s)")
        time.sleep(duration)
        output.append(f"Thread {thread_number}: finished")

    start_time = time.time()
    threads = []
    durations = []

    for i in range(10):
        duration = random.uniform(0.1, 1.0)
        durations.append(duration)
        t = threading.Thread(target=my_func, args=(i + 1, duration))
        threads.append(t)
        t.start()

    output.append(
        f"\n***All {len(threads)} threads started (concurrent execution)***\n"
    )

    for t in threads:
        t.join()

    exec_time = time.time() - start_time

    output.append(f"\nTotal execution time: {exec_time:.2f} seconds")
    output.append(f"Longest sleep time: {max(durations):.2f} seconds")
    output.append(f"Execution mode: Concurrent (join outside loop)")

    explanation.append("سناریو 2: تعریف و اجرای همزمان نخ‌ها")
    explanation.append("")
    explanation.append("این سناریو تفاوت بین اجرای ترتیبی و همزمان را نشان می‌دهد:")
    explanation.append("")
    explanation.append("نکته:")
    explanation.append("- همه نخ‌ها ابتدا start می‌شوند (حلقه اول)")
    explanation.append("- سپس همه join می‌شوند (حلقه دوم)")
    explanation.append("")
    explanation.append("مزیت: نخ‌ها به صورت همزمان اجرا می‌شوند")
    explanation.append("زمان کل ≈ بیشترین زمان خواب (نه مجموع همه)")
    explanation.append(
        "زمان کل تقریباً برابر زمان طولانی‌ترین نخ است، به علاوه سربار زمان‌بندی سیستم‌عامل."
    )
    explanation.append("")
    explanation.append("مقایسه با سناریو 1:")
    explanation.append("- سناریو 1 (ترتیبی): زمان = مجموع زمان‌ها")
    explanation.append("- سناریو 2 (همزمان): زمان = حداکثر زمان")

    return {
        "output": "\n".join(output),
        "execution_time": exec_time,
        "explanation": "\n".join(explanation),
    }


# سناریو 3: شبیه‌سازی دانلود همزمان فایل‌ها
def defining_scenario3():
    output = []
    explanation = []
    results = {}

    def download_file(file_name, size, speed):
        duration = size / speed
        output.append(
            f"[START] Downloading {file_name} ({size}MB, Speed: {speed}MB/s, Est: {duration:.2f}s)"
        )
        time.sleep(duration)
        output.append(f"[DONE] {file_name} downloaded in {duration:.2f} seconds")
        results[file_name] = {"size": size, "speed": speed, "duration": duration}

    start_time = time.time()
    threads = []

    files = [
        ("movie.mp4", 100, 25),
        ("document.pdf", 5, 10),
        ("music.mp3", 10, 10),
        ("photo.jpg", 2, 8),
        ("software.iso", 200, 50),
        ("backup.zip", 150, 50),
    ]

    output.append("Download Queue:")
    output.append("-" * 50)
    for file_name, size, speed in files:
        est_time = size / speed
        output.append(f"{file_name}: {size}MB @ {speed}MB/s (~{est_time:.2f}s)")
    output.append("-" * 50)
    output.append("\nStarting concurrent downloads...\n")

    for file_name, size, speed in files:
        t = threading.Thread(target=download_file, args=(file_name, size, speed))
        threads.append(t)
        t.start()

    output.append(f"\nAll {len(threads)} downloads started concurrently!\n")

    for t in threads:
        t.join()

    exec_time = time.time() - start_time

    total_sequential_time = sum([size / speed for _, size, speed in files])

    output.append("-" * 50)
    output.append(f"Execution time (concurrent): {exec_time:.2f} seconds")
    output.append(
        f"If sequential (without threads): {total_sequential_time:.2f} seconds"
    )
    output.append(f"Total files downloaded: {len(results)}")
    output.append("Execution mode: Concurrent (all downloads at the same time)")

    explanation.append("سناریو 3: شبیه‌سازی دانلود همزمان فایل‌ها")
    explanation.append("")
    explanation.append("- چندین فایل با حجم‌های مختلف باید دانلود شوند")
    explanation.append("- هر فایل با سرعت متفاوتی دانلود می‌شود")
    explanation.append(
        "- با استفاده از نخ‌ها، همه دانلودها به صورت همزمان انجام می‌شوند"
    )
    explanation.append("- نیازی نیست منتظر اتمام یک فایل برای شروع فایل بعدی بمانیم")
    explanation.append("")
    explanation.append("مقایسه اجرا:")
    explanation.append("- حالت ترتیبی(بدون نخ): زمان = مجموع زمان دانلود همه فایل‌ها")
    explanation.append("- حالت همزمان(با نخ): زمان = زمان دانلود بزرگترین فایل")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_defining_scenario(scenario_id: int):
    scenarios = {1: defining_scenario1, 2: defining_scenario2, 3: defining_scenario3}

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
