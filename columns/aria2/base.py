def Get_movie_name(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def Get_finish_percentage(finish: str, total: str) -> str:
    if total == "0":
        return "{:.2f}%".format(0.0)
    return "{:.2f}%".format(100 * (int(finish) / int(total)))


def Format_speed(s: str) -> str:
    _MB, _KB = int(s) / 1024 / 1024, int(s) / 1024
    if _KB < 1024:
        return "{:.2f} KB/s".format(_KB)
    else:
        return "{:.2f} MB/s".format(_MB)


def Format_size(s: str) -> str:
    _GB, _MB, _KB = int(s) / 1024 / 1024 / 1024, int(s) / 1024 / 1024, int(s) / 1024
    if _KB > 1024:
        if _MB > 1024:
            return "{:.2f} GB".format(_GB)
        else:
            return "{:.2f} MB".format(_MB)
    else:
        return "{:.2f} KB".format(_KB)


def Format_complete_time(complete: str, total: str, speed: str):
    if speed == "0":
        return "速度为0"
    seconds = (int(total) - int(complete)) / int(speed)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h >= 24:
        return "大于一天"
    else:
        if h != 0:
            return "{:.0f}时{:.0f}分{:.0f}秒".format(h, m, s)
        else:
            if m != 0:
                return "{:.0f}分{:.0f}秒".format(m, s)
            else:
                return "{:.0f}秒".format(s)
