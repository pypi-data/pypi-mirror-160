import socket
from json import dumps as json_dumps
from sys import exit as sys_exit

'''失效服务列表'''
fail_server_list = []


class Consumer:
    def __init__(self, provider_conf):
        """
        对象初始化
        :param provider_conf: 服务提供着地址及其他配置
        """
        self.server_conf = provider_conf

    def func_call_int(self, send_data):
        """
        服务提供者注册
        :return: None
        """
        connect_provider = None
        try:
            connect_provider = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[eqsmart] [consumer] [Socket创建] [ERROR]: " + str(e))
            sys_exit()

        '''连接服务提供者'''
        try:
            connect_provider.connect((self.server_conf['IP'], self.server_conf['PORT']))
            connect_provider.setblocking(True)  # 设置阻塞模式，等待Provider调用的返回
            print('[eqsmart] [consumer] [连接Provider] [SUCCESS] IP:' + self.server_conf['IP'])
        except socket.gaierror as e:
            print("[eqsmart] [consumer] [连接Provider] [ERROR]: " + str(e))
            sys_exit()

        '''获取到本机IP'''
        send_data['ip'] = socket.gethostbyname(socket.gethostname())

        '''发送信息到Provider'''
        try:
            connect_provider.sendall(bytes(json_dumps(send_data), encoding="utf8"))
            print("[eqsmart] [consumer] [Provider服务调用] [调用信息]:", json_dumps(send_data))
            data = connect_provider.recv(self.server_conf['BUF_SIZE'])
            print('[eqsmart] [consumer] [Provider服务调用] [响应信息]:', str(data, 'UTF-8'))
            res = data
        except socket.error as e:
            print("[eqsmart] [consumer] [Provider服务调用] [ERROR]: " + str(e))
            res = None
            # sys_exit()
        """
        关闭注册连接
        """
        connect_provider.close()
        return res
