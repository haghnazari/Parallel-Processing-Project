import threading
import time
import os
from threading import Thread
from random import randint


# *************************************************************
def lock_scenario1():
    counter = 0
    output = []

    class CounterThread(Thread):
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name

        def run(self):
            nonlocal counter
            temp = counter
            output.append(f"---> {self.name} read counter= {temp}")
            time.sleep(0.0001)
            counter = temp + 1
            output.append(f"---> {self.name} write counter = {counter}")

    start_time = time.time()
    threads = []
    for i in range(10):
        t = CounterThread(f"Thread#{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    exec_time = time.time() - start_time
    output.append(f"\n⏱️ Execution time: {exec_time:.3f} seconds")

    explanation = []
    explanation.append(f"✅ مقدار نهایی شمارنده: {counter}")
    explanation.append(
        f"❌ مقدار مورد انتظار: 10 (چون 10 نخ هر کدام 1 بار افزایش دادند)"
    )
    if counter < 10:
        explanation.append(f"⚠️ تعداد افزایش‌های از دست رفته: {10 - counter}")
        explanation.append(
            "🔴 دلیل: Race Condition - چند نخ همزمان مقدار را خواندند و تداخل ایجاد شد"
        )
    else:
        explanation.append("🟢 این بار Race Condition رخ نداد (خوش شانسی!)")

    explanation.append(
        "\n\n✅ در این سناریو، 10 نخ به طور همزمان سعی می‌کنند یک شمارنده مشترک را افزایش دهند."
    )
    explanation.append("\n❌ مشکل Race Condition:")
    explanation.append("- هر نخ مقدار فعلی را می‌خواند")
    explanation.append("- سپس یک کار دیگر انجام می‌دهد (در اینجا sleep)")
    explanation.append("- سپس مقدار را یک واحد افزایش می‌دهد")
    explanation.append(
        "اگر دو نخ همزمان مقدار را بخوانند، هر دو مقدار یکسان را می‌بینند و پس از افزایش، مقدار نهایی فقط یک بار افزایش می‌یابد."
    )
    explanation.append("\n📚 مثال:")
    explanation.append("نخ A: مقدار 5 را می‌خواند")
    explanation.append(
        "نخ B: مقدار 5 را می‌خواند (قبل از اینکه نخ A مقدار نهایی را بنویسد)"
    )
    explanation.append("نخ A: مقدار را به 6 تبدیل می‌کند")
    explanation.append("نخ B: مقدار را به 6 تبدیل می‌کند (اما باید 7 می‌شد!)")
    explanation.append("\n\n💡نتیجه: یک افزایش از دست می‌رود (Race Condition)")
    explanation.append("برای حل این مشکل باید از قفل (Lock) استفاده کنیم.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def lock_scenario2():
    threadLock = threading.Lock()
    counter = 0
    output = []

    class CounterThread(Thread):
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name

        def run(self):
            nonlocal counter
            threadLock.acquire()
            temp = counter
            output.append(f"---> {self.name} read counter = {temp}")
            time.sleep(0.0001)
            counter = temp + 1
            output.append(f"---> {self.name} write counter = {counter}")
            threadLock.release()

    start_time = time.time()
    threads = []
    for i in range(10):
        t = CounterThread(f"Thread#{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    exec_time = time.time() - start_time

    output.append(f"\n⏱️ Execution time: {exec_time:.3f} seconds")

    explanation = []
    explanation.append(f"✅ مقدار نهایی شمارنده: {counter}")
    explanation.append(
        f"🎯 مقدار مورد انتظار: 10 (چون 10 نخ هر کدام 1 بار افزایش دادند)"
    )
    explanation.append("")
    explanation.append("🔒 نتیجه: همگام‌سازی با قفل موفقیت‌آمیز بود!")
    explanation.append("✅ هیچ افزایشی از دست نرفته است")
    explanation.append("✅ Race Condition رخ نداده است")
    explanation.append("")
    explanation.append("📚 توضیح عملکرد قفل (Lock):")
    explanation.append("-" * 40)
    explanation.append("1️⃣ هر نخ قبل از ورود به بخش بحرانی، قفل را می‌گیرد (acquire)")
    explanation.append("2️⃣ اگر قفل در دست نخ دیگری باشد، نخ منتظر می‌ماند")
    explanation.append("3️⃣ نخ بعد از اتمام کار، قفل را آزاد می‌کند (release)")
    explanation.append("4️⃣ نخ بعدی می‌تواند قفل را بگیرد و وارد شود")
    explanation.append("")
    explanation.append("💡 نتیجه‌گیری:")
    explanation.append(
        "قفل (Lock) از تداخل نخ‌ها جلوگیری می‌کند و صحت داده را تضمین می‌نماید،"
    )
    explanation.append("اما به دلیل اجرای ترتیبی بخش بحرانی، زمان اجرا افزایش می‌یابد.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def lock_scenario3():
    bank_lock = threading.Lock()
    balance = 1000  # Initial account balance
    output = []
    transaction_count = 0
    failed_transactions = 0

    class BankTransaction(Thread):
        def __init__(self, name, amount, transaction_type):
            Thread.__init__(self)
            self.name = name
            self.amount = amount
            self.transaction_type = transaction_type  # "Deposit" or Withdraw"

        def run(self):
            nonlocal balance, transaction_count, failed_transactions
            bank_lock.acquire()
            old_balance = balance
            output.append(
                f"START    ----> {self.name}: type={self.transaction_type}, amount={self.amount}, balance_before={old_balance}"
            )
            time.sleep(0.01)
            if self.transaction_type == "Deposit":
                balance += self.amount
                output.append(
                    f"DEPOSIT ----> {self.name}: +{self.amount} | new_balance={balance}"
                )
                transaction_count += 1

            elif self.transaction_type == "Withdraw":
                if balance >= self.amount:
                    balance -= self.amount
                    output.append(
                        f"WITHDRAW ----> {self.name}: -{self.amount} | new_balance={balance}"
                    )
                    transaction_count += 1
                else:
                    output.append(
                        f"REJECTED ----> {self.name}: withdraw {self.amount} FAILED! (insufficient balance: {balance})"
                    )
                    failed_transactions += 1
            time.sleep(0.005)
            output.append(f"END      ----> {self.name}: Final_balance={balance}\n")

            bank_lock.release()

    start_time = time.time()

    transactions = []
    for i in range(10):
        amount = randint(300, 800)
        ta = ["Deposit", "Withdraw"][randint(0, 1)]
        t = BankTransaction(f"{ta}#{i+1}", amount, ta)
        transactions.append(t)

    output.append(f"🏦 STARTING BANKING OPERATION | Initial balance: {balance}")
    output.append(f"📊 Total transactions: 10")
    output.append("")

    for t in transactions:
        t.start()

    for t in transactions:
        t.join()

    exec_time = time.time() - start_time

    # 📊 Final result
    output.append("")
    output.append("=" * 60)
    output.append("📊 FINAL REPORT:")
    output.append(f"💰 Initial balance: 1000")
    output.append(f"💰 Final balance: {balance}")
    output.append(f"✅ Successful transactions: {transaction_count}")
    output.append(f"❌ Failed transactions: {failed_transactions}")
    output.append(f"📈 Balance change: {balance - 1000:+d}")
    output.append(f"⏱️ execution time: {exec_time:.3f} seconds")
    output.append("=" * 60)

    # 📝 Explanation (unchanged - Persian)
    explanation = []
    explanation.append("🏦 سناریو: شبیه‌سازی سیستم بانکی با قفل")
    explanation.append(
        "چندین کاربر همزمان به یک حساب بانکی متصل می‌شوند و تراکنش انجام می‌دهند."
    )
    explanation.append("بدون قفل، ممکن است موجودی حساب به اشتباه محاسبه شود.")
    explanation.append("")
    explanation.append("🔒 نقش قفل در این سناریو:")
    explanation.append("1️⃣ هر تراکنش قبل از دسترسی به موجودی، قفل را می‌گیرد")
    explanation.append(
        "2️⃣ در طول بررسی و انجام تراکنش، هیچ تراکنش دیگری نمی‌تواند موجودی را تغییر دهد"
    )
    explanation.append(
        "3️⃣ بعد از اتمام تراکنش، قفل آزاد می‌شود تا تراکنش بعدی انجام شود"
    )
    explanation.append("")
    explanation.append("✅ مزایای استفاده از قفل در سیستم بانکی:")
    explanation.append("- جلوگیری از برداشت همزمان بیشتر از موجودی")
    explanation.append("- ثبت دقیق همه تراکنش‌ها بدون تداخل")
    explanation.append("- جلوگیری از Race Condition در محاسبه موجودی")
    explanation.append("- حفظ یکپارچگی داده‌ها (Data Integrity)")
    explanation.append("")
    explanation.append("⚠️ اگر قفل نبود چه می‌شد؟")
    explanation.append("❌ دو برداشت همزمان ممکن بود از موجودی ناکافی انجام شود")
    explanation.append("❌ موجودی نهایی حساب اشتباه محاسبه می‌شد")
    explanation.append("❌ برخی تراکنش‌ها ثبت نمی‌شدند (از دست رفتن داده)")
    explanation.append("")
    explanation.append("💡 نتیجه‌گیری :")
    explanation.append(
        "این سناریو نشان می‌دهد که چگونه قفل (Lock) در سیستم‌های واقعی مانند بانک‌ها، صف‌های خرید، رزرو بلیط، و انبارداری استفاده می‌شود."
    )
    explanation.append(
        "قفل تضمین می‌کند که عملیات همزمان روی داده‌های مشترک، صحیح و بدون تداخل انجام شوند."
    )

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_lock_scenario(scenario_id: int):
    scenarios = {1: lock_scenario1, 2: lock_scenario2, 3: lock_scenario3}

    if scenario_id not in scenarios:
        raise ValueError(f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3")

    return scenarios[scenario_id]()
