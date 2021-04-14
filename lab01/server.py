import pickle
from hamming_algorithm import *

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_name = host_name_by_addr[2]
address = (host_name[0], port)
print(address)
srv.bind(address)
srv.listen()
conn, addr = srv.accept()
print('Подключился:', addr)
print("Сервер запущен")

data = recv_all(conn)
dataList = [int(i) for i in data.decode()]
decoded_with_err = hamming_decode(dataList, False)
print(decoded_with_err)
decoded = hamming_decode(dataList)
print(decoded)
encoded_without_err = encode_to_hamming(decoded)
indexes = list_different_index(encoded_without_err, data.decode())

data_away = pickle.dumps(indexes)
data=pickle.dumps(encoded_without_err)
conn.send(data_away)
conn.send(data)
