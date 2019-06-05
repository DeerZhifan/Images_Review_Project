# -*- coding: utf-8 -*-

from algo.kernal.review import ImagesReview
from algo.common.logger import log
from algo.common.logger import local_config

import socket
import threading
import json
import cv2


def main():
    """程序入口，创建连接，对输入做处理后返回结果"""
    log.info(local_config)
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名称
    host = local_config['server']['host']
    # 设置一个端口
    port = local_config['server']['port']
    # 将套接字与本地主机和端口绑定
    serversocket.bind((host, port))
    # 设置监听最大连接数
    serversocket.listen(local_config['server']['max_listen'])
    # 获取本地服务器的连接信息
    myaddr = serversocket.getsockname()
    log.info("服务已启动...")
    log.info("服务器地址:{}".format(str(myaddr)))
    # 循环等待接受客户端信息
    while True:
        # 获取一个客户端连接
        clientsocket, addr = serversocket.accept()
        log.info("连接地址:{}".format(str(addr)))
        try:
            t = ServerThreading(clientsocket)  # 为每一个请求开启一个处理线程
            t.start()
            pass
        except Exception as identifier:
            print(identifier)
            pass
        pass


def get_result(image_url):
    """
    算法审核并返回结果
    :param image_url: 图片地址
    :return: result: 字典
    """
    log.info("审核开始，image_url:{}".format(image_url))
    engine_review = ImagesReview(key="algo_mysql", image_url=image_url)
    try:
        result = engine_review.review()
    except cv2.error:
        log.error("cv2图片读取错误! img_url:{}".format(image_url))
        log.error("不合格! 图片读取出错")
        result = 0
    dict_result = {"result": result}
    return dict_result


class ServerThreading(threading.Thread):
    """创建连接线程"""
    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def run(self):
        log.info("开启线程......")
        try:
            # 接受数据
            msg = ''
            while True:
                # 读取recvsize个字节
                rec = self._socket.recv(self._recvsize)
                # 解码
                msg += rec.decode(self._encoding)
                # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕，
                # 所以需要自定义协议标志数据接受完毕
                if msg.strip().endswith('over'):
                    msg = msg[:-4]
                    break
            # 解析json格式的数据
            dict_result = json.loads(msg)
            log.info("获取解析后的结果:{}".format(dict_result))

            # 算法逻辑
            dict_res = get_result(dict_result['content'])
            sendmsg = json.dumps(dict_res)
            log.info("算法处理完成，sendmsg:{}".format(sendmsg))

            # 发送数据
            self._socket.send(("{}".format(sendmsg)).encode(self._encoding))
            pass
        except Exception as identifier:
            self._socket.send("500".encode(self._encoding))
            log.error(identifier)
            pass
        finally:
            self._socket.close()
        log.info("任务结束......")

        pass

    def __del__(self):

        pass


if __name__ == "__main__":
    main()
