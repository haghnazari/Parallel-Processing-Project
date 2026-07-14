import multiprocessing
import time
import random
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


# ==============================================================
# سناریو 1: همگام‌سازی فرایندها با Barrier
# ==============================================================

def test_with_barrier(synchronizer, serializer, log_queue):
    name = multiprocessing.current_process().name
    synchronizer.wait()
    now = time.time()
    with serializer:
        log_queue.put(f"process {name} ----> {datetime.fromtimestamp(now)}")


def test_without_barrier(log_queue):
    name = multiprocessing.current_process().name
    now = time.time()
    log_queue.put(f"process {name} ----> {datetime.fromtimestamp(now)}")


def run_barrier_scenario():
    output      = []
    explanation = []

    log_queue    = multiprocessing.Queue()
    synchronizer = multiprocessing.Barrier(2)
    serializer   = multiprocessing.Lock()

    output.append("SYNCHRONIZING PROCESSES WITH BARRIER")
    output.append("=" * 70)

    start_time = time.time()

    p1 = multiprocessing.Process(name="p1 - test_with_barrier",    target=test_with_barrier,    args=(synchronizer, serializer, log_queue))
    p2 = multiprocessing.Process(name="p2 - test_with_barrier",    target=test_with_barrier,    args=(synchronizer, serializer, log_queue))
    p3 = multiprocessing.Process(name="p3 - test_without_barrier", target=test_without_barrier, args=(log_queue,))
    p4 = multiprocessing.Process(name="p4 - test_without_barrier", target=test_without_barrier, args=(log_queue,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    while not log_queue.empty():
        output.append(log_queue.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 1: همگام‌سازی فرایندها با Barrier")
    explanation.append("")
    explanation.append("چهار فرایند تعریف می‌شوند:")
    explanation.append("p1, p2 : از synchronizer.wait() استفاده می‌کنند")
    explanation.append("p3, p4 : هیچ همگام‌سازی ندارند")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("Barrier(2) یعنی منتظر 2 فرایند می‌ماند.")
    explanation.append("وقتی هر دو p1 و p2 به synchronizer.wait() رسیدند، همزمان آزاد می‌شوند")
    explanation.append("و timestamp بسیار نزدیک به هم می‌گیرند.")
    explanation.append("")
    explanation.append("نقش serializer (Lock):")
    explanation.append("بعد از عبور از Barrier، هر دو فرایند همزمان می‌خواهند")
    explanation.append("پیام خود را در Queue بگذارند؛ Lock تضمین می‌کند")
    explanation.append("این کار بدون تداخل انجام شود.")
    explanation.append("البته در اینجا نیازی به Lock نبود چون خود Queue جلوی تداخل را می گیرد.")
    explanation.append("")
    explanation.append("p3 و p4 اندکی timestamp متفاوت دارند؛")
    explanation.append("چون هیچ Barrier ای بین آن‌ها نیست؛ هر کدام مستقل و در هر لحظه‌ای")
    explanation.append("که سیستم‌عامل زمان‌بندی کند اجرا می‌شود.")
    explanation.append("")
    explanation.append("Barrier(n) دقیقاً منتظر n فراخوانی wait() می‌ماند، نه n فرایند.")
    explanation.append("اگر فقط 2 تا از 4 فرایند wait() .را صدا بزنند، فقط همان 2 تا همگام می‌شوند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# ==============================================================
# سناریو 2: سیستم تراکنش بانکی با Lock
# ==============================================================

def bank_worker(amount, tx_type, balance_val, lock, log_queue):
    with lock:
        old_balance = balance_val.value
        name = multiprocessing.current_process().name
        log_queue.put(f"{timestamp()}    {name:<20s}type={tx_type}, amount={amount}, balance_before={old_balance}")
        time.sleep(0.01)

        if tx_type == "Deposit":
            balance_val.value += amount
            log_queue.put(f"{timestamp()}    {name:<20s}DEPOSIT  {amount} | new_balance={balance_val.value}")
        elif tx_type == "Withdraw":
            if balance_val.value >= amount:
                balance_val.value -= amount
                log_queue.put(f"{timestamp()}    {name:<20s}WITHDRAW  -{amount} | new_balance={balance_val.value}")
            else:
                log_queue.put(f"{timestamp()}    {name:<20s}REJECTED withdraw {amount} FAILED (insufficient balance: {balance_val.value})")

        time.sleep(0.005)
        log_queue.put(f"{timestamp()}    {name:<20s}END | final_balance={balance_val.value}")


def run_lock_scenario():
    output      = []
    explanation = []

    log_queue = multiprocessing.Queue()
    bank_lock = multiprocessing.Lock()
    balance   = multiprocessing.Value("i", 1000)

    output.append("BANKING SYSTEM WITH LOCK")
    output.append("=" * 70)
    output.append(f"Initial balance     : {balance.value}")
    output.append(f"Total transactions  : 10")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    processes = []
    for i in range(10):
        amount   = random.randint(300, 800)
        tx_type  = "Deposit" if random.random() > 0.5 else "Withdraw"
        p = multiprocessing.Process(
            name=f"Transaction{i+1}",
            target=bank_worker,
            args=(amount, tx_type, balance, bank_lock, log_queue)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not log_queue.empty():
        output.append(log_queue.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append(f"Final balance   : {balance.value}")
    output.append(f"Execution time  : {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 2: سیستم تراکنش بانکی با Lock")
    explanation.append("")
    explanation.append("چون فرایندها حافظه مستقل دارند، برای اشتراک موجودی حساب")
    explanation.append("از multiprocessing.Value('i', 1000) استفاده شده است.")
    explanation.append("")
    explanation.append("نقش Lock:")
    explanation.append("Lock تضمین می‌کند در هر لحظه فقط یک فرایند وارد بخش بحرانی شود")
    explanation.append("(خواندن موجودی، تغییر آن، نوشتن دوباره).")
    explanation.append("")
    explanation.append("اگر Lock نبود، دو فرایند می‌توانستند همزمان balance.value را بخوانند،")
    explanation.append("هر دو تغییر خودشان را روی همان مقدار قدیمی اعمال کنند،")
    explanation.append("")
    explanation.append("multiprocessing.Value خودش thread/process-safe نیست مگر با Lock محافظت شود؛")
    explanation.append("Value فقط حافظه را به اشتراک می‌گذارد، نه امنیت دسترسی همزمان را.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# ==============================================================
# سناریو 3: چراغ راهنمایی هوشمند با Event
# ==============================================================

def car_worker(name, arrival_time, light_event, log_queue):
    time.sleep(arrival_time)
    log_queue.put(f"{timestamp()}    {name:<14s} Arrived.")

    if not light_event.is_set():
        log_queue.put(f"{timestamp()}    {name:<14s} {'Light is RED':<15s}--> Waiting...")
        light_event.wait()

    log_queue.put(f"{timestamp()}    {name:<14s} {'Light is GREEN':<15s}--> Crossing...")
    time.sleep(0.2)
    log_queue.put(f"{timestamp()}    {name:<14s} Passed")


def traffic_controller(light_event, log_queue):
    log_queue.put(f"{timestamp()}    Controller     Light = RED")
    time.sleep(2)

    log_queue.put(f"{timestamp()}    Controller     Light = GREEN   --> event.set()")
    light_event.set()
    time.sleep(2)

    log_queue.put(f"{timestamp()}    Controller     Light = RED   --> event.clear()")
    light_event.clear()
    time.sleep(2)

    log_queue.put(f"{timestamp()}    Controller     Light = GREEN  --> event.set()")
    light_event.set()


def run_event_scenario():
    output      = []
    explanation = []

    log_queue   = multiprocessing.Queue()
    light = multiprocessing.Event()

    cars_data = [
        ("Car-1", 1.0),
        ("Car-2", 1.5),
        ("Car-3", 3.0),
        ("Car-4", 4.5),
        ("Car-5", 5.0),
        ("Car-6", 6.0),
    ]

    output.append("SMART TRAFFIC LIGHT WITH EVENT")
    output.append("=" * 70)
    output.append("RED   : 0s to 2s")
    output.append("GREEN : 2s to 4s")
    output.append("RED   : 4s to 6s")
    output.append("GREEN : 6s onward")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    controller = multiprocessing.Process(target=traffic_controller, args=(light, log_queue))
    controller.start()

    processes = []
    for name, arr_time in cars_data:
        p = multiprocessing.Process(target=car_worker, args=(name, arr_time, light, log_queue))
        processes.append(p)
        p.start()

    controller.join()
    for p in processes:
        p.join()

    while not log_queue.empty():
        output.append(log_queue.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 3: چراغ راهنمایی هوشمند با Event")
    explanation.append("")
    explanation.append("یک فرایند کنترلر چراغ را کنترل می‌کند.")
    explanation.append("هر فرایند ماشین در زمان مشخصی می‌رسد و وضعیت چراغ را بررسی می‌کند.")
    explanation.append("")
    explanation.append("نحوه عملکرد Event:")
    explanation.append("green_light.set()   : چراغ سبز -- همه ماشین‌های منتظر همزمان رد می‌شوند")
    explanation.append("green_light.clear() : چراغ قرمز -- event.wait() از این پس بلاک می‌کند")
    explanation.append("green_light.wait()  : اگر سبز بود فوری رد می‌شود، اگر قرمز بود منتظر می‌ماند")
    explanation.append("")
    explanation.append("چرا اینجا Event به‌جای Lock استفاده شد؟")
    explanation.append("Lock فقط اجازه یک فرایند در زمان واحد را می‌دهد.")
    explanation.append("Event به همه فرایندهای منتظر اجازه عبور همزمان می‌دهد؛")
    explanation.append("این دقیقاً رفتاری است که چراغ سبز باید داشته باشد.")
    explanation.append("")
    explanation.append("Event در multiprocessing از نظر رفتار دقیقاً مثل threading.Event است؛")
    explanation.append("تنها تفاوت این است که پرچم set/clear در سطح سیستم‌عامل بین فرایندهای")
    explanation.append("مستقل به اشتراک گذاشته می‌شود، نه فقط در حافظه یک فرایند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# ==============================================================
# سناریو 4: تولیدکننده و مصرف‌کننده با Condition
# ==============================================================

def producer_worker(condition, shared_list, max_size, log_queue):
    for i in range(10):
        time.sleep(random.uniform(0.2,0.5))
        with condition:
            while len(shared_list) >= max_size:
                log_queue.put(f"{timestamp()}    Producer   Buffer full ({len(shared_list)}). Waiting...")
                condition.wait()

            shared_list.append(1)
            log_queue.put(f"{timestamp()}    Producer   Produced 1 item. Total items: {len(shared_list)}")
            condition.notify()


def consumer_worker(condition, shared_list, log_queue):
    for i in range(10):
        time.sleep(random.uniform(0.4,0.8))
        with condition:
            while len(shared_list) == 0:
                log_queue.put(f"{timestamp()}    Consumer   No items available. Waiting...")
                condition.wait()

            shared_list.pop()
            log_queue.put(f"{timestamp()}    Consumer   Consumed 1 item. Total items: {len(shared_list)}")
            condition.notify()


def run_condition_scenario():
    output      = []
    explanation = []

    log_queue = multiprocessing.Queue()

    manager     = multiprocessing.Manager()
    shared_list = manager.list()
    condition   = multiprocessing.Condition()

    output.append("PRODUCER/CONSUMER WITH CONDITION")
    output.append("=" * 70)
    output.append("Buffer capacity: 4")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    p1 = multiprocessing.Process(target=producer_worker, args=(condition, shared_list, 4, log_queue))
    p2 = multiprocessing.Process(target=consumer_worker, args=(condition, shared_list, log_queue))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    while not log_queue.empty():
        output.append(log_queue.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 4: تولیدکننده و مصرف‌کننده با Condition")
    explanation.append("")
    explanation.append("Condition اجازه می‌دهد فرایندها بر اساس یک شرط منطقی (مثلا پر یا خالی بودن بافر) هماهنگ شوند.")
    explanation.append("")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("condition.wait() قفل داخلی را موقتاً آزاد کرده و فرایند را معلق می‌کند")
    explanation.append("تا زمانی که فرایند دیگر condition.notify() صدا بزند.")
    explanation.append("")
    explanation.append("shared_list باید از manager.list() باشد؛")
    explanation.append("لیست معمولی پایتون بین فرایندها به اشتراک گذاشته نمی‌شود؛")
    explanation.append("هر فرایند کپی مستقل خودش را می‌گیرد.")
    explanation.append("manager.list() یک لیست واقعاً مشترک بین فرایندها فراهم می‌کند.")
    explanation.append("")
    explanation.append("از while به جای if استفاده شد؛")
    explanation.append("بعد از notify، فرایند بیدارشده باید دوباره شرط را بررسی کند")
    explanation.append("چون ممکن است وضعیت بین notify و بیدار شدن واقعی تغییر کرده باشد.")
    explanation.append("")
    explanation.append("multiprocessing.Condition() به‌طور پیش‌فرض بر پایه RLock ساخته می‌شود،")
    explanation.append("دقیقاً مثل threading.Condition؛ رفتار wait/notify یکسان است،")
    explanation.append("فقط قابل استفاده بین فرایندهای کاملاً مستقل است.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# ==============================================================
# ۵. توابع هدف برای سناریوی Semaphore (پارکینگ خودرو)
# ==============================================================

def parking_worker(car_name, duration, semaphore, parked_count, lock, log_queue):
    log_queue.put(f"{timestamp()}    {car_name} arrived and waiting for parking...")

    semaphore.acquire()
    with lock:
        parked_count.value += 1
        log_queue.put(f"{timestamp()}    {car_name} entered parking. [{parked_count.value}/3 spots used]")

    time.sleep(duration)

    with lock:
        parked_count.value -= 1
        log_queue.put(f"{timestamp()}    {car_name} left.            [{parked_count.value}/3 spots used]")
    semaphore.release()


def run_semaphore_scenario():
    output      = []
    explanation = []

    log_queue    = multiprocessing.Queue()
    semaphore    = multiprocessing.Semaphore(3)
    lock         = multiprocessing.Lock()
    parked_count = multiprocessing.Value("i", 0)

    cars = [
        ("Car-A", 1.0),
        ("Car-B", 0.8),
        ("Car-C", 1.5),
        ("Car-D", 0.5),
        ("Car-E", 1.2),
    ]

    output.append("PARKING CAPACITY WITH SEMAPHORE")
    output.append("=" * 70)
    output.append("Capacity: 3 spots")
    output.append(f"Cars waiting: {len(cars)}")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    processes = []
    for name, duration in cars:
        p = multiprocessing.Process(
            target=parking_worker,
            args=(name, duration, semaphore, parked_count, lock, log_queue)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not log_queue.empty():
        output.append(log_queue.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 5: پارکینگ با ظرفیت محدود با Semaphore")
    explanation.append("")
    explanation.append("Semaphore(3) مثل یک نگهبان پارکینگ با 3 جای خالی عمل می‌کند.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("هر ماشین وارد شونده semaphore.acquire() صدا می‌زند -> مقدار -1")
    explanation.append("وقتی مقدار 0 شود، بقیه ماشین‌ها باید منتظر بمانند.")
    explanation.append("هر ماشین خارج شونده semaphore.release() صدا می‌زند -> مقدار +1")
    explanation.append("")
    explanation.append("یک Lock جداگانه هم لازم است؛")
    explanation.append("Semaphore فقط تعداد دسترسی همزمان را کنترل می‌کند؛")
    explanation.append("محافظت از parked_count.value (شمارنده مشترک) وظیفه Lock است.")
    explanation.append("این دو ابزار برای دو کار متفاوت استفاده می‌شوند.")
    explanation.append("")
    explanation.append("تفاوت Semaphore با Lock:")
    explanation.append("Lock فقط اجازه 1 دسترسی همزمان می‌دهد (مثل Semaphore(1)).")
    explanation.append("Semaphore(n) اجازه n دسترسی همزمان می‌دهد.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# ==============================================================
# سناریو 6: انتقال وجه با فراخوانی تو در تو با RLock
# ==============================================================

def validate_account(balance, amount, op_type):
    if amount <= 0:
        return False
    if op_type == "withdraw" and amount > balance:
        return False
    return True


def withdraw(balance, amount, rlock, log_queue):
    time.sleep(random.uniform(0.2,1))
    p_name=multiprocessing.current_process().name
    with rlock:
        if not validate_account(balance.value, amount, "withdraw"):
            log_queue.put(f"{timestamp()}    {p_name:<25s} Withdrawal FAILED (insufficient funds)")
            return False
        old = balance.value
        balance.value -= amount
        log_queue.put(f"{timestamp()}    {p_name:<25s} Withdrawal successful: {old} -> {balance.value}")
        return True


def deposit(balance, amount, rlock, log_queue):
    time.sleep(random.uniform(0.2,1))
    p_name=multiprocessing.current_process().name
    with rlock:
        if not validate_account(balance.value, amount, "deposit"):
            return False
        old = balance.value
        balance.value += amount
        log_queue.put(f"{timestamp()}    {p_name:<25s} Deposit successful: {old} -> {balance.value}")
        return True


def transfer(name1, bal1, lock1, name2, bal2, lock2, amount, log_queue):
    time.sleep(random.uniform(0.2,1))
    p_name=multiprocessing.current_process().name
    with lock1:
        log_queue.put(f"{timestamp()}    {p_name:<25s} Transfer {amount} from {name1} to {name2}")
        if withdraw(bal1, amount, lock1, log_queue):
            deposit(bal2, amount, lock2, log_queue)
            log_queue.put(f"{timestamp()}    {p_name:<25s} TRANSFER Completed successfully.")
        else:
            log_queue.put(f"{timestamp()}    {p_name:<25s} Failed...")


def run_rlock_scenario():
    output      = []
    explanation = []

    log_queue = multiprocessing.Queue()

    ali_bal,  ali_rlock  = multiprocessing.Value("i", 3000), multiprocessing.RLock()
    reza_bal, reza_rlock = multiprocessing.Value("i", 3000), multiprocessing.RLock()

    output.append("BANKING TRANSFERS WITH RLOCK")
    output.append("=" * 70)
    output.append(f"Initial balances -> Ali: {ali_bal.value} | Reza: {reza_bal.value}")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    p1 = multiprocessing.Process(name="Ali-Withdraw", target=withdraw,         args=(ali_bal, 2000, ali_rlock, log_queue))
    p2 = multiprocessing.Process(name="AliToReza-Transfer", target=transfer,  args=("Ali", ali_bal, ali_rlock, "Reza", reza_bal, reza_rlock, 1500, log_queue))
    p3 = multiprocessing.Process(name="Reza-Deposit", target=deposit,           args=(reza_bal, 500, reza_rlock, log_queue))
    p4 = multiprocessing.Process(name="Reza-Withdraw", target=withdraw,           args=(reza_bal, 1500, reza_rlock, log_queue))
    p5 = multiprocessing.Process(name="Ali-Deposit", target=deposit,           args=(ali_bal, 1000, ali_rlock, log_queue))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    while not log_queue.empty():
        output.append(log_queue.get())

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append(f"Final balances -> Ali: {ali_bal.value} | Reza: {reza_bal.value}")
    output.append(f"Execution time : {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 6: انتقال وجه با فراخوانی تو در تو با RLock")
    explanation.append("")
    explanation.append("سه فرایند مستقل روی دو حساب مشترک کار می‌کنند:")
    explanation.append("p1 : از حساب Ali برداشت می‌کند")
    explanation.append("p2 : از Ali به Reza انتقال می‌دهد(Transfer)")
    explanation.append("p3 : به حساب Reza واریز می‌کند")
    explanation.append("p4 : از حساب Reza برداشت می‌کند")
    explanation.append("")
    explanation.append("زنجیره فراخوانی تو در تو در p2:")
    explanation.append("transfer_process با lock1 قفل حساب Ali را می‌گیرد.")
    explanation.append("سپس withdraw را صدا می‌زند که دوباره همان lock1 را درخواست می‌کند.")
    explanation.append("")
    explanation.append("اینجا Lock معمولی کار نمی‌کند؛")
    explanation.append("اگر lock1 از نوع Lock معمولی بود:")
    explanation.append("transfer_process قفل را می‌گیرد.")
    explanation.append("withdraw می‌خواهد همان قفل را دوباره بگیرد.")
    explanation.append("قفل هرگز آزاد نمی‌شود -> Self-Deadlock.")
    explanation.append("")
    explanation.append("RLock این مشکل را حل می‌کند؛")
    explanation.append("RLock یک شمارنده داخلی دارد که تعداد acquire توسط همان فرایند را می‌شمارد")
    explanation.append("و اجازه ورود مجدد به همان فرایند را می‌دهد.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_sync_scenario(scenario_id: int):
    scenarios = {
        1: run_barrier_scenario,
        2: run_lock_scenario,
        3: run_event_scenario,
        4: run_condition_scenario,
        5: run_semaphore_scenario,
        6: run_rlock_scenario,
    }

    if scenario_id not in scenarios:
        raise ValueError(
            f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3, 4, 5, 6"
        )

    return scenarios[scenario_id]()