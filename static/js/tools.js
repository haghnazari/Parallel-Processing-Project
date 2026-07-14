const THREAD_TOOLS = [
    { id: "defining", name: "Defining a thread", desc: "تعریف و اجرای یک نخ ساده" },
    { id: "determining", name: "Determining the current thread", desc: "تشخیص و نمایش نخ جاری" },
    { id: "subclass", name: "Defining a thread subclass", desc: "تعریف نخ با استفاده از زیرکلاس" },
    { id: "lock", name: "Thread synchronization with a lock", desc: "همگام‌سازی نخ با قفل ساده" },
    { id: "rlock", name: "Thread synchronization with RLock", desc: "همگام‌سازی نخ با قفل قابل بازگشت" },
    { id: "semaphore", name: "Thread synchronization with semaphores", desc: "همگام‌سازی نخ با سمافور" },
    { id: "condition", name: "Thread synchronization with a condition", desc: "همگام‌سازی نخ با شرط" },
    { id: "event", name: "Thread synchronization with an event", desc: "همگام‌سازی نخ با رویداد" },
    { id: "barrier", name: "Thread synchronization with a barrier", desc: "همگام‌سازی نخ با مانع" },
    { id: "queue", name: "Thread communication using a queue", desc: "ارتباط نخ‌ها با صف" }
];

const PROCESS_TOOLS = [
    { id: "spawning", name: "Spawning a process", desc: "ایجاد و اجرای یک فرایند جدید" },
    { id: "naming", name: "Naming a process", desc: "نام‌گذاری فرایندها" },
    { id: "background", name: "Running processes in the background", desc: "اجرای فرایندها در پس‌زمینه" },
    { id: "killing", name: "Killing a process", desc: "متوقف کردن (کشتن) یک فرایند" },
    { id: "subclass", name: "Defining processes in a subclass", desc: "تعریف فرایند در زیرکلاس" },
    { id: "queue", name: "Using a queue to exchange data", desc: "استفاده از صف برای تبادل داده" },
    { id: "pipes", name: "Using pipes to exchange objects", desc: "استفاده از پایپ برای تبادل اشیاء" },
    { id: "sync", name: "Synchronizing processes", desc: "همگام‌سازی فرایندها" },
    { id: "pool", name: "Using a process pool", desc: "استفاده از استخر فرایند" }
];