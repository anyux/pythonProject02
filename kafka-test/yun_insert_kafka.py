import time

from pykafka import KafkaClient

client = KafkaClient(hosts="192.168.255.171:9092,192.168.255.172:9092,192.168.255.173:9092")
topic = client.topics['data-mytest-block']
producer = topic.get_producer()


def get_info(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()


def insert_kafka(datas, host_name="192.168.255.171", ports="9092"):
    print(datas)
    for  data in datas:
        # print(item)
        data = data+'- - -'+str(time.time())
        tmp = producer.produce(data.encode())
        time.sleep(1)
        print(data)


if __name__ == '__main__':
    data = get_info("gwip.txt")
    insert_kafka(datas=data)
    producer.stop()
    exit(0)
