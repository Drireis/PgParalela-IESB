import time  # Importar o módulo time para medir o tempo de execução
import multiprocessing  # Importa o módulo multiprocessing para trabalhar com subprocessos
import psutil  # Importa o psutil para medir o uso de CPU e memória
import os  # Importa o os para obter o ID do processo atual


def num_primo(n):  # Função que verifica se um número é primo

    if n < 2:  # Se o número for menor que 2, não é primo
        return False
    for i in range(2, int(n**0.5) + 1):  # Verifica se o número é divisível por algum valor até a raiz quadrada dele
        if n % i == 0:  # Se for divisível, não é primo
            return False
    return True  # Se não for divisível por nenhum valor, é primo


def calcular_primos(start, end):   # Função que calcula os números primos dentro de um intervalo
    local_primos = []  # Lista para armazenar os números primos
    for num in range(start, end):  # Itera pelos números dentro do intervalo
        if num_primo(num):  # Verifica se o número é primo
            local_primos.append(num)  # Adiciona primos à lista
        if len(local_primos) >= 50:  # Ao encontrar 50 primos, interrompe a busca
            break
    return local_primos  # Retorna a lista de primos


if __name__ == '__main__':
    start_time = time.time()  # Marca o tempo inicial de execução

    # Cria um pool de subprocessos com 2 processos
    with multiprocessing.Pool(processes=2) as pool:
        # Inicia subprocessos para calcular primos em dois intervalos
        result1 = pool.apply_async(calcular_primos, (2, 500))
        primos1 = result1.get()  # Armazena os primeiros 50 nnúmeros primos
        result2 = pool.apply_async(calcular_primos, (primos1[-1] + 1, 1000))   # Calcula os próximos 50 números
        primos2 = result2.get()

    # Combina os primos das duas listas, ajustando para ter no máximo 100 primos
    primos = primos1 + primos2[:100 - len(primos1)]
    print(f"Processo 1 calcula os primos de 2 á 500:\n {primos1}\n")
    print(f"Processo 2 calcula os primos do ultimo da lista 1 até 1000:\n {primos2}\n")
    # Exibe os números primos encontrados
    print(f"Lista dos 100 primeiros números primos encontrados (ordenada):\n {primos}\n")
    # Exibe o tempo de execução
    print(f"Tempo de execução (Subprocessos): {time.time() - start_time:.4f} segundos.")

    # Medição de uso de CPU e memória
    process = psutil.Process(os.getpid())  # Obtém o processo atual para medir o uso de CPU e memória
    cpu_usage = process.cpu_percent(interval=0.1000)  # Mede o uso de CPU com um intervalo de 1 segundo
    memory_info = process.memory_info().rss / (1024 ** 2)  # Mede o uso de memória em MB

    # Exibe o uso de CPU e memória
    print(f"Medição de uso de CPU: {cpu_usage}%")
    print(f"Medição de uso de memoria: {memory_info:.2f} MB")
