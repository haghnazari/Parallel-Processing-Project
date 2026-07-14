import multiprocessing
import random
import time
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


class Producer(multiprocessing.Process):
    def __init__(self, data_queue, log_queue):
        multiprocessing.Process.__init__(self)
        self.data_queue = data_queue
        self.log_queue = log_queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.data_queue.put(item)
            try:
                q_size = self.data_queue.qsize()
            except NotImplementedError:
                q_size = "N/A"
            self.log_queue.put(
                f"{timestamp()}    Process Producer : item {item:<3d} appended to queue {self.name:<10s}| Queue size = {q_size}"
            )
            time.sleep(0.5)
        self.log_queue.put(f"{timestamp()}    Producer finished generating items.")


class Consumer(multiprocessing.Process):
    def __init__(self, data_queue, log_queue):
        multiprocessing.Process.__init__(self)
        self.data_queue = data_queue
        self.log_queue = log_queue

    def run(self):
        time.sleep(
            0.5
        )  # حل مشکل کتاب: در کتاب باید اسلیپ اول اینجا نوشته میشد نه در بلوک الس
        while True:
            if self.data_queue.empty():
                self.log_queue.put(f"{timestamp()}    Consumer: the queue is empty")
                break
            else:
                item = self.data_queue.get()
                try:
                    q_size = self.data_queue.qsize()
                except NotImplementedError:
                    q_size = "N/A"
                self.log_queue.put(
                    f"{timestamp()}    Process Consumer : item {item:<3d} popped by {self.name:<10s}| Queue size = {q_size}"
                )
                time.sleep(1)


class ImageUploader(multiprocessing.Process):
    def __init__(self, task_queue, log_queue):
        multiprocessing.Process.__init__(self)
        self.name = "Upload-Process"
        self.task_queue = task_queue
        self.log_queue = log_queue

    def run(self):
        for i in range(1, 4):
            time.sleep(0.5)
            image = f"image_{i}"
            self.log_queue.put(f"{timestamp()}    {self.name + ':':<20s}User uploaded {image}")
            self.task_queue.put(image)
            time.sleep(0.5)
        self.log_queue.put(
            f"{timestamp()}    {self.name + ':':<20s}All images uploaded. Exiting."
        )


class ImageWorker(multiprocessing.Process):
    def __init__(self, worker_id, task_queue, log_queue):
        multiprocessing.Process.__init__(self)
        self.name = f"Worker-{worker_id}"
        self.task_queue = task_queue
        self.log_queue = log_queue

    def run(self):
        while True:
            image = self.task_queue.get()
            if image is None:
                self.log_queue.put(
                    f"{timestamp()}    {self.name + ':':<20s}Received stop signal. Exiting."
                )
                break
            self.log_queue.put(
                f"{timestamp()}    {self.name + ':':<20s}Processing {image} ..."
            )
            time.sleep(random.uniform(0.5, 1.5))
            self.log_queue.put(
                f"{timestamp()}    {self.name + ':':<20s}Finished {image} and saved to disk."
            )


class PrintUser(multiprocessing.Process):
    def __init__(self, user_name, document, print_queue, log_queue):
        multiprocessing.Process.__init__(self)
        self.name = user_name
        self.document = document
        self.print_queue = print_queue
        self.log_queue = log_queue

    def run(self):
        time.sleep(random.uniform(0.1, 0.5))
        self.print_queue.put((self.name, self.document))
        self.log_queue.put(f"{timestamp()}    {self.name+ ':':<20s}Submitted {self.document}")


class PrinterServer(multiprocessing.Process):
    def __init__(self, print_queue, log_queue):
        multiprocessing.Process.__init__(self)
        self.name = "Printer"
        self.print_queue = print_queue
        self.log_queue = log_queue

    def run(self):
        while True:
            job = self.print_queue.get()
            if job is None:
                self.log_queue.put(
                    f"{timestamp()}    {self.name+ ':':<20s}Received stop signal. Shutting down."
                )
                break
            user, doc = job
            self.log_queue.put(
                f"{timestamp()}    {self.name+ ':':<20s}Started {doc} (Owner: {user})"
            )
            time.sleep(1.2)
            self.log_queue.put(f"{timestamp()}    {self.name+ ':':<20s}Finished {doc}")


# سناریو 1: تولیدکننده و مصرف‌کننده با Process Queue
def queue_scenario1():
    output = []
    explanation = []

    data_queue = multiprocessing.Queue()
    log_queue = multiprocessing.Queue()

    output.append("PRODUCER / CONSUMER — Process Queue")
    output.append("=" * 70)

    start_time = time.time()

    producer = Producer(data_queue, log_queue)
    consumer = Consumer(data_queue, log_queue)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    exec_time = time.time() - start_time

    while not log_queue.empty():
        output.append(log_queue.get())

    output.append("")
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 1: تولیدکننده و مصرف‌کننده با Queue (طبق کتاب)")
    explanation.append("")
    explanation.append(
        "Producer و Consumer هر دو زیرکلاس multiprocessing.Process هستند"
    )
    explanation.append("و دو Queue مشترک از طریق سازنده کلاس دریافت می‌کنند:")
    explanation.append("• data_queue : برای انتقال داده واقعی (اعداد تصادفی)")
    explanation.append("• log_queue  : برای انتقال پیام‌های وضعیت به فرایند اصلی")
    explanation.append("")
    explanation.append("نحوه عملکرد Producer:")
    explanation.append("1- در هر تکرار یک عدد تصادفی تولید می‌کند")
    explanation.append("2- با data_queue.put(item) آن را داخل صف داده می‌گذارد")
    explanation.append("3- این کار را 10 بار با فاصله 1 ثانیه تکرار می‌کند")
    explanation.append("")
    explanation.append("نحوه عملکرد Consumer:")
    explanation.append("1- بررسی می‌کند آیا صف داده خالی است: data_queue.empty()")
    explanation.append("2- اگر خالی نبود، با data_queue.get() یک آیتم برمی‌دارد")
    explanation.append("3- اگر خالی بود، حلقه را با break می‌شکند و کار تمام می‌شود")
    explanation.append("")
    explanation.append("چرا دو Queue جداگانه لازم است؟")
    explanation.append("اگر فقط یک Queue داشتیم، پیام‌های متنی لاگ")
    explanation.append("با داده واقعی (اعداد) قاطی می‌شدند.")
    explanation.append("جداسازی کانال داده از کانال لاگ یک الگوی درست و رایج است.")
    explanation.append("")
    explanation.append("چرا اصلاً به Queue نیاز داریم؟")
    explanation.append("برخلاف Thread، فرایندها حافظه مشترک ندارند.")
    explanation.append("multiprocessing.Queue از طریق pipe و pickle داده را بین")
    explanation.append("فرایندهای کاملاً مستقل منتقل می‌کند.")
    explanation.append("")
    explanation.append("--- نکته شب امتحان ---")
    explanation.append("اگر Consumer سریع‌تر از Producer اجرا شود،")
    explanation.append("ممکن است صف را خالی ببیند و زودتر از موعد break بزند")
    explanation.append("در حالی که Producer هنوز آیتم تولید می‌کند.")
    explanation.append("این محدودیت شناخته‌شده الگوی ساده کتاب است؛")
    explanation.append(
        "راه‌حل بهتر استفاده از JoinableQueue با task_done/join است (سناریو 2 و 3)."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: پردازش تصاویر با فرآیند (یک به چند)
def queue_scenario2():
    output = []
    explanation = []

    task_queue = multiprocessing.Queue()
    log_queue = multiprocessing.Queue()

    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    output.append("IMAGE PROCESSING SERVER — Queue")
    output.append("=" * 65)
    output.append(f"Main process : {name}")
    output.append(f"Main PID     : {pid}")
    output.append("=" * 65)
    output.append("")

    start_time = time.time()

    workers = [ImageWorker(i, task_queue, log_queue) for i in range(1, 4)]
    uploader = ImageUploader(task_queue, log_queue)

    for w in workers:
        w.start()
    uploader.start()

    uploader.join()

    log_queue.put(
        f"{timestamp()}    {name+ ':':<20s}Sending stop signal to workers..."
    )

    for _ in workers:
        task_queue.put(None)

    for w in workers:
        w.join()

    log_queue.put(f"{timestamp()}    {name+ ':':<20s}ALL IMAGES PROCESSED & SAVED SUCCESSFULLY.")

    exec_time = time.time() - start_time

    while not log_queue.empty():
        output.append(log_queue.get())

    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 2: پردازش تصاویر با فرایند (1 Uploader، 3 Worker)")
    explanation.append("")
    explanation.append(
        "ImageUploader و ImageWorker هر دو زیرکلاس multiprocessing.Process هستند"
    )
    explanation.append("و برای تبادل داده از یک Queue استفاده می‌کنند.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append(
        "1- ImageUploader.run() هر عکس را با self.task_queue.put() اضافه می‌کند"
    )
    explanation.append(
        "2- هر ImageWorker بیکار با self.task_queue.get() یک عکس برمی‌دارد"
    )
    explanation.append(
        "3- بعد از اتمام آپلود، فرایند اصلی به تعداد Workerها سیگنال  None می‌فرستد"
    )
    explanation.append(
        "4- هر Worker با دریافت None از حلقه خارج می‌شود و فرایندش تمام می‌شود"
    )
    explanation.append("")
    explanation.append(
        "Queue معمولی راهی برای دانستن «چه زمانی همه کارها تمام شد» ندارد"
    )
    explanation.append("(بر خلاف JoinableQueue که task_done/join دارد).")
    explanation.append("راه‌حل رایج ارسال یک مقدار ویژه(Sentinel Value) مثل None است")
    explanation.append("که هر Worker با دیدن آن متوجه پایان کار می‌شود.")
    explanation.append("هر فرآیند به صورت کاملاً امن و مستقل زمان خروج خود را متوجه می‌شود.")
    explanation.append("")
    explanation.append("هر Worker فقط یک بار از حلقه while خارج می‌شود؛")
    explanation.append(
        "برای متوقف کردن هر سه Worker باید سه پیام None جداگانه بفرستیم."
    )
    explanation.append("")
    explanation.append("--- نکته شب امتحان ---")
    explanation.append("این الگو Load Balancing نام دارد: چند Worker مستقل")
    explanation.append(
        "کار را از یک صف مشترک برمی‌دارند و بار به‌صورت خودکار توزیع می‌شود."
    )
    explanation.append(
        "تفاوت با سناریو 1: سناریو 1 پایان کار را با queue.empty() تشخیص می‌داد؛"
    )
    explanation.append("این‌جا چون چند Worker داریم و ترتیب پردازش نامشخص است،")
    explanation.append("سیگنال (None) قابل اعتمادتر از بررسی empty() است.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: سیستم چاپ شبکه‌ای با فرآیند (چند به یک)
def queue_scenario3():
    output = []
    explanation = []

    print_queue = multiprocessing.Queue()
    log_queue = multiprocessing.Queue()

    name = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    
    output.append("NETWORK PRINT SERVER")
    output.append("=" * 65)
    output.append(f"Main process : {name}")
    output.append(f"Main PID     : {pid}")
    output.append("=" * 65)
    output.append("")

    start_time = time.time()

    printer = PrinterServer(print_queue, log_queue)

    clients = [
        ("Ali", "Thesis.pdf"),
        ("Sara", "Report.docx"),
        ("Reza", "Invoice.pdf"),
    ]

    users = [PrintUser(name, doc, print_queue, log_queue) for name, doc in clients]

    printer.start()
    for u in users:
        u.start()
    for u in users:
        u.join()

    log_queue.put(
        f"{timestamp()}    {name+ ':':<20s}All jobs submitted. Sending stop signal to printer..."
    )

    print_queue.put(None)
    printer.join()

    log_queue.put(f"{timestamp()}    {name+ ':':<20s}ALL PRINT JOBS COMPLETED. PRINTER GOES TO SLEEP.")

    exec_time = time.time() - start_time
    
    while not log_queue.empty():
        output.append(log_queue.get())

    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 3: سیستم چاپ شبکه‌ای با فرایند (3 User، 1 Printer)")
    explanation.append("")
    explanation.append(
        "PrintUser و PrinterServer هر دو زیرکلاس multiprocessing.Process هستند"
    )
    explanation.append("و برای تبادل داده از یک Queue استفاده می‌کنند.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append(
        "1- هر PrintUser.run() سند خودش را با self.print_queue.put() ثبت می‌کند"
    )
    explanation.append(
        "2- PrinterServer.run() با self.print_queue.get() اسناد را به ترتیب برمی‌دارد و چاپ می‌کند"
    )
    explanation.append(
        "3- چون فقط یک Printer داریم، چاپ‌ها به ترتیب ورود انجام می‌شود (FIFO)"
    )
    explanation.append("")
    explanation.append(
        "فرایند اصلی صبر می‌کند تا همه کاربران join شوند، قبل از فرستادن None."
    )
    explanation.append("تا وقتی همه کاربران کارشان تمام نشده،")
    explanation.append("ممکن است سندی هنوز به صف اضافه نشده باشد.")
    explanation.append("اگر None زودتر فرستاده شود، ممکن است Printer قبل از دریافت")
    explanation.append("همه اسناد، سیگنال پایان را ببیند و برخی اسناد چاپ نشوند.")
    explanation.append("")
    explanation.append("این الگو Serialization یا N-to-1 نام دارد؛")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_queue_scenario(scenario_id: int):
    scenarios = {
        1: queue_scenario1,
        2: queue_scenario2,
        3: queue_scenario3,
    }

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
