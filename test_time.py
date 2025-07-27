import requests
import time

url = "http://127.0.0.1:8000/"  # ← غيّر لرابط الصفحة
n = 10

real_times = []
cpu_times = []
full_cpu_times = []

for i in range(n):
    start = time.perf_counter()
    response = requests.get(url)
    end = time.perf_counter()

    duration = end - start
    real_times.append(duration)

    cpu_time = response.headers.get("X-CPU-Time")
    full_cpu = response.headers.get("X-CPU-Full-Time")

    if cpu_time:
        cpu_times.append(float(cpu_time))

    if full_cpu:
        full_cpu_times.append(float(full_cpu))

    print(f"Request {i+1}:")
    print(f"🕒 Real Time = {duration:.4f} seconds")
    print(f"⚙️ View CPU Time = {cpu_time} seconds")
    print(f"🧠 Full CPU Time = {full_cpu} seconds")

# حساب المتوسطات
real_avg = sum(real_times) / n
cpu_avg = sum(cpu_times) / len(cpu_times) if cpu_times else 0
full_cpu_avg = sum(full_cpu_times) / len(full_cpu_times) if full_cpu_times else 0

print("\n🔁 Averages over", n, "requests:")
print(f"🕒 Real Time Avg = {real_avg:.4f} seconds")
print(f"⚙️ View CPU Time Avg = {cpu_avg:.6f} seconds")
print(f"🧠 Full CPU Time Avg = {full_cpu_avg:.6f} seconds")
