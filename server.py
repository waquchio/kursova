import socket
import threading
import json
import time

# --- Алгоритмы сортировки ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- Алгоритмы поиска ---
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# --- Обработка клиента ---
def handle_client(conn, addr):
    print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ] {addr} подключился.")
    buffer = ""
    while True:
        try:
            # Получаем данные порциями по 4096 байт
            data = conn.recv(4096).decode('utf-8')
            if not data:
                break
            buffer += data
            
            # Ждем символ переноса строки, который означает конец JSON пакета
            if "\n" in buffer:
                raw_request, buffer = buffer.split("\n", 1)
                request = json.loads(raw_request)
                
                action = request.get('action')
                algo = request.get('algorithm')
                arr = request.get('data')
                
                # Засекаем время
                start_time = time.perf_counter()
                result = None
                
                if action == "sort":
                    if algo == "bubble":
                        result = bubble_sort(arr)
                    elif algo == "quick":
                        result = quick_sort(arr)
                        
                elif action == "search":
                    target = request.get('target')
                    if algo == "linear":
                        result = linear_search(arr, target)
                    elif algo == "binary":
                        result = binary_search(arr, target)
                        
                end_time = time.perf_counter()
                
                # Формируем ответ
                response = {
                    "status": "success",
                    "result": result,
                    "execution_time_ms": (end_time - start_time) * 1000
                }
                
                # Отправляем результат обратно клиенту
                conn.sendall((json.dumps(response) + "\n").encode('utf-8'))
        except Exception as e:
            print(f"[ОШИБКА] {e}")
            break
            
    conn.close()
    print(f"[ОТКЛЮЧЕНИЕ] {addr} отключился.")

# --- Запуск сервера ---
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen()
    print("[ЗАПУСК] Сервер слушает на 127.0.0.1:5555")
    
    while True:
        conn, addr = server.accept()
        # Запускаем обработку нового клиента в отдельном потоке
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()