import socket
from socketserver import ThreadingMixIn, TCPServer, ThreadingTCPServer, BaseRequestHandler
import threading
import sys

class CustomException(Exception):
    """
    Exception 클래스를 상속한 클래스를 만든다
    """
    def __init__(self, value):
        """
        생성할때 value 값을 입력 받음
        """
        self.value = value

    def __str__(self):
        """
        생성할때 받은 value 값을 확인
        """
        return self.value

def raise_exception(err_msg, ip_addr=None):
    """
    예외를 발생하는 함수
    """
    raise CustomException(err_msg)

class ThreadedTCPRequestHandler(BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        cur_thread = threading.current_thread()
        print("{} was started for {}"
              .format(cur_thread.getName(), self.client_address[0]))

        while True:
            try:
                self.recv_data = self.request.recv(1024).strip()

                # :/quit 를 입력하거나 데이터가 없다면 루프를 종료
                if self.recv_data == ":/quit" or not self.recv_data:
                    raise_exception("{} was gone".format(self.client_address[0]))

            except NameError as e:
                print("{0} got an error : {1}".format(self.client_address[0], e))
                self.request.send("Bye")
                break

            except Exception as e:
                print(e)
                self.request.send("Bye")
                break

            print("{} wrote:".format(self.client_address[0]))
            print(self.recv_data)

            # 영어의 소문자 데이터를 receive 하면 대문자로 변환해 send
            self.request.sendall(self.recv_data.upper())

        print("{} was ended for {}"
              .format(cur_thread.getName(), self.client_address[0]))

class serversocket:
    def __init__(self, host = "0.0.0.0", port = 23400):
        self.host = host
        self.port = port
        
    def run(self):
        # 소켓 객체 생성
        try:
            server = ThreadingTCPServer((self.host, self.port), ThreadedTCPRequestHandler)

        except socket.error as msg:
            print("Bind failed. Closing...")
            print("Error code: %s \nError Message: %s"% (str(msg[0]), msg[1]))
            sys.exit()

        print("Socket bound on {}".format(self.port))
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        server.serve_forever()

        server.shutdown()
        server.server_close()
