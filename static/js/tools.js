// ============================================
// لیست ابزارها بر اساس روش
// ============================================

const THREAD_TOOLS = [
    { id: "lock", name: "Lock", desc: "همگام‌سازی نخ با یک قفل ساده" },
    { id: "rlock", name: "RLock", desc: "همگام‌سازی نخ با قفل قابل بازگشت" },
    { id: "semaphore", name: "Semaphore", desc: "همگام‌سازی نخ با سمافور" },
    { id: "condition", name: "Condition", desc: "همگام‌سازی نخ با شرط" },
    { id: "event", name: "Event", desc: "همگام‌سازی نخ با رویداد" },
    { id: "barrier", name: "Barrier", desc: "همگام‌سازی نخ با مانع" },
    { id: "queue", name: "Queue", desc: "ارتباط نخ‌ها با صف" }
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