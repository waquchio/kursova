import socket
import json
import random

def send_request(request_data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Подключаемся к локальному серверу
        client.connect(('127.0.0.1', 5555))
        payload = json.dumps(request_data) + "\n"
        client.sendall(payload.encode('utf-8'))
        
        buffer = ""
        while True:
            data = client.recv(4096).decode('utf-8')
            buffer += data
            # Ждем символ переноса строки в ответе
            if "\n" in buffer:
                raw_response, _ = buffer.split("\n", 1)
                return json.loads(raw_response)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        client.close()

def main():
    while True:
        print("\n=== Сервис Обработки Массивов ===")
        print("1. Сгенерировать массив и отсортировать")
        print("2. Сгенерировать массив и найти элемент")
        print("3. Выход")
        choice = input("Выберите действие (1-3): ")
        
        if choice == '3':
            print("Выход из программы...")
            break
            
        try:
            size = int(input("Введите размер массива: "))
            # Генерируем массив случайных чисел
            arr = [random.randint(1, 10000) for _ in range(size)]
            
            if choice == '1':
                algo = input("Алгоритм сортировки (bubble / quick): ").strip().lower()
                req = {"action": "sort", "algorithm": algo, "data": arr}
                
            elif choice == '2':
                algo = input("Алгоритм поиска (linear / binary): ").strip().lower()
                target = int(input("Введите число для поиска: "))
                
                if algo == "binary":
                    # Бинарный поиск работает только на отсортированном массиве
                    arr.sort() 
                    
                req = {"action": "search", "algorithm": algo, "target": target, "data": arr}
            else:
                print("Неверный выбор. Попробуйте снова.")
                continue
                
            print("\nОтправка запроса на сервер...")
            response = send_request(req)
            
            if response.get("status") == "success":
                print(f"Операция выполнена успешно!")
                print(f"Время выполнения на сервере: {response.get('execution_time_ms'):.4f} ms")
                
                if choice == '2':
                    idx = response.get('result')
                    if idx != -1:
                        print(f"Элемент найден по индексу: {idx}")
                    else:
                        print("Элемент не найден в массиве.")
            else:
                print(f"Произошла ошибка: {response.get('message')}")
                
        except ValueError:
            print("Ошибка ввода. Пожалуйста, вводите только числа там, где это требуется.")

if __name__ == "__main__":
    main()