
def get_min_max_float_delay(proxies: list, min_diff: int = 13, max_diff: int = 25):
    delay_min = float(f'{float(min_diff / len(proxies)):.2f}')  # Min 15s difference(If proxy count=5, delay = 3.0s)
    delay_max = float(f'{float(max_diff / len(proxies)):.2f}')  # Min 30s difference(If proxy count=5, delay = 6.0s)
    return delay_min, delay_max
