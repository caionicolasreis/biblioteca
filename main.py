#!/usr/bin/env python3

import json
import sys
from datetime import date
from pathlib import Path

print("Bem vindo a biblioteca do Mago, o Inefável.\n")



# Carregando os dados JSON
biblioteca = Path('data.json')

def carregar(arquivo = biblioteca):
    """Carrega o arquivo da biblioteca do Mago
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

dados = carregar()
dados_backup = carregar()
print(f"Biblioteca carregada com sucesso a partir de {biblioteca.resolve()}.\n")



# Criando uma exibição dos livros disponíveis na biblioteca. Quando os dados crescerem, isso mudará.
livros = []

for d in dados:
    livros.append(f"{d["autor"]} - {d["nome"]}")
print(f"Os livros atualmente disponíveis são:")
for l in livros:
    print(f"- {l}")



# Função para inserir novos dados em data.json
def inserir_dados():
    while True:
        lido = input("Esse livro já foi lido, mesmo que parcialmente(s/n)?: ")
        if lido in ("s", "y"): # or não é aplicável - criaria um truthy
            nome = input("Insira o nome do livro: ")
            autor = input("Insira o autor do livro: ")
            print("Cadastre as datas de leitura em formato ISO (AAAA-MM-DD). Pressione Enter para pular qualquer etapa.")

            def inserir_data(data): # Função que permitirá cálculos de datas antes do salvamento
                """Converte uma string de data para formato ISO (AAAA-MM-DD).
                Permite novas tentativas caso ocorra algum ValueError."""
                while True:
                    if data == "":
                        return None
                    try:
                        return date.fromisoformat(data)
                    except ValueError:
                        data = input("Data inválida. Tente novamente com o formato ISO (AAAA-MM-DD): ")

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
        else: # Não vejo muita necessidade desse else existir. Mas ele não fere o código por agora.
            print("Resposta inválida.")

    # Inserção de tags individuais sequencialmente - procurar uma forma de inserir diversas
    tags = []
    print("Insira uma tag por vez")
    while True:
        tag = input("Insira uma tag (Enter para sair): ")
        if tag == "": # Não entendi por que utilizar 'None' não funcionou aqui - pesquisar
            break
        tags.append(tag)

    # Preparando dados para serem inseridos no JSON
    def para_json(valor):
        """Tenta converter algum valor para uma data de formato ISO (AAAA-MM-DD).
        Retorna Null caso nada seja inserido.

        Quebra em qualquer entrada que não seja possível converter para o formato ISO."""
        if valor:
            return valor.isoformat()
        else:
            return valor

    insercao = {
        "nome": nome,
        "autor": autor,
        "inicio": para_json(inicio),
        "fim": para_json(fim),
        "interrompido": para_json(interrompido),
        "retornado": para_json(retornado),
        "tags": tags
    }

    # Confirmando se os dados estão corretos diretamente com o usuário e inserido caso estejam
    while True:
        confirmacao_insercao = input(f"Os dados que serão cadastrados são: \n\n {insercao} \n\n\n\n Esses dados inseridos estão corretos(s/n)?: ")
        if confirmacao_insercao in ("s", "y"): # or não é aplicável - criaria um truthy
            dados.append(insercao)
            print(f"Dados adicionados com sucesso. O livro {insercao['autor']} - {insercao['nome']} foi inserido com sucesso.")
            print(f'\nUtilize a função "salvar()" para tornar as modificações permanentes.')
            break
        elif confirmacao_insercao == "n":
            print("Inserção cancelada.")  # Posso criar algo melhor para editar o que foi inserido caso a resposta seja "n"
            break
        else:
            print("Resposta inválida.")



# Selecionando e removendo uma entrada dos dados
def remover_dados():
    """Remove uma ou mais entradas dos dados JSON."""
    alvos = []
    cont_alvos = 0
    multiplos = input("Deseja remover múltiplos livros (s/n)?: ")
    if multiplos in ("s", "y"):
        print("\nDigite o nome de um livro por vez. Insira um valor vazio para finalizar.\n")
        while True:
            nome = input("Insira o nome do livro a ser removido: ")
            if nome != "":
                alvos.append(nome)
                cont_alvos += 1
            else:
                break
    else:
        alvos = input("Insira o nome do livro a ser removido: ")
    cont_remocoes = 0
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
    else:
        print(f"\nO Processo de remoção foi concluído e nenhum livro foi removido.") # Considerando que nunca existirão menos de 0 alvos
        return
    print(f'\nUtilize a função "salvar()" para tornar as modificações permanentes.')


# Placeholder da função de reversão
# Essa função vai precisar de um contador de inserções para saber como gerir os backups de dados em memória
def reverter_modificacoes():
    print("Função em desenvolvimento. Reclame com o Dev.")



# Salvando dados no JSON da biblioteca
# Pesquisando sobre, descobri que utilizar um arquivo temporário é interessante para proteger o arquivo original de erros.
def salvar_modificacoes(arquivo = biblioteca):
    try:
        with open(arquivo, "w") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            print(f"Inserções salvas com sucesso em: {biblioteca.resolve()}")
    except (OSError, TypeError) as e:
        print(f"Ocorreu um erro durante o salvamento no arquivo: {biblioteca.resolve()}:\n\n{e}")
    except Exception as e:
        print(f"Ocorreu um erro:\n\n{e}")
