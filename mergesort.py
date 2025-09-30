import os
import random
import heapq

# --- Parâmetros do Trabalho ---
N_REGISTROS = 500  # n > 50, conforme solicitado
TAMANHO_BLOCO = 50  # Define o tamanho de cada bloco que cabe na memória (M)
ARQUIVO_ENTRADA = 'dados_nao_ordenados.txt'
ARQUIVO_SAIDA = 'dados_ordenados.txt'
K = 5

# ----------------------------------------------------
# 1. FUNÇÃO PARA GERAR O ARQUIVO DE TESTE
# ----------------------------------------------------
def criar_arquivo_teste(nome_arquivo, n_registros):
    """Gera um arquivo com n_registros de números inteiros aleatórios."""
    print(f"-> Gerando arquivo de teste com {n_registros} registros...")
    with open(nome_arquivo, 'w') as f:
        for _ in range(n_registros):
            # Usando números aleatórios para simular os registros
            f.write(str(random.randint(0, 100000)) + '\n')
    print(f"   Arquivo '{nome_arquivo}' criado com sucesso.")


# ----------------------------------------------------
# 2. FASE 1: ORDENAÇÃO INTERNA E CRIAÇÃO DE BLOCOS
# ----------------------------------------------------
def fase_1_ordenacao(input_file, tamanho_bloco):
    """
    Divide o arquivo de entrada em blocos, ordena cada bloco na memória principal 
    e salva-os em arquivos temporários em disco.
    """
    print("\n-> INÍCIO da Fase 1: Ordenação Interna e Criação de Blocos")
    blocos_temporarios = []
    contador_bloco = 0
    
    # Abrindo o arquivo de entrada
    with open(input_file, 'r') as f:
        while True:
            bloco = []
            
            # 1. Leitura de um bloco de dados (conjunto menor de dados)
            for _ in range(tamanho_bloco):
                linha = f.readline()
                if not linha:
                    break
                try:
                    bloco.append(int(linha.strip()))
                except ValueError:
                    # Trata o caso de linhas vazias ou não numéricas
                    continue 
            
            if not bloco:
                break
            
            # 2. Ordenação interna do bloco na memória principal
            bloco.sort() 
            
            # 3. Gravação do bloco ordenado no disco (arquivo temporário)
            nome_bloco = f'temp_bloco_{contador_bloco:03d}.txt'
            with open(nome_bloco, 'w') as out_f:
                for item in bloco:
                    out_f.write(str(item) + '\n')
            
            blocos_temporarios.append(nome_bloco)
            contador_bloco += 1
            
    print(f"   Fase 1 concluída. {len(blocos_temporarios)} blocos ordenados criados e gravados em disco.")
    return blocos_temporarios


# ----------------------------------------------------
# 3. FASE 2: INTERCALAÇÃO (K-WAY MERGE)
# ----------------------------------------------------
def fase_2_intercalacao(blocos_temporarios, output_file, k):

    print("\n-> INÍCIO da Fase 2: Intercalação (Merge)")
    
    round = 0

    # Verifica se ainda existe mais de um arquivo
    while len(blocos_temporarios) > 1:

        novos_blocos = []

        # Interacala K blocos temporários de cada vez
        while blocos_temporarios:

            temp_output = f'temp_{round}'

            # Pega os K arquivo temporários a serem ordenados
            blocos_intermediario = blocos_temporarios[:k]
            blocos_temporarios = blocos_temporarios[k:]

            files = [open(bloco, 'r') for bloco in blocos_intermediario]

            if not files:
                break

            # Usa a árvore de Mean Heap para guardar os valores de forma ordenada
            mh = []
            for i, f in enumerate(files):
                linha = f.readline()
                if linha:
                    heapq.heappush(mh, (int(linha.strip()), i))

            with open(temp_output, 'w') as file:

                while mh:

                    valor, idx = heapq.heappop(mh)

                    file.write(str(valor) + '\n')

                    linha = files[idx].readline()

                    if linha:
                        heapq.heappush(mh, (int(linha.strip()), idx))

                novos_blocos.append(temp_output)

            # Fecha e exclui os arquivos
            for f in files:
                f.close()
                os.remove(f.name)

            round += 1

        blocos_temporarios = novos_blocos

    os.replace(novos_blocos[0], output_file)
        
    print("   Fase 2 concluída. Arquivo final ordenado gerado.")


# ----------------------------------------------------
# 4. EXECUÇÃO PRINCIPAL
# ----------------------------------------------------
def executar_merge_sort_externo():
    
    # Tarefa 1: Gerar arquivo de teste
    criar_arquivo_teste(ARQUIVO_ENTRADA, N_REGISTROS)
    
    # Tarefa 2: Primeira Fase (Ordenação)
    # A leitura do arquivo de teste é feita aqui, e os blocos são gravados em arquivos temporários.
    blocos = fase_1_ordenacao(ARQUIVO_ENTRADA, TAMANHO_BLOCO)
    
    # Tarefa 3: Segunda Fase (Intercalação)
    # A leitura dos arquivos temporários é feita aqui para a intercalação final.
    fase_2_intercalacao(blocos, ARQUIVO_SAIDA, K)

    print("\n[SUCESSO] O processo de Merge Sort Externo foi concluído.")
    print(f"Verifique o arquivo: '{ARQUIVO_SAIDA}' para os resultados ordenados.")

# Executa o programa principal
if __name__ == "__main__":
    executar_merge_sort_externo()