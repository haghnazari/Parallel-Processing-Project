import multiprocessing


def create_items(pipe):
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    output_pipe.close()


def multiply_items(pipe_1, pipe_2):
    close, input_pipe = pipe_1
    close.close()
    output_pipe, _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()
            output_pipe.send(item * item)
    except EOFError:
        output_pipe.close()


# سناریو 1: تبادل اشیاء بین دو فرایند با Pipe
def pipes_scenario1():
    output      = []
    explanation = []

    output.append("EXCHANGING OBJECTS WITH PIPE")
    output.append("=" * 70)

    pipe_1 = multiprocessing.Pipe(True)
    process_pipe_1 = multiprocessing.Process(target=create_items, args=(pipe_1,))
    process_pipe_1.start()

    pipe_2 = multiprocessing.Pipe(True)
    process_pipe_2 = multiprocessing.Process(target=multiply_items, args=(pipe_1, pipe_2))
    process_pipe_2.start()

    # بستن سرهای استفاده‌نشده در فرایند اصلی
    # این کار برای دریافت درست EOFError در فرایند دوم ضروری است
    pipe_1[0].close()
    pipe_2[0].close()

    results = []
    try:
        while True:
            results.append(pipe_2[1].recv())
    except EOFError:
        output.append("End (EOFError received — pipe closed by sender)")

    process_pipe_1.join()
    process_pipe_2.join()

    output.append("")
    output.append(f"Results (squares of 0-9): {results}")
    output.append("=" * 70)

    explanation.append("سناریو 1: تبادل اشیاء بین دو فرایند با Pipe")
    explanation.append("")
    explanation.append("دو Pipe و دو فرایند در این سناریو ساخته می‌شوند:")
    explanation.append("pipe_1 : بین فرایند اصلی/create_items و multiply_items")
    explanation.append("pipe_2 : بین multiply_items و فرایند اصلی")
    explanation.append("")
    explanation.append("نحوه عملکرد create_items:")
    explanation.append("1- output_pipe, _ = pipe   -> فقط سر ارسال (pipe_1[0]) استفاده می‌شود")
    explanation.append("2- برای هر عدد 0 تا 9، output_pipe.send(item) صدا زده می‌شود")
    explanation.append("3- بعد از پایان، output_pipe.close() سر ارسال را می‌بندد")
    explanation.append("")
    explanation.append("نحوه عملکرد multiply_items:")
    explanation.append("1- close, input_pipe = pipe_1")
    explanation.append("   close      = pipe_1[0]  (سر ارسال؛ در این فرایند لازم نیست)")
    explanation.append("   input_pipe = pipe_1[1]  (سر دریافت؛ همینجا استفاده می‌شود)")
    explanation.append("2- close.close()  سر ارسال pipe_1 در این فرایند بسته می‌شود")
    explanation.append("   (چون این فرایند فقط باید دریافت کند، نه ارسال)")
    explanation.append("3- output_pipe, _ = pipe_2  -> سر ارسال pipe_2 برای فرستادن نتیجه")
    explanation.append("4- در یک حلقه بی‌پایان: item = input_pipe.recv()")
    explanation.append("   سپس output_pipe.send(item * item)")
    explanation.append("5- وقتی create_items همه اعداد را فرستاد و pipe را بست،")
    explanation.append("   فراخوانی بعدی recv() یک EOFError پرتاب می‌کند")
    explanation.append("   و حلقه با بستن output_pipe پایان می‌یابد")
    explanation.append("")
    explanation.append("نحوه عملکرد فرایند اصلی:")
    explanation.append("1- pipe_1[0].close()  سر ارسال pipe_1 در فرایند اصلی بسته می‌شود")
    explanation.append("   (فرایند اصلی به این سر نیازی ندارد؛ فقط create_items از آن استفاده می‌کند)")
    explanation.append("2- pipe_2[0].close()  سر ارسال pipe_2 در فرایند اصلی بسته می‌شود")
    explanation.append("   (فرایند اصلی فقط باید از pipe_2[1] دریافت کند)")
    explanation.append("3- در حلقه‌ای pipe_2[1].recv() صدا زده می‌شود تا نتایج دریافت شوند")
    explanation.append("4- وقتی multiply_items کارش تمام شد و pipe_2 را بست،")
    explanation.append("   EOFError در فرایند اصلی رخ می‌دهد و حلقه پایان می‌یابد")
    explanation.append("")
    explanation.append("چرا بستن سرهای استفاده‌نشده اهمیت دارد؟")
    explanation.append("برای اینکه EOFError به‌درستی رخ دهد، تمام نسخه‌های باز")
    explanation.append("سر ارسال یک Pipe (در همه فرایندها) باید بسته شوند.")
    explanation.append("هر فرایند یک کپی مستقل از هر دو سر Pipe را نگه می‌دارد؛")
    explanation.append("اگر فرایند اصلی سر ارسال را باز نگه دارد، حتی بعد از بسته شدن")
    explanation.append("آن سر در فرایند فرستنده، سیستم‌عامل هنوز EOF را گزارش نمی‌دهد.")
    explanation.append("")
    explanation.append("تفاوت Pipe با Queue:")
    explanation.append("Pipe فقط برای ارتباط بین دو نقطه (Point-to-Point) طراحی شده است.")
    explanation.append("Queue برای ارتباط بین چند تولیدکننده/مصرف‌کننده مناسب‌تر است.")
    explanation.append("از نظر عملکرد، Pipe سریع‌تر است چون Queue خودش بر پایه Pipe ساخته شده")
    explanation.append("و لایه‌های اضافی (قفل، بافر داخلی) روی آن اضافه می‌کند.")

    return {"output": "\n".join(output), "explanation": "\n".join(explanation)}


# # *************************************************************
def run_pipes_scenario(scenario_id: int):
    scenarios = {
        1: pipes_scenario1,
    }

    if scenario_id not in scenarios:
        raise ValueError(
            f"سناریوی {scenario_id} وجود ندارد. سناریوی موجود: 1"
        )

    return scenarios[scenario_id]()