import threading
from queue import Queue
import time
import random
from datetime import datetime


# سناریو 1: سیستم تولیدکننده/مصرف‌کننده هوشمند با Queue
def queue_scenario1():
    output = []
    explanation = []
    log_lock = threading.Lock()
    
    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")
            
    class Producer(threading.Thread):
        def __init__(self, queue):
            super().__init__()
            self.queue = queue

        def run(self):
            for i in range(5):
                item = random.randint(0, 256)
                self.queue.put(item)
                log(f"Producer notify : item N°{item} appended to queue by {self.name}")
                time.sleep(1)

    class Consumer(threading.Thread):
        def __init__(self, queue):
            super().__init__()
            self.queue = queue

        def run(self):
            while True:
                item = self.queue.get()
                log(f"Consumer notify : {item} popped from queue by {self.name}")
                self.queue.task_done()
    
    
    output.append("PRODUCER / CONSUMER - Queue")
    output.append("=" * 70)
    
    queue = Queue()
    t1 = Producer(queue)
    t2 = Consumer(queue)
    t3 = Consumer(queue)
    t4 = Consumer(queue)
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True
    
    start_time = time.time()
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()

    log(f"{'SYSTEM':<12s} Waiting for queue to be fully processed (queue.join)...")
    queue.join()

    exec_time = time.time() - start_time

    log("ALL ITEMS PROCESSED SUCCESSFULLY. EXITING.")
    output.append(f"\nExecution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("=" * 70)
    explanation.append(" Queue بهترین ابزار همگام‌سازی نخ هاست.")
    explanation.append("=" * 70)
    explanation.append("۱. کپسوله‌سازیِ قفل‌ها (Encapsulation of Locks):")
    explanation.append("   در سناریوهای قبلی (مثل Event) مجبور بودیم برای محافظت از لیست اشتراکی،")
    explanation.append("   دستورات 'with lock' را دستی بنویسیم. اما شیء Queue در پایتون ذاتا Thread-Safe")
    explanation.append("   است. یعنی متدهای put و get در درون خودشان Lock و Condition دارند.")
    explanation.append("-" * 70)
    explanation.append("۲. رفع باگِ کتاب با معماری Daemon و Queue.join:")
    explanation.append("   کدِ کتاب به خاطر حلقه while True در Consumer، دچار بن‌بست (Deadlock) در زمان")
    explanation.append("   خروج می‌شدو نخ‌های مصرف‌کننده برای همیشه منتظر می‌ماندند. برای حل این مشکل، نخ‌های مصرف‌کننده را به صورت Daemon تعریف کردیم.")
    explanation.append("   سپس در نخ اصلی به جای t.join برای مصرف‌کننده‌ها، از متد هوشمندِ queue.join()")
    explanation.append("   استفاده کردیم.")
    explanation.append("-" * 70)
    explanation.append("۳. task_done:")
    explanation.append("   هر بار که put اجرا می‌شود، یک کانتر داخلی در صف بالا می‌رود.")
    explanation.append("   هر بار که task_done اجرا می‌شود، آن کانتر پایین می‌آید.")
    explanation.append("   متد queue.join() برنامه را مسدود نگه می‌دارد تا زمانی که این کانتر دقیقاً به صفر برسد.")
    explanation.append("-" * 70)
    explanation.append("* نخ‌های Daemon زمانی که تمام نخ‌های غیر Daemon برنامه خاتمه پیدا کنند، به صورت خودکار متوقف می‌شوند. بنابراین برنامه منتظر پایان آن‌ها نمی‌ماند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: پردازش تصاویر (یک تولیدکننده، چند مصرف‌کننده) برای تقسیم کار و بالا بردن سرعت
def queue_scenario2():
    output = []
    explanation = []
    log_lock = threading.Lock()
    
    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")
            
    # صف وظایف پردازش تصویر
    image_queue = Queue()
    
    class ImageUploader(threading.Thread):
        def __init__(self, queue):
            super().__init__(name="Upload-Thread")
            self.queue = queue

        def run(self):
            for i in range(1, 4):
                image_name = f"image_{i}"
                log(f"User uploaded {image_name}")
                self.queue.put(image_name)
                time.sleep(0.5)
            log("Producer: All images uploaded. Exiting.")

    class ImageWorker(threading.Thread):
        def __init__(self, queue, worker_id):
            super().__init__(name=f"Worker-{worker_id}")
            self.queue = queue

        def run(self):
            while True:
                image_name = self.queue.get()
                log(f"{self.name} processing {image_name} ...")
                time.sleep(random.uniform(1, 2))
                log(f"{self.name} finished {image_name} and saved to disk.")
                self.queue.task_done()

    output.append("IMAGE PROCESSING SERVER - Task Queue")
    output.append("=" * 70)
    

    uploader = ImageUploader(image_queue)
    workers = []
    for i in range(1, 4):
        w = ImageWorker(image_queue, worker_id=i)
        w.daemon = True
        workers.append(w)
        
    start_time = time.time()
    
    for w in workers:
        w.start()
    uploader.start()

    uploader.join()
    
    log("SYSTEM: Waiting for all images to be processed...")
    image_queue.join()
    log("ALL IMAGES PROCESSED & SAVED SUCCESSFULLY.")
    
    exec_time = time.time() - start_time
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 2: پردازش تصاویر با Task Queue")
    explanation.append("")
    explanation.append("یک نخ uploader عکس‌ها را آپلود می‌کند و سه نخ Worker آن‌ها را پردازش می‌کنند.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- uploader هر عکس را با put() داخل صف می‌گذارد")
    explanation.append("2- هر Worker که بیکار باشد با get() یک عکس از صف برمی‌دارد")
    explanation.append("3- چون get() عملیات اتمیک است، هیچ دو Worker یک عکس را همزمان نمی‌گیرند")
    explanation.append("4- هر Worker بعد از پردازش task_done() صدا می‌زند")
    explanation.append("")
    explanation.append("چرا این سناریو از سناریو 1 بهتر بار را تقسیم می‌کند؟")
    explanation.append("اینجا 3 Worker داریم، نه فقط 1.")
    explanation.append("Workerی که سریع‌تر کارش تمام شود، عکس بعدی را از صف می‌گیرد.")
    explanation.append("این یعنی بار کار خودکار بین Workerها متوازن می‌شود.")
    
    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: سیستم چاپ شبکه‌ای (چند تولیدکننده، یک مصرف‌کننده) برای نظم دادن و جلوگیری از قاطی شدن اطلاعات
def queue_scenario3():
    output = []
    explanation = []
    log_lock = threading.Lock()
    
    def log(msg):
        with log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            output.append(f"{timestamp}    {msg}")
            
    print_queue = Queue()
    
    class User(threading.Thread):
        def __init__(self, user_name, document, queue):
            super().__init__(name=user_name)
            self.user_name = user_name
            self.document = document
            self.queue = queue

        def run(self):
            time.sleep(random.uniform(0.1, 0.5))
            log(f"{self.user_name} submitted {self.document}")
            self.queue.put((self.user_name, self.document))

    class PrinterServer(threading.Thread):
        def __init__(self, queue):
            super().__init__(name="Printer-Device")
            self.queue = queue

        def run(self):
            while True:
                user, doc = self.queue.get()
                
                log(f"Printer started {doc} (Owner: {user})")
                time.sleep(1.2)
                
                log(f"Printer finished {doc}")
                self.queue.task_done()

    output.append("NETWORK PRINT SERVER - Serialization (N-to-1)")
    output.append("=" * 70)
    
    printer = PrinterServer(print_queue)
    printer.daemon = True
    
    # راه‌اندازی کاربران تولیدکننده
    clients = [
        User("Ali", "Thesis.pdf", print_queue),
        User("Sara", "Report.docx", print_queue),
        User("Reza", "Invoice.pdf", print_queue)
    ]
    
    start_time = time.time()
    
    printer.start()
    for user in clients:
        user.start()
        
    for user in clients:
        user.join()
        
    log("SYSTEM: Waiting for printer to empty the Spooler...")
    print_queue.join()
    log("ALL PRINT JOBS COMPLETED. PRINTER GOES TO SLEEP.")
    
    exec_time = time.time() - start_time
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")

    explanation.append("سناریو 3: سیستم چاپ شبکه‌ای با Queue")
    explanation.append("")
    explanation.append("سه کاربر همزمان سند برای چاپ می‌فرستند، اما فقط یک پرینتر وجود دارد.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- هر کاربر سند خودش را با put() داخل صف چاپ می‌گذارد")
    explanation.append("2- پرینتر یکی‌یکی با get() اسناد را از صف برمی‌دارد و چاپ می‌کند")
    explanation.append("3- چون فقط یک پرینتر داریم، اسناد به ترتیب ورود چاپ می‌شوند (FIFO)")
    explanation.append("")
    explanation.append("چرا Queue اینجا بهتر از اتصال مستقیم به پرینتر است؟")
    explanation.append("اگر هر کاربر مستقیم به پرینتر دسترسی داشت، ممکن بود")
    explanation.append("دو سند همزمان قاطی هم چاپ شوند.")
    explanation.append("صف مثل یک منشی عمل می‌کند: درخواست‌ها را می‌گیرد")
    explanation.append("و یکی‌یکی و به ترتیب به پرینتر تحویل می‌دهد.")
    explanation.append("")
    explanation.append("نکته:")
    explanation.append("کاربران بعد از ثبت سند منتظر چاپ نمی‌مانند و کار خودشان را ادامه می‌دهند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}



# *************************************************************
def run_queue_scenario(scenario_id: int):
    scenarios = {1: queue_scenario1, 2: queue_scenario2, 3: queue_scenario3}

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد.")

    return scenarios[scenario_id]()