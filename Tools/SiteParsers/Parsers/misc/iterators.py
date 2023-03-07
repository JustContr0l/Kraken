from fake_user_agent import user_agent


def proxy_ua_iterator(proxies: list, one_proxy_count: int = 3):
    while True:
        for proxy in proxies:
            ua = user_agent()
            for _ in range(one_proxy_count):
                yield proxy, ua
