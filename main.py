#!/usr/bin/env python3

import json
import sys
from pathlib import Path

print("Bem vindo a biblioteca do Mago, o Inefável.\n")



# Carregando os dados JSON.
biblioteca = Path('data.json')

def carregar(arquivo = biblioteca):
    """Carrega o arquivo do biblioteca do Mago

    Self-contained com error handling e sys.exit. Termina o programa em qualquer erro.
    """
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        sys.exit(f"Arquivo não encontrado: {e.filename}")
    except json.JSONDecodeError as e:
        sys.exit(f"{biblioteca.resolve()} corrompido na linha {e.lineno}: {e.msg}")
    except Exception as e:
        sys.exit(f"Algum erro ocorreu durante o carregamento do arquivo:\n\n{e}")

dados = carregar()
print(f"Biblioteca carregada com sucesso a partir de {biblioteca.resolve()}.\n")



# Criando uma exibição dos livros disponíveis na biblioteca. Quando os dados crescerem, isso mudará.
livros = []

for i in dados:
    livros.append(f"{i["autor"]} - {i["nome"]}")

print(f"Os livros atualmente disponíveis são:")
for livro in livros:
    print(f"- {livro}")



# Função para inserir novos dados em data.json
def inserir_livro():
    lido = input("Esse livro já foi lido, mesmo que parcialmente(s/n)?\n")
    nome = input("Insira o nome do livro: ")
    autor = input("Insira o autor do livro: ")
    if lido == "s": # falta incluir "y"
        inicio = input("Insira quando iniciou a leitura do livro (Enter para vazio): ")        # não deveria aceitar inputs que não sejam datas (YYYY-MM-DD)
        fim = input("Insira quando finalizou a leitura do livro (Enter para vazio): ")         # não deveria aceitar inputs que não sejam datas (YYYY-MM-DD)
        interrompido = input("Insira quando interrompeu a leitura livro (Enter para vazio): ") # não deveria aceitar inputs que não sejam datas (YYYY-MM-DD)
    else: # inclui inputs incorretos
        inicio = fim = interrompido = None
    # Inserção de tags individuais sequencialmente - procurar uma forma de inserir diversas
    tags = []
    print("Insira uma tag por vez")
    while True:
        tag = []
        tag = input("Insira uma tag (Enter para sair): ")
        if tag == "": # não entendi por que utilizar 'None' não funcionou aqui - pesquisar
            break
        tags.append(tag)
    insercao = {"nome": nome, "autor": autor, "inicio": inicio, "fim": fim, "interrompido": interrompido, "tags": tags}
    confirmacao_insercao = input(f"{insercao}\n\nEsses dados inseridos estão corretos(s/n)?\n")
    if confirmacao_insercao == "s": # falta incluir "y"
        dados.append(insercao)
        print("Dados adicionados com sucesso. Salve as mudanças com a função ""Salvar"" para as tornar permanentes.")
    else: # inclui inputs incorretos - encontrar forma de corrigir isso
        print("Inserção cancelada.") # posso criar algo melhor para editar o que foi inserido caso a resposta seja "n"



# Placeholder de função de salvamento
def salvar():
    print("Função ainda não funcional. Reclame com o dev.")