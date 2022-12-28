import re
import requests, traceback

# from . import base
# import basic


class Douyin:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
    )

    def __init__(self, url: str):
        self.url = url

    def run(self):
        return self.getVideoInfo()

    def getVideoInfo(self):
        res = self.s.get("https://api.missuo.me/douyin/?url=" + self.url).json()
        return {
            "作者": res["nickname"],
            "简介": res["desc"],
            "视频链接": res["mp4"],
            "音频链接": res["mp3"],
        }


def get_douyin(url):
    url_list = re.findall(r"http[s]?://v.douyin.com/\S+", url)
    if url_list:
        dy = Douyin(url_list[0])
        try:
            url_judged = dy.run()
        except:
            traceback.print_exc()
            url_judged = "仅支持解析视频，像图文类的就不支持。"

        return url_judged
    else:
        return "请检查你输入的链接是否正确，例如: https://v.douyin.com/6kAoWvc/"


# if __name__ == "__main__":
#     url = "https://v.douyin.com/hDVSKKf/"
#     a = get_douyin(url)
#     print(a)
