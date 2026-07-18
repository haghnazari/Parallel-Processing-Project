import multiprocessing
import time
import random
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


def foo(q):
    name = multiprocessing.current_process().name
    q.put(f"{timestamp()}    Starting {name}")
    if name == "background_process":
        for i in range(0, 5):
            q.put(f"{timestamp()}    {name:<24s}---> {i}")
            time.sleep(1)
    else:
        for i in range(5, 10):
            q.put(f"{timestamp()}    {name:<24s}---> {i}")
            time.sleep(0.5)
    q.put(f"{timestamp()}    Exiting {name}")


def background_worker(task_name, duration, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Started  : {task_name}"
    )
    time.sleep(duration)
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Finished : {task_name}"
    )


def foreground_worker(task_name, steps, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Started  : {task_name}"
    )
    for i in range(1, steps + 1):
        time.sleep(0.5)
        q.put(
            f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Step {i}/{steps}"
        )
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Finished : {task_name}"
    )


def antivirus_scan(files, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Antivirus scan started ({len(files)} files)"
    )
    for f in files:
        time.sleep(random.uniform(0.2, 0.5))
        q.put(
            f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Scanned: {f}"
        )
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}Antivirus scan complete"
    )


def user_session(actions, q):
    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}User session started"
    )
    for action in actions:
        time.sleep(random.uniform(0.2, 1))
        q.put(
            f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}User action: {action}"
        )
    q.put(
        f"{timestamp()}    {'['+name+']':<22}{'[PID' +str(pid)+']':<15}User session ended — program exits now"
    )


# سناریو 1: فرایند daemon و غیر daemon (طبق کتاب)
def background_scenario1():
    output = []
    explanation = []

    q = multiprocessing.Queue()

    output.append("BACKGROUND PROCESSES")
    output.append("=" * 65)
    output.append(f"Main process : {multiprocessing.current_process().name}")
    output.append(f"Main PID     : {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    background_process = multiprocessing.Process(
        name="background_process", target=foo, args=(q,)
    )
    background_process.daemon = True

    no_background_process = multiprocessing.Process(
        name="NO_background_process", target=foo, args=(q,)
    )
    no_background_process.daemon = False

    start_time = time.time()

    background_process.start()
    no_background_process.start()

    no_background_process.join()

    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 65)
    output.append(f"background_process: {background_process.is_alive()}")
    output.append(f"no_background_process: {no_background_process.is_alive()}")
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 65)

    explanation.append("سناریو 1: فرآیند daemon و غیر daemon (طبق کتاب)")
    explanation.append("")
    explanation.append("دو فرایند با همان تابع target ساخته می‌شوند:")
    explanation.append("• background_process    : daemon=True")
    explanation.append("• NO_background_process : daemon=False")
    explanation.append("")
    explanation.append("رفتار daemon=True:")
    explanation.append("وقتی همه فرایندهای غیر daemon تمام شوند،")
    explanation.append("فرایندهای daemon به صورت خودکار کشته می‌شوند.")
    explanation.append("به همین دلیل فقط خروجی NO_background_process کامل است.")
    explanation.append("")
    explanation.append("چرا background_process خروجی ناقص دارد؟")
    explanation.append("چون فقط no_background_process را join کردیم.")
    explanation.append("بعد از پایان آن، برنامه اصلی تمام می‌شود")
    explanation.append("و background_process قبل از اتمام کشته می‌شود.")
    explanation.append("")
    explanation.append("کاربرد واقعی daemon=True:")
    explanation.append("• پردازش‌های پس‌زمینه مثل آنتی‌ویروس، آپدیت خودکار")
    explanation.append("• فرایندهایی که نباید مانع خروج برنامه شوند")
    explanation.append("• سرویس‌های مانیتورینگ و لاگ‌گیری")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: کار پس‌زمینه و پیش‌زمینه همزمان
def background_scenario2():
    output = []
    explanation = []

    q = multiprocessing.Queue()

    output.append("BACKGROUND vs FOREGROUND PROCESSES")
    output.append("=" * 65)
    output.append(f"Main PID: {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    # فرایندهای پس‌زمینه — daemon=True
    bg_processes = [
        multiprocessing.Process(
            name=f"BG-{task}",
            target=background_worker,
            args=(task, duration, q),
            daemon=True,
        )
        for task, duration in [
            ("Indexing files", 2),
            ("Syncing cloud", 6),
            ("Updating cache", 7),
        ]
    ]

    # فرایند پیش‌زمینه — daemon=False
    fg_process = multiprocessing.Process(
        name="FG-UserTask",
        target=foreground_worker,
        args=("Export report", 5, q),
        daemon=False,
    )

    start_time = time.time()

    for p in bg_processes:
        p.start()
    fg_process.start()

    # فقط فرایند پیش‌زمینه را join می‌کنیم
    fg_process.join()

    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 65)
    output.append("Processes status after foreground finished:")
    for p in bg_processes:
        status = "still alive — will be killed" if p.is_alive() else "finished"
        output.append(f"  {p.name:<25s} : {status}")
    output.append(f"  {fg_process.name:<25s} : finished")
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 65)

    explanation.append("سناریو 2: کار پس‌زمینه و پیش‌زمینه همزمان")
    explanation.append("")
    explanation.append("سه فرایند daemon در پس‌زمینه کار می‌کنند:")
    explanation.append("• BG-Indexing files  : ایندکس‌گذاری فایل‌ها")
    explanation.append("• BG-Syncing cloud   : همگام‌سازی با ابر")
    explanation.append("• BG-Updating cache  : به‌روزرسانی کش")
    explanation.append("")
    explanation.append("یک فرایند غیر daemon کار اصلی کاربر را انجام می‌دهد.")
    explanation.append("")
    explanation.append("با پایان fg_process (کار کاربر):")
    explanation.append("همه فرایندهای daemon بلافاصله کشته می‌شوند")
    explanation.append("حتی اگر هنوز کارشان تمام نشده باشد.")
    explanation.append("")
    explanation.append("این الگو در سیستم‌عامل‌ها رایج است:")
    explanation.append("وقتی کاربر برنامه را می‌بندد، همه سرویس‌های پس‌زمینه آن برنامه")
    explanation.append("به صورت خودکار متوقف می‌شوند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: آنتی‌ویروس در پس‌زمینه، نشست کاربر در پیش‌زمینه
def background_scenario3():
    output = []
    explanation = []

    files_to_scan = [
        "system32.dll",
        "kernel.exe",
        "driver.sys",
        "setup.msi",
        "update.pkg",
        "config.ini",
        "startup.bat",
        "hosts.txt",
        "registry.reg",
        "service.exe",
    ]

    user_jobs = [
        "Open browser",
        "Edit document",
        "Save file",
        "Close browser",
        "Shut down",
    ]

    q = multiprocessing.Queue()

    output.append("ANTIVIRUS IN BACKGROUND — daemon Process")
    output.append("=" * 65)
    output.append(f"Main process name : {multiprocessing.current_process().name}")
    output.append(f"Main process PID  : {multiprocessing.current_process().pid}")
    output.append("=" * 65)
    output.append("")

    antivirus = multiprocessing.Process(
        name="Antivirus-Scanner",
        target=antivirus_scan,
        args=(files_to_scan, q),
        daemon=True,
    )

    session = multiprocessing.Process(
        name="User-Session", target=user_session, args=(user_jobs, q), daemon=False
    )

    start_time = time.time()

    session.start()
    antivirus.start()

    session.join()

    while not q.empty():
        output.append(q.get())

    exec_time = time.time() - start_time
    scanned_count = sum(1 for line in output if "Scanned:" in line)
    remaining = len(files_to_scan) - scanned_count

    output.append("")
    output.append("=" * 65)
    output.append(f"  User session    : finished")
    status = "still alive — will be killed" if antivirus.is_alive() else "finished"
    output.append(f"  Antivirus       : {status}")
    output.append(f"  Files scanned   : {scanned_count} / {len(files_to_scan)}")
    output.append(f"  Files remaining : {remaining} (not scanned — process killed)")
    output.append(f"  Execution time  : {exec_time:.3f} seconds")
    output.append("=" * 65)

    explanation.append("سناریو 3: آنتی‌ویروس در پس‌زمینه")
    explanation.append("")
    explanation.append("یک فرایند daemon اسکن آنتی‌ویروس را انجام می‌دهد.")
    explanation.append("یک فرایند غیر daemon نشست کاربر را مدیریت می‌کند.")
    explanation.append("")
    explanation.append("نتیجه:")
    explanation.append("اسکن آنتی‌ویروس کامل نمی‌شود چون daemon است.")
    explanation.append("به محض پایان نشست کاربر، اسکن متوقف می‌شود.")
    explanation.append("")
    explanation.append("اگر daemon=False بود:")
    explanation.append("برنامه اصلی منتظر می‌ماند تا اسکن همه فایل‌ها کامل شود.")
    explanation.append("این رفتار مطلوب نیست — کاربر نباید منتظر آنتی‌ویروس بماند.")
    explanation.append("")
    explanation.append("جمع‌بندی daemon:")
    explanation.append("daemon=True  : فرایند پس‌زمینه — با برنامه اصلی کشته می‌شود")
    explanation.append("daemon=False : فرایند پیش‌زمینه — برنامه منتظر پایانش می‌ماند")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_background_scenario(scenario_id: int):
    scenarios = {
        1: background_scenario1,
        2: background_scenario2,
        3: background_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
