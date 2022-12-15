import basic


def Format_douyin_videotime(t: int):
    _sec = int(str(t)[:-3])
    return basic.Format_second(_sec)
