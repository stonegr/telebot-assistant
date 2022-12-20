import time
from ZtjAria2Rpc import Aria2Rpc
import threading

from telebot import TeleBot

from . import base
from tgbot import config


class Aria2_do(Aria2Rpc):
    def __init__(self, uri="http://127.0.0.1:6800/rpc", secret=None):
        # 两种继承方法
        # super(Aria2Rpc,self).__init__(uri, secret)
        Aria2Rpc.__init__(self, uri, secret)

        self.active = {}
        self.waiting = {}
        self.stopped = {}

    def list_methods(self):
        """列出所有可用方法"""
        return self.call("system.listMethods")

    def remove_result(self, gid):
        """移除下载结果,不删除文件"""
        return self.call("aria2.removeDownloadResult", gid)

    def remove_noerror(self, gid):
        try:
            self.remove_result(gid)
        except:
            self.remove(gid)

    def init_data(self):
        _data_tmp = {}
        _downloading_list = self.active
        _waiting_list = self.waiting
        for i in _downloading_list:
            _data_tmp[base.Get_movie_name(i["files"][0]["path"])] = {
                "gid": i["gid"],
                "status": i["status"],
            }
        for i in _waiting_list:
            _data_tmp[base.Get_movie_name(i["files"][0]["path"])] = {
                "gid": i["gid"],
                "status": i["status"],
            }
        return _data_tmp

    def format_downloading(self):
        d = self.active
        if not d:
            return "无任务"

        _d_tmp = ""
        for i in d:
            _d_tmp += "name: {}\nprogress: {}\nsize: {}\nspeed: {}\ncomplete_time: {}\n\n".format(
                base.Get_movie_name(i["files"][0]["path"]),
                base.Get_finish_percentage(i["completedLength"], i["totalLength"]),
                base.Format_size(i["totalLength"]),
                base.Format_speed(i["downloadSpeed"]),
                base.Format_complete_time(
                    i["completedLength"], i["totalLength"], i["downloadSpeed"]
                ),
            )
        return _d_tmp.rstrip("\n\n")

    def format_stoped(self):
        d = self.stopped
        if not d:
            return "无已完成任务"

        _d_tmp = ""
        for i in reversed(d):
            _d_tmp += "name: {}\nprogress: {}\nsize: {}".format(
                base.Get_movie_name(i["files"][0]["path"]),
                base.Get_finish_percentage(i["completedLength"], i["totalLength"]),
                base.Format_size(i["totalLength"]),
            )
            if i.get("errorMessage"):
                _d_tmp += "\nerror: {}\n\n".format(i.get("errorMessage"))
            else:
                _d_tmp += "\n\n"
        return _d_tmp.rstrip("\n\n")

    def format_pause_download(self):
        """
        格式化正在下载的任务用于暂停
        """
        d = self.active
        if not d:
            return "无任务"
        _d_tmp = {}
        for i in d:
            _d_tmp[base.Get_movie_name(i["files"][0]["path"])] = i["gid"]
        return _d_tmp

    def format_download_pause(self):
        d = self.waiting
        if not d:
            return "无任务"
        _d_tmp = {}
        for i in d:
            _d_tmp[base.Get_movie_name(i["files"][0]["path"])] = i["gid"]
        return _d_tmp

    def format_acivate_paused_stop(self, default="无任务"):
        """
        返回正在下载,暂停,已停止
        """
        _all = {}
        _all.update(self.init_data())
        _stoped = self.stopped
        for i in reversed(_stoped):
            _all[base.Get_movie_name(i["files"][0]["path"])] = {
                "gid": i["gid"],
                "status": i["status"],
            }
        if not _all:
            return default
        return _all

    def monitor_active(self, bot: TeleBot):
        """
        检测是否有下载成功的任务
        """
        # 验证是否是第一次
        time.sleep(5)

        while True:
            if not hasattr(self, "now_data"):
                self.now_data = self.format_acivate_paused_stop({})
            else:
                _new_data = self.format_acivate_paused_stop({})
                for k, v in self.now_data.items():
                    if (
                        _new_data.get(k, {}).get("status") == "complete"
                        and v.get("status") == "active"
                    ):
                        for i in config.NOTIFY_USER_ID.split(","):
                            bot.send_message(i, "{} completed!".format(k))
                for k, v in _new_data.items():
                    if _new_data.get(k, {}).get("status") == "active" and (
                        k not in self.now_data
                    ):
                        for i in config.NOTIFY_USER_ID.split(","):
                            bot.send_message(i, "{} started!".format(k))
                self.now_data = _new_data
            time.sleep(2)

    def flush_aria2_status(self):
        while True:
            try:
                self.active = self.tell_active()
                self.waiting = self.tell_waiting(0, config.ARIA2_DEPTH)
                self.stopped = self.tell_stopped(0, config.ARIA2_DEPTH)
                time.sleep(1)
            except Exception as e:
                pass


_tgbot_tmp = Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)


def Moniter_active(bot: TeleBot):

    t = threading.Thread(
        target=_tgbot_tmp.monitor_active,
        args=(bot,),
    )
    t.start()


def Flush_data():
    """
    刷新数据
    """
    t = threading.Thread(
        target=_tgbot_tmp.flush_aria2_status,
    )
    t.start()


# aria2 = Aria2_do("http://127.0.0.1:6800/rpc", "123-=shi")
# aria2.monitor_active()
