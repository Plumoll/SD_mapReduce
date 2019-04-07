import pika, json, yaml
from cos_backend import COSBackend


with open('ibm_cloud_config', 'r') as config_file:
    res = yaml.safe_load(config_file)
url = res["rabbitmq"]["url"]

odb = COSBackend(res['ibm_cos'])
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='map')

def callback(ch, method, properties, body):
    #received_data = json.loads(body)
    global odb
    fileFromServer = odb.get_object("magisd", body.decode('UTF-8')).decode('UTF-8')
    odb.delete_object("magisd", body.decode('UTF-8'))
    received_data = json.loads(fileFromServer)
    print(received_data["re"])
    print(received_data)

channel.basic_consume('map', callback, True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
connection.close()