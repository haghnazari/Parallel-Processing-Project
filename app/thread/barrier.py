import threading
import time
import random
from threading import Thread, Barrier
from datetime import datetime


# سناریو 1: مسابقه دو با سه شرکت‌کننده
def barrier_scenario1():
    output = []
    explanation = []

    num_runners = 3
    runners = ["Huey", "Dewey", "Louie"]
    finish_line = Barrier(num_runners)
    log_lock = threading.Lock()

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    def runner():
        name = runners.pop()
        time.sleep(random.randrange(0.5, 1.5))
        log(f"{name} reached the barrier.")
        finish_line.wait()

    output.append("START RACE!")
    output.append("=" * 50)

    start_time = time.time()

    threads = []
    for i in range(num_runners):
        threads.append(Thread(target=runner))
        threads[-1].start()
    for thread in threads:
        thread.join()

    exec_time = time.time() - start_time

    output.append("=" * 50)
    output.append("Race over!")
    output.append(f"Execution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 1: مسابقه دو با Barrier ")
    explanation.append("")
    explanation.append("سه دونده با تاخیرهای تصادفی به خط پایان می‌رسند.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- Barrier با عدد 3 ساخته می‌شود یعنی منتظر 3 نخ می‌ماند")
    explanation.append("2- هر دونده پس از رسیدن، finish_line.wait() صدا می‌زند")
    explanation.append("3- دونده‌ای که زودتر رسیده پشت Barrier منتظر می‌ماند")
    explanation.append(
        "4- وقتی نفر سوم هم وارد شد،  سیستم‌عامل هر ۳ نخ را همزمان بیدار کرده و اجازه عبور به خطوط بعدی را می‌دهد."
    )
    explanation.append("")
    explanation.append("نکته مهم:")
    explanation.append("ترتیب رسیدن دونده‌ها تصادفی است.")
    explanation.append("کسی که زودتر به wait() برسد، تا رسیدن همه باید صبر کند.")
    explanation.append("هیچ نخی نمی‌تواند زودتر از بقیه از Barrier رد شود.")
    explanation.append("")
    explanation.append(
        "   استفاده از runners.pop() در کد کتاب برای توزیع اسامی نخ ها، از داده مشترک بدون قفل استفاده شده است "
    )
    explanation.append(
        "   Race Condition: با انتقال متغیرها به عنوان آرگومان ورودی کلاس (runner_name)، از تداخل حافظه جلوگیری کامل به عمل می آید."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: لابی بازی آنلاین
def barrier_scenario2():
    output = []
    explanation = []
    log_lock = threading.Lock()
    num_players = 4

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    def start_match_server():
        log("SERVER: All players loaded the map! STARTING MATCH NOW!")

    match_barrier = Barrier(num_players, action=start_match_server)

    class Player(Thread):
        def __init__(self, name):
            super().__init__()
            self.player_name = name

        def run(self):
            log(f"{self.player_name:<16s} Connecting and loading map ...")
            time.sleep(random.uniform(1.0, 3.5))
            log(f"{self.player_name:<16s} 100% loaded. Waiting in lobby.")
            match_barrier.wait()
            log(f"{self.player_name:<16s} Spawned in the map! Let's go!")

    output.append("MULTIPLAYER GAME LOBBY - Barrier")
    output.append("=" * 60)

    players = [
        Player("Player_1(PC)"),
        Player("Player_2(PS5)"),
        Player("Player_3(Xbox)"),
        Player("Player_4(PC)"),
    ]

    start_time = time.time()

    for p in players:
        p.start()
    for p in players:
        p.join()

    exec_time = time.time() - start_time

    output.append("=" * 60)
    output.append("Match finished cleanly.")
    output.append(f"Total time in lobby: {exec_time:.3f} seconds")

    explanation.append("سناریو 2: لابی بازی چندنفره (قابلیت Action در Barrier)")
    explanation.append("")
    explanation.append(
        "چهار بازیکن با سخت‌افزار و پینگ مختلف در حال لود کردن نقشه هستند."
    )
    explanation.append("هیچکس نباید زودتر از بقیه وارد بازی شود.")
    explanation.append("")
    explanation.append("نکات این سناریو:")
    explanation.append(
        "1- استفاده از پارامتر action=start_match_server در ساخت Barrier."
    )
    explanation.append(
        "2- وقتی آخرین نفر (نفر چهارم) به wait() می‌رسد، قبل از اینکه نخ‌ها را بیدار شوند، ابتدا تابع start_match_server اجرا می‌شود."
    )
    explanation.append(
        "3- این ویژگی برای انجام لاگ‌گیری مرکزی، تجمیع داده‌ها یا اعلام شروع فاز بعدی در سیستم‌های توزیع‌شده کاربرددارد."
    )
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: نرمال‌سازی موازی ماتریس با Barrier
def barrier_scenario3():
    output = []
    explanation = []
    log_lock = threading.Lock()

    matrix = [[10, 20, 30, 40], [5, 15, 25, 35], [2, 4, 6, 8]]

    num_threads = 3
    local_maxes = [0] * num_threads
    global_max = 0
    current_phase = 1

    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")

    def barrier_phase_manager():
        nonlocal current_phase, global_max
        if current_phase == 1:
            global_max = max(local_maxes)
            log(
                f"BARRIER ACTION: Phase 1 complete. Global Max calculated = {global_max}\n"
            )
            current_phase += 1

        else:
            log(
                "BARRIER ACTION: Phase 2 complete. All threads finished normalizing.\n"
            )

    matrix_barrier = Barrier(num_threads, action=barrier_phase_manager)

    class MatrixWorker(Thread):
        def __init__(self, thread_id):
            super().__init__()
            self.thread_id = thread_id
            self.row_index = thread_id

        def run(self):
            log(
                f"Worker-{self.thread_id:<2} [Phase 1]: Scanning row {self.row_index}..."
            )
            time.sleep(random.uniform(0.5, 1))
            row_max = max(matrix[self.row_index])
            local_maxes[self.thread_id] = row_max
            log(
                f"Worker-{self.thread_id:<2} [Phase 1]: Local max is {row_max}. Waiting at barrier..."
            )

            matrix_barrier.wait()

            log(
                f"Worker-{self.thread_id:<2} [Phase 2]: Normalizing row {self.row_index} using global max {global_max}..."
            )
            time.sleep(random.uniform(0.5, 1.0))

            for i in range(len(matrix[self.row_index])):
                matrix[self.row_index][i] = round(
                    matrix[self.row_index][i] / global_max, 3
                )

            log(
                f"Worker-{self.thread_id:<2} [Phase 2]: Row {self.row_index} done. Waiting to finalize..."
            )

            matrix_barrier.wait()

    output.append("MULTI-PHASE MATRIX NORMALIZATION - Barrier")
    output.append("Original Matrix:")
    for row in matrix:
        output.append(f"  {row}")
    output.append("-" * 70)

    workers = [MatrixWorker(i) for i in range(num_threads)]

    start_time = time.time()
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    exec_time = time.time() - start_time

    output.append("=" * 70)
    output.append("Final Normalized Matrix:")
    for row in matrix:
        output.append(f"  {row}")
    output.append(f"\nExecution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 3: عملیات ماتریسی چند مرحله‌ای (نرمال‌سازی موازی)")
    explanation.append("")
    explanation.append("سه نخ به طور همزمان روی سطرهای مختلف یک ماتریس کار می‌کنند.")
    explanation.append(
        "عملیات دو فاز دارد: ۱. یافتن ماکزیمم هر سطر ۲. نرمال‌سازی ماتریس با ماکزیممِ کل."
    )
    explanation.append("")
    explanation.append(
        "1- در فاز اول هر نخ ماکزیمم محلی را پیدا کرده و پشت سد می‌ماند."
    )
    explanation.append("2- اجرای Action: زمانی که همه نخ‌ها به wait() رسیدند، متد اکشن")
    explanation.append(
        "   به صورت خودکار اجرا می‌شود تا ماکزیمم کل (Global Max) را حساب کند."
    )
    explanation.append(
        "3-  همان نخ‌ها دوباره بیدار شده، فاز دوم(تقسیم مقادیر بر عدد ماکزیمم سراسری) را در دست می‌گیرند و"
    )

    explanation.append(
        " در انتهای فاز دوم دوباره پشت همان سد (barrier.wait) با هم سینک می‌شوند تا برنامه ماتریسِ ناتمام را چاپ نکند."
    )
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_barrier_scenario(scenario_id: int):
    scenarios = {1: barrier_scenario1, 2: barrier_scenario2, 3: barrier_scenario3}

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد.")

    return scenarios[scenario_id]()
