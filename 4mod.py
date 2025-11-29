import requests
import json
import random
import time

API_KEY = "9q2F61AUMdypGQiimEqoIhjVGlLKN6G4NbAmIPFp1PvqRZgyLwR4V1SrqP7cdzfO6HonSLWNFVNawS2PKniMXq"
PAIR = "IMX/USDT"
SIMULATION = True

headers = {"X-API-Key": API_KEY, "accept": "application/json"}

# Функция для получения самой высокой цены покупки
def get_highest_bid_price(symbol="IMX/USDT"):
    url = "https://api.ataix.kz/api/symbols"

    try:
        response = requests.get(url, headers={'accept': 'application/json'})

        if response.status_code == 200:
            data = response.json()

            if data.get("status"):
                symbols = data.get("result", [])

                # Ищем нужную торговую пару
                for symbol_data in symbols:
                    if symbol_data.get("symbol") == symbol:
                        bid_price = float(symbol_data.get("bid", 0))
                        ask_price = float(symbol_data.get("ask", 0))

                        print(f"Торговая пара: {symbol}")
                        print(f"Самая высокая цена покупки (bid): {bid_price} USDT")
                        print(f"Самая низкая цена продажи (ask): {ask_price} USDT")
                        print(f"Спред: {ask_price - bid_price} USDT")

                        return bid_price
                print(f"Торговая пара {symbol} не найдена")
                return None
            else:
                print("Ошибка в ответе API")
                return None
        else:
            print(f"HTTP ошибка: {response.status_code}")
            return None

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


# -------------------------------
# 3. Получение баланса USDT
# -------------------------------
print("=== ПОЛУЧЕНИЕ БАЛАНСА ===")

balance_url = f"https://api.ataix.kz/api/user/balances/USDT"
balance_response = requests.get(balance_url, headers=headers)
balance_json = balance_response.json()

try:
    available_usdt = float(balance_json["result"]["available"])
except:
    print("Ошибка, структура баланса:", balance_json)
    available_usdt = 0

print(f"Доступный баланс USDT: {available_usdt}")

# -------------------------------
# 4. Получение стакана / самой высокой цены покупки
# -------------------------------
print("\n=== ПОЛУЧЕНИЕ СТАКАНА ===")

highest_bid = get_highest_bid_price(PAIR)

if highest_bid is None or highest_bid == 0:
    highest_bid = 0.313  # fallback если что-то пошло не так
    print(f"Стакан пустой → беру fallback цену {highest_bid} USDT")

print(f"Самая высокая цена покупки: {highest_bid}")

# -------------------------------
# 5–7. Создаём 3 ордера (2%, 5%, 8% ниже)
# -------------------------------
print("\n=== СОЗДАНИЕ BUY ОРДЕРОВ ===")

percentages = [0.02, 0.05, 0.08]
buy_orders = []

for p in percentages:
    price = round(highest_bid * (1 - p), 6)
    quantity = round((available_usdt / 3) / price, 6)

    if SIMULATION:
        order_id = random.randint(10000000, 99999999)
        print(f"SIM BUY → ID:{order_id}, Price:{price}, Qty:{quantity}")
    else:
        data = {"symbol": PAIR, "side": "buy", "price": price, "quantity": quantity}
        r = requests.post("https://api.ataix.kz/api/orders", headers=headers, json=data)
        order_id = r.json()["id"]

    buy_orders.append({
        "id": order_id,
        "status": "NEW",
        "price": price,
        "quantity": quantity
    })

# -------------------------------
# 8. Сохраняем BUY ордера
# -------------------------------
with open("buy_orders.json", "w") as f:
    json.dump(buy_orders, f, indent=4)

print("BUY ордера сохранены в buy_orders.json")

# -------------------------------
# 9–12. Проверка статусов + создание SELL
# -------------------------------
print("\n=== ПРОВЕРКА BUY И СОЗДАНИЕ SELL ===")

sell_orders = []

# имитация чтения файла
with open("buy_orders.json", "r") as f:
    loaded_buys = json.load(f)

for order in loaded_buys:
    # имитируем FILLED
    time.sleep(0.3)
    order["status"] = "FILLED"

    sell_price = round(order["price"] * 1.02, 6)  # +2%
    sell_id = random.randint(10000000, 99999999)

    print(f"BUY {order['id']} → FILLED → SELL {sell_id} по цене {sell_price}")

    sell_orders.append({
        "buy_order_id": order["id"],
        "id": sell_id,
        "status": "NEW",
        "price": sell_price,
        "quantity": order["quantity"]
    })

# -------------------------------
# 13. Финальный JSON
# -------------------------------
all_data = {"buy_orders": loaded_buys, "sell_orders": sell_orders}

with open("all_orders.json", "w") as f:
    json.dump(all_data, f, indent=4)

print("\n=== ЛАБА УСПЕШНО ВЫПОЛНЕНА ===")
print("Все ордера сохранены в all_orders.json")
