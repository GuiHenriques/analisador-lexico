# Trabalho de Compiladores - Parte 1

## Grupo
Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques


## Parte A – Analisador Léxico com DFA

### Estrutura dos arquivos

- `parte-a/lexer.py` → Implementação do analisador léxico usando diagramas de transição (DFA).
- `parte-a/dfa.py` → Definição dos autômatos para identificadores, números inteiros e operadores relacionais.
- `parte-a/tokens.py` → Definições de tokens e operadores relacionais.
- `parte-a/table.py` → Implementação da tabela de símbolos com palavras-chave.
- `parte-a/main.py` → Arquivo principal para execução do analisador léxico.
- `parte-a/test-files/valida.txt` → Exemplo de entrada correta (sem erros léxicos).
- `parte-a/test-files/invalida.txt` → Exemplo de entrada com erro léxico.

---

### Como executar

No terminal Linux:

```bash
python3 parte-a/main.py parte-a/test-files/valida.txt
```

Para testar com erro léxico:

```bash
python3 parte-a/main.py parte-a/test-files/invalida.txt
```

---

## Parte B – Analisador Léxico com PLY

### Estrutura dos arquivos

- `parte-b/lexer_ply.py` → Implementação do analisador léxico usando a biblioteca PLY.
- `parte-b/main_ply.py` → Arquivo principal para execução do analisador com PLY.
- `parte-b/test-files/valida.lsi` → Exemplo de entrada válida conforme a linguagem LSI-2025-1.
- `parte-b/test-files/invalida.lsi` → Exemplo de entrada com erro léxico.

---

### Como executar

Primeiro, instale a biblioteca PLY:

```bash
pip install ply
```

Em seguida, execute:

```bash
python3 parte-b/main_ply.py parte-b/test-files/valida.lsi
```

Para testar com erro léxico:

```bash
python3 parte-b/main_ply.py parte-b/test-files/invalida.lsi
```