import threading
import time
import statistics
from unittest.mock import patch
import auth_system


response_times = []
lock = threading.Lock()


def simulate_login(username, password):
    start_time = time.time()
    result = auth_system.login(username, password)
    end_time = time.time()

    response_time = end_time - start_time

    with lock:
        response_times.append((response_time, result))


def run_performance_test():
    auth_system.user_db.clear()
    auth_system.user_profiles.clear()

    for i in range(100):
        username = f"user{i}"
        password = "Strong123!"
        auth_system.user_db[username] = password
        auth_system.user_profiles[username] = {
            "name": username,
            "email": f"{username}@example.com",
            "last_login": None
        }

    threads = []

    for i in range(100):
        t = threading.Thread(target=simulate_login, args=(f"user{i}", "Strong123!"))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    times_only = [item[0] for item in response_times]

    print(f"Total login attempts: {len(times_only)}")
    print(f"Average response time: {statistics.mean(times_only):.4f} seconds")
    print(f"Minimum response time: {min(times_only):.4f} seconds")
    print(f"Maximum response time: {max(times_only):.4f} seconds")


if __name__ == "__main__":
    run_performance_test()