import datetime


def execute():
    # 現在の日付を表示
    current_date = datetime.datetime.now()
    print("p001")
    print("現在の日付:", current_date.strftime("%Y年%m月%d日"))
    print("現在の時刻:", current_date.strftime("%H:%M:%S"))
