import json


def Format_second(t: int):
    """
    将秒格式化为分钟格式
    """
    return "{}分{}秒".format(t // 60, t % 60)


def Format_json(d: dict) -> str:
    """
    格式化json,缩进为4
    """
    return str(
        json.dumps(
            d, sort_keys=False, ensure_ascii=False, indent=4, separators=(",", ": ")
        )
    )
