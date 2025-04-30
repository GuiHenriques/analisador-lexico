# Trabalho de Compiladores - Parte A
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

# DFA para operadores relacionais válidos: <, <=, >, >=, =, <>
relop_states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
relop_alphabet = {">", "<", "="}
relop_transitions = {
    ("q0", "<"): "q1",   # pode ser < ou <>
    ("q0", ">"): "q2",   # pode ser > ou >=
    ("q0", "="): "q3",   # apenas '='

    ("q1", "="): "q4",   # <=
    ("q1", ">"): "q5",   # <>
    ("q2", "="): "q6",   # >=
}

relop_start = "q0"

relop_accept = {
    "q1",  # < 
    "q2",  # >
    "q3",  # =
    "q4",  # <=
    "q5",  # <>
    "q6",  # >=
}


# DFA para identificadores (letra seguida de letras ou digitos)
id_states = {"q0", "q1"}
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
id_alphabet = set(letters + digits)
id_transitions = {}
# Transicao do estado inicial q0: ao ler qualquer letra, vai para q1
for ch in letters:
    id_transitions[("q0", ch)] = "q1"
# Transicao do estado q1: ao ler letra ou digito, permanece em q1
for ch in letters + digits:
    id_transitions[("q1", ch)] = "q1"
id_start = "q0"
id_accept = {"q1"}

# DFA para numeros inteiros (uma ou mais digitos)
num_states = {"q0", "q1"}
num_alphabet = set(digits)
num_transitions = {}
# Transicao do estado inicial q0: ao ler qualquer digito, vai para q1
# Transicao do estado q1: ao ler digito, permanece em q1
for d in digits:
    num_transitions[("q0", d)] = "q1"
    num_transitions[("q1", d)] = "q1"
num_start = "q0"
num_accept = {"q1"}

# Instanciacao dos DFAs
relop_dfa = DFA(relop_states, relop_alphabet, relop_transitions, relop_start, relop_accept)
id_dfa = DFA(id_states, id_alphabet, id_transitions, id_start, id_accept)
num_dfa = DFA(num_states, num_alphabet, num_transitions, num_start, num_accept)
