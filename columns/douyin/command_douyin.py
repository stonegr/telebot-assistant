import re
import requests, traceback

from . import base
import basic


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
        res = self.s.get(self.url).url
        ids = res.split("video/")[1].split("?")[0]
        self.ids = ids
        return self.getVideoInfo()

    def getVideoInfo(self):
        res = self.s.get(
            "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + self.ids
        ).json()
        return {
            "作者": res["item_list"][0]["author"]["nickname"],
            "视频时长": base.Format_douyin_videotime(
                res["item_list"][0]["video"]["duration"]
            ),
            "音频时长": basic.Format_second(res["item_list"][0]["music"]["duration"]),
            "分辨率": str(res["item_list"][0]["video"]["height"])
            + " x "
            + str(res["item_list"][0]["video"]["width"]),
            "视频链接": res["item_list"][0]["video"]["play_addr"]["url_list"][0]
            .replace("playwm", "play")
            .replace("720p", "9999"),
            "音频链接": res["item_list"][0]["music"]["play_url"]["uri"],
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
        return "请检查你输入的链接是否正确，例如：https://v.douyin.com/6kAoWvc/"


# if __name__ == "__main__":
#     url = "https://v.douyin.com/hDVSKKf/"
#     a = get_douyin(url)
#     print(a)
