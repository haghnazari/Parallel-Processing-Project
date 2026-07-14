import threading
import time
import random
from threading import Thread


# سناریو اول: مثال کتاب
def rlock_scenario1():
    output = []
    explanation = []

    class Box:
        def __init__(self):
            self.lock = threading.RLock()
            self.total_items = 0

        def execute(self, value):
            with self.lock:
                self.total_items += value

        def add(self):
            with self.lock:
                self.execute(1)

        def remove(self):
            with self.lock:
                self.execute(-1)

    def adder(box, items):
        output.append(f"N° {items} items to ADD")
        while items:
            box.add()
            time.sleep(0.5)
            items -= 1
            output.append(f"ADDED one item --> {items} item to ADD")

    def remover(box, items):
        output.append(f"N° {items} items to REMOVE")
        while items:
            box.remove()
            time.sleep(0.5)
            items -= 1
            output.append(f"REMOVED one item --> {items} item to REMOVE")

    start_time = time.time()
    box = Box()

    t1 = threading.Thread(target=adder, args=(box, random.randint(10, 20)))
    t2 = threading.Thread(target=remover, args=(box, random.randint(1, 10)))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    exec_time = time.time() - start_time

    output.append(f"\n📊 Final total items: {box.total_items}")
    output.append(f"⏱️ Execution time: {exec_time:.3f} seconds")

    explanation.append("📚 سناریو 1: سیستم مدیریت جعبه با RLock")
    explanation.append("")
    explanation.append("🔑 **نحوه عملکرد RLock در این کد:**")
    explanation.append("1️⃣ متد add() ابتدا قفل را می‌گیرد (acquire)")
    explanation.append("2️⃣ سپس متد execute() را صدا می‌زند که دوباره قفل را می‌گیرد")
    explanation.append("3️⃣ اگر از Lock معمولی استفاده می‌شد، Deadlock رخ می‌داد")
    explanation.append("4️⃣ اما RLock به همان نخ اجازه قفل مجدد می‌دهد")
    explanation.append("")
    explanation.append("📊 **مقایسه با Lock:**")
    explanation.append("• Lock: ❌ در فراخوانی‌های تو در تو قفل می‌کند")
    explanation.append("• RLock: ✅ اجازه قفل مجدد توسط همان نخ را می‌دهد")
    explanation.append("")
    explanation.append("📌 **نکته مهم:**")
    explanation.append(
        "RLock یک شمارنده (counter) دارد که تعداد دفعات acquire را می‌شمرد"
    )
    explanation.append("و به همان تعداد release نیاز دارد تا قفل آزاد شود")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو دوم: سیستم بانکی و عملیات تو در تو
def rlock_scenario2():
    output = []
    explanation = []

    class BankAccount:

        def __init__(self, owner, account_number, balance):
            self.owner = owner
            self.account_number = account_number
            self.balance = balance
            self.lock = threading.RLock()

        def __repr__(self):
            return self.owner

        def _validate(self, tx_id, amount, operation):
            with self.lock:
                if amount <= 0:
                    output.append(
                        f"\nTransaction #{tx_id} Reject: [{self.owner}] Invalid amount: {amount}"
                    )
                    return False
                if operation == "withdraw" and amount > self.balance:
                    output.append(
                        f"\nTransaction #{tx_id} Reject: [{self.owner}] Insufficient balance (Available={self.balance}, Requested={amount})"
                    )
                    return False
                return True

        def deposit(self, tx_id, amount):
            with self.lock:
                if not self._validate(tx_id, amount, "deposit"):
                    return False
                old_balance = self.balance
                time.sleep(2)
                self.balance += amount
                output.append(
                    f"\nTransaction #{tx_id}: [{self.owner}] Deposit successful: {old_balance} -> {self.balance}"
                )
                return True

        def withdraw(self, tx_id, amount):
            with self.lock:
                if not self._validate(tx_id, amount, "withdraw"):
                    return False
                old_balance = self.balance
                time.sleep(2)
                self.balance -= amount
                output.append(
                    f"\nTransaction #{tx_id}: [{self.owner}] Withdrawal successful: {old_balance} -> {self.balance}"
                )
                return True

        def transfer(self, tx_id, target_account, amount):
            if self.account_number < target_account.account_number:
                first_lock, second_lock = self.lock, target_account.lock
            else:
                first_lock, second_lock = target_account.lock, self.lock

            with first_lock:
                with second_lock:
                    if not self.withdraw(tx_id, amount):
                        return False
                    target_account.deposit(tx_id, amount)
                    return True

    class Transaction(Thread):
        def __init__(
            self,
            transaction_id,
            transaction_type,
            source_account,
            amount,
            target_account=None,
        ):
            Thread.__init__(self)
            self.transaction_id = transaction_id
            self.transaction_type = transaction_type
            self.source_account = source_account
            self.target_account = target_account
            self.amount = amount

        def run(self):
            if self.transaction_type == "deposit":
                output.append(
                    f"\nTransaction #{self.transaction_id}: [DEPOSIT] to {self.source_account} | Amount: {self.amount}"
                )
                self.source_account.deposit(self.transaction_id, self.amount)

            elif self.transaction_type == "withdraw":
                output.append(
                    f"\nTransaction #{self.transaction_id}: [WITHDRAW] from {self.source_account} | Amount: {self.amount}"
                )
                self.source_account.withdraw(self.transaction_id, self.amount)

            elif self.transaction_type == "transfer":
                output.append(
                    f"\nTransaction #{self.transaction_id}: [TRANSFER] from {self.source_account} to {self.target_account} | Amount: {self.amount}"
                )
                success = self.source_account.transfer(
                    self.transaction_id, self.target_account, self.amount
                )
                if success:
                    # ✅ اصلاح شد: self.owner به self.source_account و target_account به self.target_account تغییر یافت
                    output.append(
                        f"Transaction #{self.transaction_id}: [TRANSFER] {self.amount} from {self.source_account} to {self.target_account} completed"
                    )
                else:
                    output.append(
                        f"Transaction #{self.transaction_id}: [TRANSFER] {self.amount} from {self.source_account} to {self.target_account} Failed."
                    )

            output.append(f"Transaction #{self.transaction_id} finished")

    # ==================================================
    accounts = {
        "Ali": BankAccount("Ali", 101, 5000),
        "Sara": BankAccount("Sara", 102, 3500),
        "Reza": BankAccount("Reza", 103, 7000),
        "Maryam": BankAccount("Maryam", 104, 4200),
    }

    output.append("=" * 70)
    output.append("BANKING SYSTEM")
    output.append("=" * 70)
    output.append("\nInitial Balances:")
    for acc in accounts.values():
        output.append(f"{acc.owner:10s} ({acc.account_number}) : {acc.balance}")

    transactions = [
        Transaction(1, "withdraw", accounts["Ali"], 1000),
        Transaction(2, "transfer", accounts["Ali"], 1500, accounts["Reza"]),
        Transaction(3, "deposit", accounts["Sara"], 500),
        Transaction(4, "withdraw", accounts["Reza"], 2000),
        Transaction(5, "transfer", accounts["Reza"], 1000, accounts["Ali"]),
        Transaction(6, "transfer", accounts["Maryam"], 700, accounts["Sara"]),
        Transaction(7, "withdraw", accounts["Sara"], 1000),
    ]

    start_time = time.time()
    output.append("\nStarting Transactions...\n")

    for t in transactions:
        t.start()
    for t in transactions:
        t.join()

    exec_time = time.time() - start_time

    output.append("\n" + "=" * 70)
    output.append("FINAL BALANCES")
    output.append("=" * 70)
    for acc in accounts.values():
        output.append(f"{acc.owner:10s} ({acc.account_number}) : {acc.balance}")
    output.append(f"\nExecution time: {exec_time:.2f} seconds")

    explanation.append("سناریو 2: سیستم بانکی با RLock")
    explanation.append("")
    explanation.append("۱. برخورد دو تراکنش همزمان روی یک حساب (Race Condition):")
    explanation.append(
        "اگر دو نخ بخواهند همزمان حساب علی را تغییر دهند (یکی برداشت و دیگری واریز کند):"
    )
    explanation.append(
        "- نخ اول قفل حساب علی را تصاحب میکند و نخ دوم پشت در قفل منتظر (Blocked) میماند."
    )
    explanation.append(
        "- این کار از خرابی داده ها جلوگیری کرده و ثبات موجودی نهایی را تضمین میکند."
    )
    explanation.append("")
    explanation.append("۲. نقش حیاتی RLock (قفل بازگشتی):")
    explanation.append("هنگام انتقال وجه (transfer):")
    explanation.append("- متد transfer قفل حساب مبدا را میگیرد.")
    explanation.append("- از داخل همان بلاک قفل شده، متد withdraw را صدا میزند.")
    explanation.append("- متد withdraw نیز دوباره قفل همان حساب را درخواست میکند.")
    explanation.append(
        "- اگر از Lock معمولی استفاده شود: نخ پشت در قفلی که خودش نگه داشته میماند و برنامه تا ابد متوقف میشود (Self-Deadlock)."
    )
    explanation.append(
        "- با RLock: سیستم مالکیت نخ را تشخیص میدهد و اجازه ورود مجدد و تو در تو را بدون ایجاد بن بست صادر میکند."
    )
    explanation.append("")
    explanation.append("۳. جلوگیری از ددلاک دوطرفه (Lock Ordering):")
    explanation.append(
        "اگر علی به رضا پول واریز کند و همزمان رضا به علی پول بزند، یک بن بست چرخشی رخ میدهد."
    )
    explanation.append(
        "با استفاده از شرط 'if self.account_number < target_account.account_number'، "
        "قفل ها همیشه با یک ترتیب ثابت (شماره حساب کوچک تر) گرفته میشوند. "
        "این کار نخ ها را مجبور به رعایت اولویت کرده و ددلاک متقاطع را کاملا خنثی میکند."
    )

    return {
        "output": "\n".join(output),
        "explanation": "\n".join(explanation),
    }


#  سناریو سوم: ایستگاه هواشناسی
def rlock_scenario3():

    output = []
    explanation = []

    class WeatherStation:

        def __init__(self):
            self.temperature = 0
            self.humidity = 0
            self.lock = threading.RLock()

        def save_temperature(self, temp_value):
            with self.lock:
                thread_name = threading.current_thread().name
                output.append(f"[{thread_name}] 🌡️ Saving temperature: {temp_value}°C")
                time.sleep(0.2)  # شبیه‌سازی زمان ثبت در سخت‌افزار سنسور
                self.temperature = temp_value
                output.append(f"[{thread_name}] ✅ Temperature saved")

        def save_humidity(self, humid_value):
            with self.lock:
                thread_name = threading.current_thread().name
                output.append(f"[{thread_name}] 💧 Saving humidity: {humid_value}%")
                time.sleep(0.2)  # شبیه‌سازی زمان ثبت در سخت‌افزار سنسور
                self.humidity = humid_value
                output.append(f"[{thread_name}] ✅ Humidity saved")

        def save_snapshot(self, temp_value, humid_value):
            #ثبت همزمان داده‌های کامل ایستگاه

            with self.lock:
                thread_name = threading.current_thread().name
                output.append("")
                output.append(f"[{thread_name}] 📦 Starting weather snapshot...")
                self.save_temperature(temp_value)
                self.save_humidity(humid_value)

                output.append(f"[{thread_name}] 📦 Snapshot completed")
                output.append("")

    class SensorTask(Thread):

        def __init__(self, station, mode, temperature=None, humidity=None):
            Thread.__init__(self)
            self.station = station
            self.mode = mode
            self.task_temperature = temperature
            self.task_humidity = humidity

        def run(self):
            if self.mode == "SNAPSHOT":
                self.station.save_snapshot(self.task_temperature, self.task_humidity)
            elif self.mode == "TEMPERATURE":
                self.station.save_temperature(self.task_temperature)
            elif self.mode == "HUMIDITY":
                self.station.save_humidity(self.task_humidity)

    # ==================================================
    # اجرای سناریو
    # ==================================================
    station = WeatherStation()

    output.append("=" * 75)
    output.append("🌤️ WEATHER STATION WITH RLock")
    output.append("=" * 75)
    output.append("")

    threads = [
        SensorTask(station, "SNAPSHOT", temperature=25, humidity=60),
        SensorTask(station, "TEMPERATURE", temperature=27),
        SensorTask(station, "HUMIDITY", humidity=65),
    ]

    threads[0].name = "Snapshot-Thread"
    threads[1].name = "Temp-Thread"
    threads[2].name = "Humidity-Thread"

    start_time = time.time()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    exec_time = time.time() - start_time

    # ==================================================
    # گزارش نهایی
    # ==================================================
    output.append("")
    output.append("=" * 75)
    output.append("📊 FINAL SENSOR STATE")
    output.append("=" * 75)
    output.append(f"🌡️ Final Temperature: {station.temperature}°C")
    output.append(f"💧 Final Humidity: {station.humidity}%")
    output.append(f"⏱️ Execution Time: {exec_time:.2f} seconds")

    # ==================================================
    # توضیحات
    # ==================================================
    explanation.append("🌤️ سناریو 3: ثبت اطلاعات ایستگاه هواشناسی با RLock")
    explanation.append("")
    explanation.append("🎯 هدف سناریو:")
    explanation.append(
        "نمایش کاربرد RLock در زمانی که یک متد قفل‌دار، "
        "متدهای قفل‌دار دیگری را فراخوانی می‌کند."
    )
    explanation.append("")
    explanation.append("🔑 نحوه عملکرد:")
    explanation.append("1️⃣ متد save_snapshot ابتدا قفل ایستگاه را می‌گیرد.")
    explanation.append("2️⃣ سپس save_temperature را فراخوانی می‌کند.")
    explanation.append("3️⃣ متد save_temperature دوباره همان قفل را درخواست می‌کند.")
    explanation.append("4️⃣ سپس save_humidity نیز همان قفل را درخواست می‌کند.")
    explanation.append("")
    explanation.append(
        "اگر از Lock معمولی استفاده شود، "
        "نخ Snapshot-Thread هنگام ورود به "
        "save_temperature پشت قفل خودش گیر می‌کند "
        "و Self-Deadlock رخ می‌دهد."
    )
    explanation.append("")
    explanation.append(
        "اما RLock تشخیص می‌دهد که مالک فعلی قفل "
        "همان نخ جاری است؛ بنابراین اجازه ورود مجدد "
        "به بخش بحرانی را صادر می‌کند."
    )
    explanation.append("")
    explanation.append("📌 نتیجه:")
    explanation.append(
        "RLock زمانی استفاده می‌شود که متدهای "
        "قفل‌دار یک شیء، متدهای قفل‌دار دیگری "
        "از همان شیء را فراخوانی کنند."
    )
    explanation.append("")
    explanation.append("💡 کاربردهای واقعی:")
    explanation.append("• سیستم‌های ثبت داده سنسورها")
    explanation.append("• نرم‌افزارهای حسابداری")
    explanation.append("• سیستم‌های بانکی")
    explanation.append("• کلاس‌هایی که متدهای عمومی و خصوصی قفل‌دار دارند")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_rlock_scenario(scenario_id: int):
    scenarios = {1: rlock_scenario1, 2: rlock_scenario2, 3: rlock_scenario3}
    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")
    return scenarios[scenario_id]()
