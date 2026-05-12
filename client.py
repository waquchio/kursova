import socket
import json
import random

def send_request(request_data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5555))
        payload = json.dumps(request_data) + "\n"
        client.sendall(payload.encode('utf-8'))
        
        buffer = ""
        while True:
            data = client.recv(4096).decode('utf-8')
            buffer += data
            if "\n" in buffer:
                raw_response, _ = buffer.split("\n", 1)
                return json.loads(raw_response)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        client.close()

def main():
    while True:
        print("\n=== Сервіс Обробки Масивів ===")
        print("1. Згенерувати масив та відсортувати")
        print("2. Згенерувати масив та відсортувати")
        print("3. Вихід")
        choice = input("Виберіть дію (1-3): ")
        
        if choice == '3':
            print("Вихід з программи...")
            break
            
        try:
            size = int(input("Введіть розмір масиву: "))
            arr = [random.randint(1, 10000) for _ in range(size)]
            
            if choice == '1':
                algo = input("Алгоритм сортування (bubble / quick): ").strip().lower()
                req = {"action": "sort", "algorithm": algo, "data": arr}
                
            elif choice == '2':
                algo = input("Алгоритм пошуку (linear / binary): ").strip().lower()
                target = int(input("Введіть число для пошуку: "))
                
                if algo == "binary":
                    arr.sort() 
                    
                req = {"action": "search", "algorithm": algo, "target": target, "data": arr}
            else:
                print("Невірний вибір. Спробуйте знову.")
                continue
                
            print("\nВідправка запиту на сервер...")
            response = send_request(req)
            
            if response.get("status") == "success":
                print(f"Операція виконана успішно!")
                print(f"Час виконання на сервері: {response.get('execution_time_ms'):.4f} ms")
                
                if choice == '2':
                    idx = response.get('result')
                    if idx != -1:
                        print(f"Елемент знайдено за індексом: {idx}")
                    else:
                        print("Елемент не знайдено в масиві.")
            else:
                print(f"Сталася помилка: {response.get('message')}")
                
        except ValueError:
            print("Помилка введення. Будь ласка, вводіть лише числа там, де це потрібно.")

if __name__ == "__main__":
    main()