import datetime
import os
import requests

members = {
    "huangjunqing": "XiaoZhuo_Ops",
    # "yangchh": "yangchh1998",
    "ivan": "zjrenivan",
    "SimhaZF": "ZSimha",
    "rookie0080": "rookie0080"
}

PUSH_KEY = os.getenv("PUSH_KEY")


def check(days_before):
    checklist = list(members.keys())
    today = datetime.date.today()
    day = today - datetime.timedelta(days=days_before)

    path_day = os.path.join(os.getcwd(), "homework", day.strftime('%Y%m'), day.strftime('%m%d'))

    for _, _, files in os.walk(path_day):
        for file in files:
            for member in checklist:
                if member in file:
                    checklist.remove(member)
    return [members[i] for i in checklist]


def notify(_title, _message=None):
    if not PUSH_KEY:
        print("未配置PUSH_KEY！")
        return

    if not _message:
        _message = _title

    print(_title)
    # print(_message)

    _response = requests.post(f"https://sc.ftqq.com/{PUSH_KEY}.send", {"text": _title, "desp": _message})

    if _response.status_code == 200:
        print(f"发送通知状态：{_response.content.decode('utf-8')}")
    else:
        print(f"发送通知失败：{_response.status_code}")


if __name__ == "__main__":
    l1 = check(1)
    l2 = check(2)
    ll = []
    for m in l1:
        if m in l2:
            ll.append(m)
    if not ll:
        notify("今日平安夜")
        print("今日平安夜")
    else:
        atlist = ""
        for lucky in ll:
            atlist = atlist + "@" + lucky + " "
        ret = "群友 %s连续两天未完成作业，请发随机红包 %s 元共 %s 份!" % (atlist, 2 * len(members), len(members) - 1)
        notify("有红包", ret)
        print(ret)
