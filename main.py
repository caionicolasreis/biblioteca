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
        print(f"Snapshot criado. Entrada mais antiga removida.\n{len(historico_snapshots)} snapshots existentes.\n")
    elif len(historico_snapshots) == 1:
        print(f"Snapshot criado.\n1 snapshot existente.\n")
    else:
        print(f"Snapshot criado.\n{len(historico_snapshots)} snapshots existentes.\n")

# Definindo a função de reversão para algum snapshot
def carregar_snapshot(dados_atuais, i = 0):
    dados_atuais[:] = deepcopy(snapshots[i]) # Sem o slicing, é interpretado como variável local nesse caso
    criar_snapshot(dados, snapshots)         # Atualiza a lista de snapshots. Cria duplicidade,
                                             # mas preserva histórico correto

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
print(f"As aquisições mais recentes da Biblioteca do Mago:\n")
for lr in livros_recentes:
    print(f"- {lr}")


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
            inicio = fim = interrompido = retornado = None
            break
        else: # Cobre o caso de respostas vazias; como em um enter acidental
            print("Resposta inválida.")

    # Inputs de tags individuais sequencialmente - procurar uma forma de inserir diversas
    tags = []
    print("Insira uma tag por vez")
    while True:
        tag = input("Insira uma tag (Enter para sair): ")
        if tag == "": # Não entendi por que utilizar 'None' não funcionou aqui - pesquisar
            break
        tags.append(tag)

    # Preparando inserção de dados
    insercao = {
        "nome": nome,
        "autor": autor,
        "inicio": para_json(inicio),
        "fim": para_json(fim),
        "interrompido": para_json(interrompido),
        "retornado": para_json(retornado),
        "tags": tags
    }

    # Confirmando se os dados estão corretos diretamente com o usuário e os inserido caso estejam
    while True:
        confirmacao_insercao = input(f"Os dados que serão cadastrados são: \n\n {insercao} \n\n\n\n "
                                     f"Esses dados inseridos estão corretos(s/n)?: ")
        if confirmacao_insercao in ("s", "y"): # or não é aplicável - criaria um truthy
            dados.append(insercao)
            print(f"Dados adicionados com sucesso. "
                  f"O livro {insercao['autor']} - {insercao['nome']} foi inserido com sucesso.")
            print(f'\nUtilize a função "salvar()" para tornar as modificações permanentes.')
            break
        elif confirmacao_insercao == "n":
            print("Inserção cancelada.")  # Posso criar algo melhor para editar o que
                                          # foi inserido caso a resposta seja "n"
            break
        else:  # Cobre o caso de respostas vazias; como em um enter acidental
            print("Resposta inválida.")



# Selecionando e removendo uma entrada dos dados
def remover_dados():
    """Remove uma ou mais entradas dos dados JSON."""
    alvos = []
    cont_alvos = 0
    cont_remocoes = 0

    multiplos = input("Deseja remover múltiplos livros (s/n)?: ")
    while True:
        if multiplos in ("s", "y"):
            print("\nDigite o nome de um livro por vez. Insira um valor vazio para finalizar.\n")
            while True:
                nome = input("Insira o nome do livro a ser removido: ")
                if nome != "":
                    alvos.append(nome)
                    cont_alvos += 1
                else:
                    break
        elif multiplos == "n":
            alvos = input("Insira o nome do livro a ser removido: ")
            cont_alvos += 1
            break
        else: # Cobre o caso de respostas vazias; como em um enter acidental
            print("Resposta inválida.")

    for a in alvos:
        alvo_individual = a
        for i, livro in enumerate(dados):
            if alvo_individual.lower() == livro["nome"].lower():
                removido = dados.pop(i)
                print(f"Removido com sucesso: {removido['autor']} - {removido['nome']}")
                cont_remocoes += 1
                break
        else: # Adicionar uma confirmação de remoção caso um não seja encontrado
            print(f'O livro "{alvo_individual}" não foi encontrado na biblioteca.')

    if cont_alvos == 1:
        print(f"\nO processo de remoção foi concluído e {cont_remocoes} de {cont_alvos} livro foi removido.")
    elif cont_alvos > 1:
        print(f"\nO processo de remoção foi concluído e {cont_remocoes} de {cont_alvos} livros foram removidos.")
    else: # Está sendo impresso caso apenas um livro seja inserido por meio do else da linha 164. Comentário na linha entrega a solução.
        print(f"\nO Processo de remoção foi concluído e nenhum livro foi removido.") # Considerando que nunca existirão menos de 0 alvos
        return
    print(f'\nUtilize a função "salvar()" para tornar as modificações permanentes.')



# Salvando dados no JSON da biblioteca
def salvar_modificacoes(arquivo = biblioteca):
    """Salva as modificações de 'dados' no arquivo da biblioteca.

    Utiliza um arquivo temporário para salvamento a prova de interrupções"""
    tmp = arquivo.with_suffix(".json.tmp")                    # Cria o endereço do arquivo em memória e substitui '.json' por '.json.tmp'
    try:
        with open(tmp, "w") as f:                             # Cria o arquivo temporário
            json.dump(dados, f, ensure_ascii=False, indent=2) # Preenche o arquivo com 'dados'
        os.replace(tmp, arquivo)                              # mv. Sem brechas para corrupção.
        print(f"Inserções salvas com sucesso em: {biblioteca.resolve()}")
    except (OSError, TypeError) as e:
        print(f"Ocorreu um erro durante o salvamento no arquivo: {biblioteca.resolve()}:\n\n{e}")
    except Exception as e:
        print(f"Ocorreu um erro:\n\n{e}")
    tmp.unlink(missing_ok=True) # Caso o replace (mv) funcione, não resta arquivo para remover (rm). Mas caso falhe, é necessário.
                                # Por isso utiliza-se o 'missing_ok=True'.
