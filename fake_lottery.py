import requests
import time
import json
import random
import pymysql.cursors


def execute(sql, params=None, db='video_lottery', is_fetchone=False):
    # Connect to the database
    connection = pymysql.connect(host='192.168.0.224',
                                 port=3306,
                                 user='root',
                                 password='111111',
                                 db=db,
                                 autocommit=True,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            if is_fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()
    except:
        connection.rollback()
    finally:
        connection.close()


if __name__ == '__main__':
    while True:
        result = execute('SELECT id FROM lot_order_detail WHERE detail_status=0 and station_number is NOT NULL')
        if result:
            num = 0
            detail_id_list = []
            for x in result:
                detail_id_list.append(x['id'])
            detail_id_list.sort()
            detail_id = detail_id_list[0]
            detail_id_max = detail_id_list[-1]

            amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 15, 20, 25,
                      30, 50, 60, 80, 90, 100, 120, 150, 180, 200, 300, 350, 500, 800,
                      1000, 1200, 1500, 3000, 5000]
            while detail_id < detail_id_max + 1:
                if num == 0:
                    time.sleep(10)
                ticket_no = int(str(detail_id) + str(random.randint(11111, 99999)))
                index = random.randint(0, len(amount) - 1)
                am = amount[index]
                if am == 0:
                    bouns_status = 0
                else:
                    bouns_status = 1
                response = requests.get(
                    url='http://111.200.217.42:8386/video-lottery-base_api/notify/bonus?amount={0}&deviceId=11&ticketNo={1}&detailId={2}&bonusStatus={3}'.format(
                        am, ticket_no, detail_id, bouns_status))
                execute("update lot_order_detail set route='http://www.taopic.com/uploads/allimg/140320/235013-14032020515270.jpg',is_upload=1 where id=%s",params=(detail_id))
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
                print('detail_id:' + str(detail_id), '   ticket_no:' + str(ticket_no), '   amount:' + str(am))
                print(json.loads(response.content))
                print('----------------------华丽的分割线-------------------------')
                time.sleep(3)
                ticket_no += 1
                detail_id += 1
                num += 1
        else:
            print('没有订单!!')
        time.sleep(30)
