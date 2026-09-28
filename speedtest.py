import argparse
import sys
import time
import urllib.request

CHUNK = 64 * 1024


def fetch(url, timeout):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Cache-Control": "no-cache",
    })
    size = 0
    start = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        while True:
            chunk = resp.read(CHUNK)
            if not chunk:
                break
            size += len(chunk)
    return size, time.perf_counter() - start


def main():
    parser = argparse.ArgumentParser(description="Замер скорости скачивания")
    parser.add_argument("url", help="адрес файла, например большой картинки")
    parser.add_argument("-n", type=int, default=10, help="количество запросов (по умолчанию 10)")
    parser.add_argument("-t", "--timeout", type=float, default=30, help="таймаут запроса, сек")
    args = parser.parse_args()

    total_bytes = 0
    times = []

    for i in range(1, args.n + 1):
        try:
            size, elapsed = fetch(args.url, args.timeout)
        except Exception as e:
            print(f"#{i}: ошибка - {e}")
            continue
        total_bytes += size
        times.append(elapsed)
        print(f"#{i}: {size / 1024 / 1024:.2f} МБ за {elapsed:.3f} с")

    if not times:
        print("Ни один запрос не прошел")
        sys.exit(1)

    total_time = sum(times)
    avg = total_time / len(times)
    mb = total_bytes / 1024 / 1024
    speed = mb / total_time

    print()
    print(f"Успешных запросов: {len(times)} из {args.n}")
    print(f"Среднее время запроса: {avg:.3f} с")
    print(f"Скачано всего: {mb:.2f} МБ")
    print(f"Скорость: {speed:.2f} МБ/с ({speed * 8:.2f} Мбит/с)")


if __name__ == "__main__":
    main()