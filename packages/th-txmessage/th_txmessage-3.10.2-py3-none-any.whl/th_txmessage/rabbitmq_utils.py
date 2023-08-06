import pika
class rabbitmq_helper():
    message_dict:dict

    def __init__(self,user,pwd,host) -> None:
        self.message_dict = {};
        credentials = pika.PlainCredentials(user, pwd)  # mq用户名和密码
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = host,port = 5672,virtual_host = '/',credentials = credentials))
        self.channel = connection.channel()

    def send_message(self,body,quenuName):
        result = self.channel.queue_declare(queue = 'python-test')
        self.channel.basic_publish(exchange = '',routing_key = quenuName,body = body)
    
    def receive_message(self,name):
        def wrap(func):
            self.message_dict[name] = func;
        return wrap;
    def callback(self,ch, method, properties, body):
        flag = False;
        try:
            flag = self.message_dict[method.routing_key](body.decode(encoding="utf-8"));
        except Exception as e:
            print(e);
        if flag:
            ch.basic_ack(delivery_tag = method.delivery_tag)

    def listen(self):
        for i in self.message_dict.keys():
            self.channel.basic_consume(i,self.callback);
        self.channel.start_consuming()