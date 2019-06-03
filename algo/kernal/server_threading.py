# -*- coding:utf-8 -*-
import threading
import json
from algo.common.logger import log


class ServerThreading(threading.Thread):
    """创建连接线程"""
    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def run(self):
        log.info("开启线程...")
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

            # 算法处理逻辑
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
        log.info("任务结束...")

        pass

    def __del__(self):

        pass
