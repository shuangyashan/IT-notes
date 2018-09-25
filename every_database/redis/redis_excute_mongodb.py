import json, redis, pymongo

def main():
    # ָ��Redis���ݿ���Ϣ
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    # ָ��MongoDB���ݿ���Ϣ
    mongocli = pymongo.MongoClient(host='localhost', port=27017)
    # �������ݿ���
    db = mongocli['sina']
    # ��������
    sheet = db['sina_items']
    offset = 0
    while True:
        # FIFOģʽΪ blpop��LIFOģʽΪ brpop����ȡ��ֵ
        source, data = rediscli.blpop(["sinainfospider_redis:items"])
        item = json.loads(data.decode("utf-8"))
        sheet.insert(item)
        offset += 1
        print(offset)
        try:
            print("Processing: %s " % item)
        except KeyError:
            print("Error procesing: %s" % item)

if __name__ == '__main__':
    main()
