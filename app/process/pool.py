import multiprocessing
import time
import random
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


def function_square(data):
    time.sleep(0.15)
    return data * data


def analyze_dataset(name, numbers):
    time.sleep(1)
    return {
        "name":    name,
        "count":   len(numbers),
        "sum":     sum(numbers),
        "average": sum(numbers) / len(numbers),
        "max":     max(numbers),
        "min":     min(numbers),
    }


def sum_of_factorials(task_name, n):
    time.sleep(3)
    total = 0
    value = 1
    for i in range(1, n + 1):
        value *= i
        total += value
    return f"{task_name}: Sum of factorials up to {n}! has {len(str(total))} digits"


# سناریو 1: Pool با متد map
def pool_scenario1():
    output      = []
    explanation = []

    output.append("PROCESS POOL — map()")
    output.append("=" * 70)

    inputs = list(range(0, 100))

    output.append(f"Total inputs   : {len(inputs)}")
    output.append(f"Pool processes : 4")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    pool = multiprocessing.Pool(processes=4)
    pool_outputs = pool.map(function_square, inputs)
    pool.close()
    pool.join()

    exec_time = time.time() - start_time

    output.append(f"First 10 results  : {pool_outputs[:10]}")
    output.append(f"Last 10 results   : {pool_outputs[-10:]}")
    output.append("")
    output.append("=" * 70)
    output.append(f"Total results   : {len(pool_outputs)}")
    output.append(f"Execution time  : {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 1: Pool با متد map")
    explanation.append("")
    explanation.append("Pool مکانیزمی است که اجرای یک تابع روی چندین ورودی را")
    explanation.append("موازی می‌کند و داده‌ها را بین فرایندهای Pool توزیع می‌کند.")
    explanation.append("این نوع موازی‌سازی Data Parallelism نام دارد.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- multiprocessing.Pool(processes=4) یک استخر 4 فرایندی می‌سازد")
    explanation.append("2- pool.map(func, inputs) لیست ورودی را به قطعاتی تقسیم می‌کند")
    explanation.append("   و هر قطعه را به یکی از 4 فرایند می‌سپارد")
    explanation.append("3- نتیجه دقیقاً به ترتیب ورودی برگردانده می‌شود")
    explanation.append("   (برخلاف چیزی که ممکن است تصور شود، ترتیب خروجی به‌هم نمی‌ریزد)")
    explanation.append("4- pool.close() اجازه نمی‌دهد کار جدیدی به Pool اضافه شود")
    explanation.append("5- pool.join() منتظر می‌ماند تا همه فرایندهای Pool تمام شوند")
    explanation.append("")
    explanation.append("مقایسه با map معمولی پایتون:")
    explanation.append("pool.map(f, inputs) از نظر نتیجه دقیقاً معادل map(f, inputs) است،")
    explanation.append("با این تفاوت که اینجا واقعاً روی چند هسته CPU موازی اجرا می‌شود.")
    explanation.append("")
    explanation.append("map() بلاک‌کننده (Blocking) است: برنامه اصلی تا پایان کامل")
    explanation.append("همه محاسبات منتظر می‌ماند و چیز دیگری نمی‌تواند انجام دهد.")
    explanation.append("اگر تعداد processes کمتر از تعداد ورودی‌ها باشد،")
    explanation.append("Pool به‌طور خودکار کارها را در قالب دسته (chunk) بین آن‌ها تقسیم می‌کند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 2: Pool با متد map_async
def pool_scenario2():
    output      = []
    explanation = []

    output.append("PROCESS POOL — map_async()")
    output.append("=" * 70)

    inputs = list(range(1, 100))

    output.append(f"Total inputs   : {len(inputs)}")
    output.append(f"Pool processes : 4")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    pool = multiprocessing.Pool(processes=4)

    output.append(f"{timestamp()}    Main process     Calling map_async()")
    output.append(f"{timestamp()}    Pool processes   Start... (non-blocking, returns immediately)")
    
    async_result = pool.map_async(function_square, inputs)

    output.append(f"{timestamp()}    Main process     Continues doing other work...")
    for i in range(3):
        time.sleep(0.5)
        output.append(f"{timestamp()}    Main process     Working #{i+1} (still not blocked)")

    output.append(f"{timestamp()}    Main process     Waiting... (calling .get() to fetch results)")
    results = async_result.get()   # اینجا فرایند اصلی منتظر می‌ماند تا نتایج آماده شوند
    output.append(f"{timestamp()}    Pool processes   End!")
    output.append(f"{timestamp()}    Main process     Continue...")
    
    pool.close()
    pool.join()

    exec_time = time.time() - start_time

    output.append("")
    output.append(f"First 10 results  : {results[:10]}")
    output.append(f"Last 10 results   : {results[-10:]}")
    output.append("")
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 2: Pool با متد map_async")
    explanation.append("")
    explanation.append("map_async نسخه ناهمگام map است.")
    explanation.append("")
    explanation.append("map()       : برنامه اصلی را مسدود می‌کند تا نتیجه آماده شود")
    explanation.append("map_async() : بلافاصله یک شیء AsyncResult برمی‌گرداند")
    explanation.append("              و برنامه اصلی می‌تواند کارهای دیگری انجام دهد")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- async_result = pool.map_async(func, inputs)")
    explanation.append("   این خط بلافاصله برمی‌گردد؛ محاسبات در پس‌زمینه ادامه دارد")
    explanation.append("2- برنامه اصلی می‌تواند در همین حین کار دیگری انجام دهد")
    explanation.append("3- async_result.get() نتیجه نهایی را می‌خواند")
    explanation.append("   اگر محاسبات هنوز تمام نشده باشد، اینجا منتظر می‌ماند")
    explanation.append("")
    explanation.append("اگر تابعی به عنوان callback به map_async داده شود:")
    explanation.append("pool.map_async(func, inputs, callback=my_callback)")
    explanation.append("آن callback به‌محض آماده شدن نتیجه، در فرایند اصلی فراخوانی می‌شود")
    explanation.append("و نباید کار طولانی انجام دهد؛")
    explanation.append("در غیر این صورت، نخ داخلی مدیریت نتایج Pool مسدود می‌شود.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 3: Pool با متد apply
def pool_scenario3():
    output      = []
    explanation = []

    output.append("PROCESS POOL — apply()")
    output.append("=" * 70)

    datasets = [
        ("Sales-Q1",  [120, 340, 210, 560, 430]),
        ("Sales-Q2",  [200, 150, 480, 390, 610]),
        ("Sales-Q3",  [310, 275, 500, 190, 440]),
    ]

    output.append(f"Total datasets : {len(datasets)}")
    output.append(f"Pool processes : 4")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    pool = multiprocessing.Pool(processes=1)

    results = []
    for name, numbers in datasets:
        output.append(f"{timestamp()}    Calling apply() for {name}... (blocking until this result is ready)")
        result = pool.apply(analyze_dataset, args=(name, numbers))
        results.append(result)
        output.append(f"{timestamp()}    Result: {result}")

    pool.close()
    pool.join()

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append("Summary of all datasets:")
    for r in results:
        output.append(f"  {r['name']:<10s} | count={r['count']} | avg={r['average']:.1f} | max={r['max']} | min={r['min']}")
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 3: Pool با متد apply")
    explanation.append("")
    explanation.append("apply برخلاف map، یک تابع را فقط یک‌بار با یک مجموعه آرگومان مشخص اجرا می‌کند.")
    explanation.append("")
    explanation.append("تفاوت اصلی با map:")
    explanation.append("map(func, inputs)   : همان تابع را روی هر عضو یک لیست اجرا می‌کند")
    explanation.append("apply(func, args)   : تابع را فقط یک‌بار، با یک دسته آرگومان خاص اجرا می‌کند")
    explanation.append("                      شبیه فراخوانی معمولی تابع، با این تفاوت که")
    explanation.append("                      در یک فرایند جداگانه از Pool اجرا می‌شود")
    explanation.append("")
    explanation.append("چرا در این سناریو از حلقه با apply استفاده شد نه از map؟")
    explanation.append("چون هر دیتاست آرگومان‌های متفاوتی دارد (نام و لیست اعداد جداگانه)؛")
    explanation.append("apply برای فراخوانی‌های مجزا و مستقل مناسب‌تر است.")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- pool.apply(func, args=(...)) یک فرایند از Pool را می‌گیرد")
    explanation.append("2- تابع را با آرگومان‌های داده‌شده اجرا می‌کند")
    explanation.append("3- تا آماده شدن نتیجه، فرایند اصلی مسدود (Blocking) می‌ماند")
    explanation.append("")
    explanation.append("چون apply() بلاک‌کننده است، در این حلقه سه بار پشت سر هم صدا زده می‌شود؛")
    explanation.append("یعنی این سه محاسبه عملاً به‌صورت ترتیبی اجرا می‌شوند نه کاملاً موازی؛")
    explanation.append("برای موازی‌سازی واقعی چند فراخوانی apply، باید از apply_async استفاده کرد (سناریو 4).")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# سناریو 4: Pool با متد apply_async
def pool_scenario4():
    output      = []
    explanation = []

    output.append("PROCESS POOL — apply_async()")
    output.append("=" * 70)

    tasks = [
        ("Task-A", 500),
        ("Task-B", 700),
        ("Task-C", 600),
        ("Task-D", 800),
    ]

    output.append(f"Total tasks    : {len(tasks)}")
    output.append(f"Pool processes : 3")
    output.append("=" * 70)
    output.append("")

    start_time = time.time()

    pool = multiprocessing.Pool(processes=3)

    async_results = []
    for name, n in tasks:
        output.append(f"{timestamp()}    Submitting {name} with apply_async()... (non-blocking, returns immediately)")
        ar = pool.apply_async(sum_of_factorials, args=(name, n))
        async_results.append(ar)

    output.append(f"{timestamp()}    All {len(tasks)} tasks submitted. Main process is free to do other work.")
    output.append(f"{timestamp()}    Main process continues doing other work...")
    for i in range(3):
        time.sleep(0.5)
        output.append(f"{timestamp()}    Main process working #{i+1} (still not blocked)")

    output.append(f"{timestamp()}    Main process waiting...(collecting results with .get() for each task...)")
    for ar in async_results:
        result = ar.get()   # منتظر می‌ماند تا نتیجه همین Task آماده شود
        output.append(f"{timestamp()}    {result}")

    pool.close()
    pool.join()

    exec_time = time.time() - start_time

    output.append("")
    output.append("=" * 70)
    output.append(f"Execution time: {exec_time:.3f} seconds")
    output.append("=" * 70)

    explanation.append("سناریو 4: Pool با متد apply_async")
    explanation.append("")
    explanation.append("apply_async نسخه ناهمزمان apply است.")
    explanation.append("")
    explanation.append("تفاوت اصلی با apply:")
    explanation.append("apply()       : فرایند اصلی را تا آماده شدن نتیجه مسدود می‌کند")
    explanation.append("apply_async() : بلافاصله یک AsyncResult برمی‌گرداند")
    explanation.append("                و فراخوانی بعدی بدون انتظار برای نتیجه قبلی انجام می‌شود")
    explanation.append("")
    explanation.append("نحوه عملکرد:")
    explanation.append("1- هر ar = pool.apply_async(func, args) بلافاصله برمی‌گردد")
    explanation.append("2- همه tasks پشت سر هم و بدون انتظار submit می‌شوند")
    explanation.append("3- تمام taskها همزمان روی 4 فرایند Pool در حال اجرا هستند")
    explanation.append("4- ar.get() برای هر task به‌ترتیب صدا زده می‌شود تا نتیجه گرفته شود")
    explanation.append("")
    explanation.append("این سناریو سریع‌تر از سناریو 3 (apply) است.")
    explanation.append("در سناریو 3، هر apply() منتظر می‌ماند تا نتیجه‌اش آماده شود")
    explanation.append("قبل از این‌که فراخوانی بعدی شروع شود -> عملاً ترتیبی.")
    explanation.append("در این سناریو، همه taskها بلافاصله و بدون انتظار ارسال می‌شوند")
    explanation.append("و همزمان در پس‌زمینه روی فرایندهای مختلف اجرا می‌شوند -> واقعاً موازی.")
    explanation.append("")
    explanation.append("جدول مقایسه چهار متد Pool:")
    explanation.append("  map()         : چند ورودی، همان تابع، بلاک‌کننده")
    explanation.append("  map_async()   : چند ورودی، همان تابع، ناهمزمان")
    explanation.append("  apply()       : یک فراخوانی با آرگومان دلخواه، بلاک‌کننده")
    explanation.append("  apply_async() : یک فراخوانی با آرگومان دلخواه، ناهمزمان")
    explanation.append("")
    explanation.append("تفاوت map و apply در نوع ورودی است (لیست در برابر آرگومان تکی)")
    explanation.append("و تفاوت async و غیر async در بلاک شدن یا نشدن فرایند اصلی است.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# *************************************************************
def run_pool_scenario(scenario_id: int):
    scenarios = {
        1: pool_scenario1,
        2: pool_scenario2,
        3: pool_scenario3,
        4: pool_scenario4,
    }

    if scenario_id not in scenarios:
        raise ValueError(
            f"سناریوی {scenario_id} وجود ندارد. سناریوهای موجود: 1, 2, 3, 4"
        )

    return scenarios[scenario_id]()