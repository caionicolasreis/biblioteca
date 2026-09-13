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

    Args: arquivo
        default: biblioteca"""
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        sys.exit(f"Arquivo não encontrado: {e.filename}")
    except json.JSONDecodeError as e:
        sys.exit(f"{biblioteca.resolve()} corrompido na linha {e.lineno}: {e.msg}")
    except Exception as e:
        sys.exit(f"Algum erro ocorreu durante o carregamento do arquivo:\n\n{e}")

data = carregar()
print(f"Biblioteca carregada com sucesso a partir de {biblioteca.resolve()}.\n")



# Criando uma exibição dos livros disponíveis na biblioteca. Quando os dados crescerem, isso mudará.
livros = []

for i in data:
    livros.append(f"{i["autor"]} - {i["nome"]}")

print(f"Os livros atualmente disponíveis são:")
for livro in livros:
    print(f"- {livro}")