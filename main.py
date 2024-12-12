import json
from web3 import Web3

# Настроим подключение к сети BSC (Binance Smart Chain)
bsc_url = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc_url))

# Проверяем подключение
if not web3.is_connected():
    print("Не удалось подключиться к сети BSC.")
    exit()

# Адрес контракта для получения информации о токенах (ERC20)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Адрес токена, который вы хотите проверять (например, USDT на BSC)
token_address = "0x59E69094398AfbEA632F8Bd63033BdD2443a3Be1"

# Проверяем, что это корректный адрес
if not web3.is_address(token_address):
    print(f"Некорректный адрес токена: {token_address}")
    exit()

# Создаем контракт для взаимодействия с токеном
token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)

# Функция для проверки наличия токенов на адресе
def check_tokens(wallet_address):
    try:
        # Получаем количество токенов на кошельке
        balance = token_contract.functions.balanceOf(wallet_address).call()
        # Получаем количество десятичных знаков токена (decimals)
        decimals = token_contract.functions.decimals().call()
        
        # Преобразуем баланс в читаемый вид, делим на 10^decimals
        readable_balance = balance / (10 ** decimals)
        return readable_balance
    except Exception as e:
        print(f"Ошибка при проверке токенов для адреса {wallet_address}: {e}")
        return 0

# Чтение адресов из файла wallets.txt
def check_wallets_from_file(filename):
    total_tokens = 0  # Переменная для суммирования токенов

    with open(filename, "r") as file:
        for line in file:
            wallet_address = line.strip()
            if web3.is_address(wallet_address):
                print(f"Проверяем адрес: {wallet_address}")
                balance = check_tokens(wallet_address)
                if balance > 0:
                    print(f"Адрес {wallet_address} имеет {balance:.4f} токенов.")
                    total_tokens += balance  # Добавляем баланс к общей сумме
                else:
                    print(f"Адрес {wallet_address} не имеет токенов.")
            else:
                print(f"Некорректный адрес в файле: {wallet_address}")
    
    return total_tokens

# Основной блок программы
if __name__ == "__main__":
    filename = "wallets.txt"
    total_tokens = check_wallets_from_file(filename)
    
    print(f"\nОбщее количество токенов на всех кошельках: {total_tokens:.4f}")
