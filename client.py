import socket
from time import time


def splt(keys, a, i):
    if a[i].split(' ')[0] not in keys:
        keys.append(a[i].split(' ')[0])
    else:
        pass


def tstamp():
    return int(time())


class Client():

    def __init__(self, host, port, timeout=None):
        self.timeout = timeout
        self.host = host
        self.port = port
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        self.err_msg = 'error\nwrong command\n\n'

    def _read(self):
        data = ''
        while not data[len(data) - 2:] == '\n\n':
            try:
                resp = self.sock.recv(1024)
                data += resp.decode("utf-8")
                return data
            except socket.error:
                ClientError('error send data', socket.error)



    def put(self, key, val, timestamp=tstamp()):
        s = '{} {} {} {}{}'.format('put', str(key), str(val), str(timestamp), '\n')
        s = s.encode()
        self.sock.sendall(s)
        self._read()

    def get(self, key):
        s = '{} {}{}'.format("get", str(key), '\n')
        s = s.encode()
        self.sock.sendall(s)
        resp = self._read()

        if len(resp) < 3:
            return {}
        else:
            data = resp.split('\n')
            a = []
            keys = []
            for i in data:
                if len(i) > 3:
                    a.append(i)
            """preparing this: b'put load 301 3\ntest 0.5 1\n'
                      to this: {'load': [(3, 301.0)], 'test': [(1, 0.5), (2, 0.4)]
            """

            for i in range(len(a)):
                splt(keys, a, i)
            result = {}
            for i in range(len(keys)):
                result.update({keys[i]: []})
                for k in range(len(a)):
                        if a[k].split(' ')[0] == keys[i]:
                            result[str(keys[i])].append(((int(a[k].split(' ')[2])), (float(a[k].split(' ')[1]))))
        return result


class ClientError(Exception):
    pass


#def _main():
#    client = Client(host='127.0.0.1', port='9091')

#if __name__ == "__main__":
#    _main()
