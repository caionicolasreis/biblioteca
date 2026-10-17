#!/usr/bin/env python3

import json
import os
import sys
from copy import deepcopy
from datetime import date
from pathlib import Path

print("Bem vindo a Biblioteca do Mago, o Inefável.\n")



# Carregando dados e preparando pontos para retorno
biblioteca = Path('data.json')

# Definindo a função de carregamento
def carregar(arquivo = biblioteca):
    """Carrega o arquivo da biblioteca do Mago.

    Self-contained com error handling e sys.exit. Termina o programa em qualquer erro."""
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except (OSError) as e:
        sys.exit(f"Ocorreu um erro durante o carregamento do arquivo: {biblioteca.resolve()}:\n\n{e}")
    except json.JSONDecodeError as e:
        sys.exit(f"{biblioteca.resolve()} corrompido na linha {e.lineno}: {e.msg}")
    except Exception as e:
        sys.exit(f"Ocorreu um erro:\n\n{e}")

# Definindo a função de criação de snapshots
def criar_snapshot(dados_entrada, historico_snapshots, limite = 10):
    """Guarda até n snapshots que podem ser utilizados sob demanda.

    Automaticamente apaga o mais antigo com `pop(0)` ao superar o limite estabelecido."""
    snapshot_removido = False
    historico_snapshots.append(deepcopy(dados_entrada))
    if len(historico_snapshots) > limite:
        historico_snapshots.pop(0)
        snapshot_removido = True
    if snapshot_removido == True:
        print(f"Snapshot criado. Entrada mais antiga removida.\n{len(historico_snapshots)} snapshots existentes.")
    elif len(historico_snapshots) == 1:
        print(f"Snapshot criado.\n1 snapshot existente.")
    else:
        print(f"Snapshot criado.\n{len(historico_snapshots)} snapshots existentes.")

# Definindo a função de reversão para algum snapshot
def carregar_snapshot(dados_atuais, menu = "n", i = 0):
    """Carrega uma snapshot.

    Permite exibição e escolha direta das opções de snapshot pelo parâmetro 'menu' (s/n)."""
    cancelamento = False
    while True:
        if menu in ("s", "y"):
            for i, valores in enumerate(snapshots):
                print(i, "- ", valores, "\n")
            try:
                i = int(input("Insira qual snapshot deseja restaurar: "))
            except ValueError:
                cancelamento = True # Interpretando inputs vazios como tentativa de saída
                break
            break
        elif menu == "n":
            break
        else:
            print("Resposta inválida.")
    try:
        if cancelamento == False:
            dados_atuais[:] = deepcopy(snapshots[i]) # Sem o slicing, é interpretado como variável local nesse caso
            print(f"Snapshot {i} carregado com sucesso.")
            criar_snapshot(dados, snapshots)         # Atualiza a lista de snapshots. Cria duplicidade,
                                                     # mas preserva histórico correto
        else:
            print("Carregamento cancelado.")
            return
    except IndexError:
        print(f"O snapshot {i} não existe.")
        return
    except Exception as e:
        print(f"Ocorreu um erro durante o carregamento do snapshot {i}:\n\n{e}")
        return

# Preparando pontos para retorno
# Notei que esse bloco imprime mensagens de sucesso mesmo em caso de falhas. Falta error handling...
dados = carregar()
print(f"Biblioteca carregada com sucesso a partir de {biblioteca.resolve()}.")
snapshots = []
criar_snapshot(dados, snapshots)


# Criando uma exibição dos livros inseridos recentemente na biblioteca
livros_recentes = []
for d in dados[-1: -6: -1]: # 5 últimos itens, do mais novo para o mais antigo.
    livros_recentes.append(f"{d["autor"]} - {d["nome"]}")
print(f"\nAs aquisições mais recentes da Biblioteca do Mago:\n")
for lr in livros_recentes:
    print(f"- {lr}")

# Variáveis utilizadas em diversas funções
mensagem_salvar = '\nUtilize a função "salvar_modificacoes()" para tornar as modificações permanentes.'

# Função que permitirá cálculos de datas antes do salvamento
def inserir_data(data):
    """Converte uma string de data para formato ISO (AAAA-MM-DD).

    Permite novas tentativas caso ocorra algum ValueError."""
    while True:
        if data == "":
            return None
        try:
            return date.fromisoformat(data)
        except ValueError:
            data = input("Data inválida. Tente novamente com o formato ISO (AAAA-MM-DD): ")

# Função de preparação dos dados para serem inseridos no JSON
def para_json(valor):
    """Tenta converter algum valor para uma data de formato ISO (AAAA-MM-DD).

    Retorna Null caso nada seja inserido.

    Quebra em qualquer entrada que não seja possível converter para o formato ISO.
    A preparação dos dados de entrada já elimina essa possibilidade."""
    if valor:
        return valor.isoformat()
    else:
        return valor

# Função para inserir novos dados em data.json
def inserir_dados():
    """Cria e insere nos dados uma nova entrada.

    Não permite saída da função até seu final."""
    # Input dos dados a serem registrados
    while True:
        lido = input("Esse livro já foi lido, mesmo que parcialmente(s/n)?: ")
        if lido in ("s", "y"): # or não é aplicável - criaria um truthy
            nome = input("Insira o nome do livro: ")
            autor = input("Insira o autor do livro: ")
            # Inputs de tags individuais sequencialmente - procurar uma forma de inserir diversas
            tags = []
            print("Insira uma tag por vez")
            while True:
                tag = input("Insira uma tag (Enter para sair): ")
                if tag == "":
                    break
                tags.append(tag) # Adiciona uma tag por vez na lista
            print("Cadastre as datas de leitura em formato ISO (AAAA-MM-DD). "
                  "Pressione Enter para pular qualquer etapa.")
            inicio = inserir_data(input("Insira quando iniciou a leitura do livro: "))
            fim = inserir_data(input("Insira quando finalizou a leitura do livro: "))
            interrompido = inserir_data(input("Insira quando interrompeu a leitura do livro: "))
            retornado = inserir_data(input("Insira quando retornou a leitura do livro: "))
            break
        elif lido == "n":
            nome = input("Insira o nome do livro: ")
            autor = input("Insira o autor do livro: ")
            tags = []
            inicio = fim = interrompido = retornado = None
            break
        else: # Cobre o caso de respostas vazias; como em um enter acidental
            print("Resposta inválida.")

    # Preparando inserção de dados
    insercao = {
        "nome": nome,
        "autor": autor,
        "tags": tags,
        "inicio": para_json(inicio),
        "fim": para_json(fim),
        "interrompido": para_json(interrompido),
        "retornado": para_json(retornado)
    }

    # Confirmando se os dados estão corretos diretamente com o usuário e os inserido caso estejam
    while True:
        print(f"Os dados que serão cadastrados são:\n")
        for chave, valor in insercao.items(): # .items() cria uma view com a chave e o valor, permitindo unpacking
            if valor is None or valor is []:
                continue # Para evitar impressões de valores não registrados
            if isinstance(valor, list):  # Checa se valor é uma lista
                valor = ", ".join(valor) # Exibe uma lista como "valor1, valor2, valor3, ..., valorN"
            print(f"{chave.capitalize()}: {valor}") # Capitaliza a chave e exibe o valor
        confirmacao_insercao = input("\nEsses dados inseridos estão corretos(s/n)?: ")
        if confirmacao_insercao in ("s", "y"): # or não é aplicável - criaria um truthy
            dados.append(insercao)
            print(f"Dados adicionados com sucesso. "
                  f"O livro {insercao['autor']} - {insercao['nome']} foi inserido com sucesso.\n")
            criar_snapshot(dados, snapshots)
            print(mensagem_salvar)
            break
        elif confirmacao_insercao == "n":
            print("Inserção cancelada.")  # Posso criar algo melhor para editar o que
                                          # foi inserido caso a resposta seja "n"
            break
        else:  # Cobre o caso de respostas vazias; como em um enter acidental
            print("Resposta inválida.")



# Selecionando e removendo uma entrada dos dados
def remover_dados():
    """Remove uma ou mais entradas dos dados JSON.

    Solicita individualmente diversos livros para a remoção, procura matches com os dados, retorna a entradas
    encontradas e as não encontradas, solicita confirmação para a remoção dos encontrados, remove e cria um snapshot.
    Caso nenhum input seja entregue, nenhum alvo seja encontrado ou o usuário negue a remoção, a função é encerrada.

    Limitações conhecidas:
    - Nào é capaz de discernir entre 2 livros com o mesmo nome e remove apenas o primeiro que encontrar
    - Não existe funcionalidade para alterar os alvos após input"""

    # Criação dos alvos para remoção
    alvos = []        # Lista de alvos
    print("\nDigite o nome de um livro por vez. Insira um valor vazio para finalizar a inserção.\n")
    while True:
        nome = input("Insira o nome do livro a ser removido: ")
        if nome != "":
            alvos.append(nome)
        else:
            break

    # Procura dos alvos dentro dos dados existentes
    encontrado = []     # Lista de dicionários
    nao_encontrado = [] # Lista comum
    for a in alvos:     # Separa os livros encontrados dos não encontrados e os armazena em listas separadas
        alvo_individual = a
        for i, livro in enumerate(dados):
            if alvo_individual.lower() == livro["nome"].lower():
                encontrado.append({"i": i, "autor": livro["autor"], "nome": livro["nome"]})
                break
        else:
            nao_encontrado.append(alvo_individual)

    # Feedback dos resultados da procura
    cont_remocoes = 0 # Contagem de livros removidos
    if len(encontrado) == 0:     # Nenhum encontrado, fim de operação
        print("Nenhum dos livros foi encontrado. Operação encerrada.")
        return
    elif len(encontrado) > 0:    # Pelo menos um encontrado
        print("Foram encontrados os livros:")
        for e_livro in encontrado:
            print(f"- {e_livro["autor"]} - {e_livro["nome"]}") # Utiliza o nome com a capitalização real
    if len(nao_encontrado) > 0 : # Pelo menos um não encontrado
        print("\nNÃO foram encontrados os livros:")
        for ne_livro in nao_encontrado: # Utiliza o nome com a capitalização do usuário
            print(f"- {ne_livro}")

    # Confirmação e remoção dos alvos encontrados
    while True:
        seguir = input("Deseja prosseguir com a remoção dos livros encontrados (s/n)?")
        if seguir in("s", "y"):
            for i in reversed(encontrado):
                dados.pop(i["i"]) # Remove o alvo utilizando o índice da variável "encontrado"
                cont_remocoes += 1
                print(f"O livro {i["autor"]} - {i["nome"]} foi removido com sucesso.")
            break
        elif seguir == "n":
            print("Remoção cancelada.")
            return
        else: # Cobre o caso de respostas vazias; como em um enter acidental
            print("Resposta inválida.")

    # Mensagens finais e criação de snapshot automático
    if len(alvos) == 1:  # Em caso de remoção única
        print(f"\nO processo de remoção foi concluído e "
              f"{cont_remocoes} de {len(alvos)} livro foi removido.\n")
    elif len(alvos) > 1: # Em caso de diversos alvos
        print(f"\nO processo de remoção foi concluído e "
              f"{cont_remocoes} de {len(alvos)} livros foram removidos.\n")
    criar_snapshot(dados, snapshots) # Snapshot criado após as modificações
    print(mensagem_salvar)



# Salvando dados no JSON da biblioteca
def salvar_modificacoes(arquivo = biblioteca):
    """Salva as modificações de 'dados' no arquivo da biblioteca.

    Utiliza um arquivo temporário para salvamento a prova de interrupções"""
    tmp = arquivo.with_suffix(".json.tmp")                    # Cria o endereço do arquivo em memória
                                                              # e substitui '.json' por '.json.tmp'
    try:
        with open(tmp, "w") as f:                             # Cria o arquivo temporário
            json.dump(dados, f, ensure_ascii=False, indent=2) # Preenche o arquivo com 'dados'
        os.replace(tmp, arquivo)                              # mv. Sem brechas para corrupção.
        print(f"Inserções salvas com sucesso em: {biblioteca.resolve()}")
    except (OSError, TypeError) as e:
        print(f"Ocorreu um erro durante o salvamento no arquivo: {biblioteca.resolve()}:\n\n{e}")
    except Exception as e:
        print(f"Ocorreu um erro:\n\n{e}")
    tmp.unlink(missing_ok=True) # Caso o replace (mv) funcione, não resta arquivo para remover (rm).
                                # Mas caso falhe, é necessário. Por isso utiliza-se o 'missing_ok=True'.
