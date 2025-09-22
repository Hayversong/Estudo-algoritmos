import os
import random
import platform

def criar_arquivo_teste(nome_arquivo, n_registros):
    """gera um arquivo com n_registros de numeros aleatorios"""
    with open(nome_arquivo, 'w') as f:
        for _ in range(n_registros):
            f.write(str(random.randint(0, 10000)) + '\n')

def fase_1_ordenacao(input_file, tamanho_bloco):
    """le o arquivo de entrada, divide em blocos, ordena e salva no disco"""
    blocos_temporarios = []
    
    with open(input_file, 'r') as f:
        while True:
            bloco = []
            # Lê um bloco de dados do arquivo de entrada
            for _ in range(tamanho_bloco):
                linha = f.readline()
                if not linha:
                    break
                bloco.append(int(linha.strip()))
            
            if not bloco:
                break
            
            # Ordena o bloco na memória principal
            bloco.sort() 
            
            # Salva o bloco ordenado em um arquivo temporário
            nome_bloco = f'temp_bloco_{len(blocos_temporarios)}.txt'
            with open(nome_bloco, 'w') as out_f:
                for item in bloco:
                    out_f.write(str(item) + '\n')
            
            blocos_temporarios.append(nome_bloco)
            
    return blocos_temporarios

# Exemplo de uso:
# criar_arquivo_teste('dados.txt', 1000)
# blocos = fase_1_ordenacao('dados.txt', 100)
# print(f'Arquivos temporários criados: {blocos}')