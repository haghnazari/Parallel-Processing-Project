import multiprocessing
import time
import random
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


def foo(q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID ' +str(pid)+']':<15}Starting function"
    )

    for i in range(10):
        q.put(f"{timestamp()}    {'['+name+']':<22}{'[PID ' +str(pid)+']':<15}--> {i}")
        time.sleep(1)

    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID ' +str(pid)+']':<15}Finished function"
    )


def download_file(file_name, size, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID ' +str(pid)+']':<15}Connecting to server for download {file_name}"
    )
    downloaded = 0
    while downloaded < size:
        time.sleep(0.5)
        downloaded += random.randint(10, 20)
        if downloaded > size:
            downloaded = size
        q.put(
            f"{timestamp()}    {'['+name+']':<22}{'[PID ' +str(pid)+']':<15}Downloading {file_name}: {downloaded}/{size} MB"
        )


def image_processing(image_name, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid

    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID '+str(pid)+']':<15}Started processing {image_name}"
    )

    for i in range(10):
        time.sleep(1)

        q.put(
            f"{timestamp()}    {'['+name+']':<22}{'[PID '+str(pid)+']':<15}Processing... {10*(i+1)}%"
        )

    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID '+str(pid)+']':<15}Image processed successfully"
    )


# سناریو 1: متد terminate و بازخوانی وضعیت خروج فرآیند
def killing_scenario1():
    output = []
    explanation = []

    q = multiprocessing.Queue()

    output.append("KILLING PROCESSES")
    output.append("=" * 65)
    output.append(f"Main process : {multiprocessing.current_process().name}")
    output.append(f"Main PID     : {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    p = multiprocessing.Process(target=foo, args=(q,))

    output.append(f"{'Process before execution:':<27s}{str(p):<80s}{p.is_alive()}")

    p.start()
    output.append(f"{'Process running:':<27s}{str(p):<80s}{p.is_alive()}")

    time.sleep(3.5)

    p.terminate()
    # time.sleep(0.5)
    output.append(f"{'Process terminated:':<27s}{str(p):<80s}{p.is_alive()}")

    p.join()
    output.append(f"{'Process joined:':<27s}{str(p):<80s}{p.is_alive()}")

    output.append(f"{'Process exit code:':<27s}{p.exitcode}")
    output.append("-" * 110)

    while not q.empty():
        output.append(q.get())

    explanation.append("سناریو 1: خاتمه اجباری فرآیند (طبق کتاب)")
    explanation.append("")
    explanation.append(
        "در این سناریو، فرآیند فرزند ساخته شده و قرار است ۱۰ ثانیه کار کند."
    )
    explanation.append(
        "اما فرآیند والد بعد از 3.5 ثانیه متد p.terminate() را فراخوانی می‌کند."
    )
    explanation.append("")
    explanation.append("مکانیسم تغییر وضعیت فرآیند فرزند:")
    explanation.append(
        "• قبل از start: فرآیند زنده نیست (False) و کد خروج وجود ندارد (None)."
    )
    explanation.append(
        "• بعد از start: فرآیند زنده می‌شود (True) و کد خروج همچنان None است چون در حال اجراست."
    )
    explanation.append(
        "• بعد از terminate و join: فرآیند می‌میرد (False) و کد خروج یک عدد غیرصفر و منفی می‌شود."
    )
    explanation.append(
        "  (این عدد منفی نشان‌دهنده این است که فرآیند داوطلبانه خارج نشده، بلکه توسط سیستم‌عامل کشته شده است)."
    )
    explanation.append("")
    explanation.append("مقادیر ممکن برای ExitCode:")
    explanation.append(
        "۱. مقدار ExitCode = 0 (خروج موفقیت‌آمیز - Clean Exit) : فرآیند به خط پایانی می‌رسد و به طور طبیعی پایات می یابد."
    )
    explanation.append(
        "۲. مقدار ExitCode > 0 (بروز خطا در لایه کاربر - Application Error) : یک خطای منطقی یا استثنا(Exception) رخ داده."
    )
    explanation.append(
        "   که فرآیند نتوانسته آن را هندل کند.(مثلاً خطای تقسیم بر صفر، پر شدن حافظه، یا عدم دسترسی به یک فایل)"
    )
    explanation.append(
        "۳. مقدار ExitCode < 0 (خاتمه اجباری توسط سیستم‌عامل - Killed by Signal) : سیستم‌عامل یا فرآیند والد با شلیک یک سیگنال (Signal)، فرآیند را درجا سقط (Abort) کرده‌اند."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: لغو دانلود توسط کاربر (Cancel Download)
def killing_scenario2():
    output = []
    explanation = []

    q = multiprocessing.Queue()

    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    output.append("PROCESS TERMINATION — CANCEL DOWNLOAD")
    output.append("=" * 65)
    output.append(f"Main process : {name}")
    output.append(f"Main PID     : {pid}")
    output.append("=" * 65)
    output.append("")

    download_p = multiprocessing.Process(
        name="Download-Engine", target=download_file, args=("big_file.zip", 500, q)
    )

    download_p.start()

    time.sleep(1.8)

    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID ' +str(pid)+']':<15}User clicked 'CANCEL' button"
    )

    download_p.terminate()
    download_p.join()

    while not q.empty():
        output.append(q.get())
    output.append(f"\nDownloader Process Exit Code: {download_p.exitcode}")

    explanation.append("سناریو 2: شبیه‌سازی سیستم لغو دانلود(Cancel Download)")
    explanation.append("")
    explanation.append(
        "یک کاربرد ملموس دکمه لغو در نرم‌افزارها، فرستادن سیگنال خاتمه به فرآیند مسئول دانلود است."
    )
    explanation.append(
        "• فرآیند Download-Engine به صورت درصدی داده‌ها را دانلود و گزارش می‌کند."
    )
    explanation.append(
        "• با زدن کلید لغو، برنامه اصلی بدون معطلی فرآیند را terminate می‌کند."
    )
    explanation.append(
        "• در خروجی لاگ‌ها به وضوح خواهید دید که دانلود در اواسط کار قطع شده و لاگ Finished هرگز ثبت نمی‌شود."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو ۳: پایان دادن به پردازش زمان‌بر (Timeout)
def killing_scenario3():
    output = []
    explanation = []

    q = multiprocessing.Queue()
    
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    output.append("PROCESS TERMINATION — IMAGE PROCESSING TIMEOUT")
    output.append("=" * 65)
    output.append(f"Main process : {name}")
    output.append(f"Main PID     : {pid}")
    output.append("=" * 65)
    output.append("")

    p = multiprocessing.Process(
        name="ImageProcessor", target=image_processing, args=("brain_scan.png", q)
    )

    p.start()

    time.sleep(4)

    q.put(f"{timestamp()}    {'['+name+']':<22}{'[PID '+str(pid)+']':<15}Timeout exceeded (4 seconds)")
    q.put(f"{timestamp()}    {'['+name+']':<22}{'[PID '+str(pid)+']':<15}Terminating ImageProcessor...")

    p.terminate()
    p.join()

    while not q.empty():
        output.append(q.get())

    output.append("")
    output.append(f"Process Exit Code: {p.exitcode}")

    explanation.append("سناریو ۳: پایان دادن به پردازش زمان‌بر (Timeout)")
    explanation.append("")
    explanation.append("در بسیاری از سامانه‌ها برای جلوگیری از اشغال شدن منابع، برای هر پردازش یک حداکثر زمان مجاز (Timeout) تعریف می‌شود.")
    explanation.append("در این مثال فرآیند ImageProcessor مسئول پردازش یک تصویر است.")
    explanation.append("اگر پردازش بیش از ۴ ثانیه طول بکشد،")
    explanation.append("فرآیند والد فرض می‌کند برنامه دچار گیرکردن (Hang) یا کندی غیرعادی شده است.")
    explanation.append("")
    explanation.append("در نتیجه:")
    explanation.append("• والد پیام Timeout را ثبت می‌کند.")
    explanation.append("• متد terminate() را فراخوانی می‌کند.")
    explanation.append("• سیستم‌عامل بلافاصله فرآیند را متوقف می‌کند.")
    explanation.append("• پیام Image processed successfully هرگز چاپ نمی‌شود.")
    explanation.append("• ExitCode فرآیند منفی خواهد بود که نشان‌دهنده خاتمه اجباری است.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_killing_scenario(scenario_id: int):
    scenarios = {1: killing_scenario1, 2: killing_scenario2, 3: killing_scenario3}

    if scenario_id not in scenarios:
        raise ValueError(
            f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود برای بخش Killing: 1, 2, 3"
        )

    return scenarios[scenario_id]()
