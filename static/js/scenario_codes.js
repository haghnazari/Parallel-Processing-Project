// ============================================
// کدهای پایتون هر سناریو (فایل جداگانه)
// ============================================

const SCENARIO_CODES = {
    // ========== Lock ==========
    lock: {
        1:`def lock_scenario1():
    counter = 0
    output = []

    class CounterThread(Thread):
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name

        def run(self):
            nonlocal counter
            temp = counter
            output.append(f"---> {self.name} read counter = {temp}")
            time.sleep(0.0001)
            counter = temp + 1
            output.append(f"---> {self.name} write counter = {counter}")

    threads = []
    for i in range(10):
        t = CounterThread(f"Thread#{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()`,
        
        2: `def lock_scenario2():
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
        t.join()`,

        
        3: `def lock_scenario3():
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
            output.append(f"START    ----> {self.name}: type={self.transaction_type}, amount={self.amount}, balance_before={old_balance}")
            time.sleep(0.01)
            if self.transaction_type == "Deposit":
                balance += self.amount
                output.append(f"DEPOSIT ----> {self.name}: +{self.amount} | new_balance={balance}")
                transaction_count += 1
                
            elif self.transaction_type == "Withdraw":
                if balance >= self.amount:
                    balance -= self.amount
                    output.append(f"WITHDRAW ----> {self.name}: -{self.amount} | new_balance={balance}")
                    transaction_count += 1
                else:
                    output.append(f"REJECTED ----> {self.name}: withdraw {self.amount} FAILED! (insufficient balance: {balance})")
                    failed_transactions += 1       
            time.sleep(0.005)
            output.append(f"END      ----> {self.name}: Final_balance={balance}\n")

            bank_lock.release()

    transactions = []
    for i in range(10):
        amount = randint(300, 800)
        ta = ["Deposit", "Withdraw"][randint(0,1)]
        t = BankTransaction(f"{ta}#{i+1}", amount, ta)
        transactions.append(t)
    

    output.append(f"🏦 STARTING BANKING OPERATION | Initial balance: {balance}")
    output.append(f"📊 Total transactions: 10")
    output.append("")
    
    for t in transactions:
        t.start()
    
    for t in transactions:
        t.join()`
    },

    // ========== RLock ==========
    rlock: {
        1: `# کد سناریو 1 RLock - به زودی اضافه می‌شود`,
        2: `# کد سناریو 2 RLock - به زودی اضافه می‌شود`,
        3: `# کد سناریو 3 RLock - به زودی اضافه می‌شود`
    }
};