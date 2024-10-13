import threading  # Importa o módulo threading para trabalhar com threads
import time  # Importa o módulo time para medir o tempo de execução
import psutil  # Importa o psutil para medir o uso de CPU e memória
import os  # Importa o os para obter o ID do processo atual


def num_primo(n):  # Função que verifica se um número é primo
    if n < 2:  # Se o número for menor que 2, não é primo
        return False
    for i in range(2, int(n**0.5) + 1):  # Verifica se o número é divisível por algum valor até a raiz quadrada dele
        if n % i == 0:  # Se for divisível, não é primo
            return False
    return True  # Se não for divisível por nenhum valor, é primo


def calcular_primos(start, end, primost):  # Função que calcula os números primos dentro de um intervalo
    for num in range(start, end):  # Itera pelos números dentro do intervalo
        if num_primo(num):  # Verifica se o número é primo
            primost.append(num)  # Adiciona primos à lista
        if len(primost) >= 50:  # Ao encotrar 50 primos, interrompe a busca
            break


if __name__ == '__main__':
    start_time = time.time()  # Marca o tempo inicial de execução

    primes1 = []  # Lista para armazenar os primos calculados pela primeira thread
    primes2 = []  # Lista para armazenar os primos calculados pela segunda thread

    # Cria a primeira thread para calcular primos no intervalo de 2 a 500
    thread1 = threading.Thread(target=calcular_primos, args=(2, 500, primes1))

    # Inicia a primeira thread
    thread1.start()
    # Aguarda que a primeira thread termine
    thread1.join()

    # Verifica se há primos na lista 1 e inicia a segunda thread com o último primo encontrado
    if primes1:
        last_prime = primes1[-1] + 1  # O próximo número a ser verificado é o último primo + 1
        thread2 = threading.Thread(target=calcular_primos, args=(last_prime, 1000, primes2))

        # Inicia a segunda thread
        thread2.start()
        # Aguarda que a segunda thread termine
        thread2.join()

    # Combina os primos das duas listas, ajustando para ter no máximo 100 primos
    all_primes = sorted(primes1 + primes2)
    print(f"Processo 1 calcula os primos de 2 á 500:\n {primes1}\n")
    print(f"Processo 2 calcula os primos do fim da lista 1 á 1000:\n {primes2}\n")
    # Exibe os números primos encontrados
    print(f"Lista dos números primos encontrados (ordenada):\n {all_primes[:100]}\n")  # Exibe apenas os 100 primeiros
    # Exibe o tempo de execução
    print(f"Tempo de execução (Threads): {time.time() - start_time:.4f} seconds")

    # Medição de uso de CPU e memória
    process = psutil.Process(os.getpid())  # Obtém o processo atual para medir o uso de CPU e memória
    cpu_usage = process.cpu_percent(interval=0.0010)  # Mede o uso de CPU com um intervalo de 1 segundo
    memory_info = process.memory_info().rss / (1024 ** 2)  # Mede o uso de memória em MB

    # Exibe o uso de CPU e memória
    print(f"Medição de uso de CPU: {cpu_usage}%")
    print(f"Medição de uso de memoria: {memory_info:.2f} MB")
