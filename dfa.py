class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states # q
        self.alphabet = alphabet # inputs
        self.transition_function = transition_function # delta
        self.start_state = start_state # q0
        self.accept_states = accept_states # F

    def run(self, input_string):
        current_state = self.start_state
        while input_string != "":
            current_state = self.transition_function[(current_state, input_string[0])]
            char = input_string[0]
            if char not in self.alphabet:
                raise ValueError(f"Invalid character '{char}' in input string.")
            input_string = input_string[1:]
        return current_state in self.accept_states

relop_dfa = DFA(
    states={
        "q0", # start state
        "q1", # first char
        "q2", # LE
        "q3", # NE
        "q4", # LT
        "q5", # EQ
        "q6", # other first char
        "q7", # GE
        "q8", # GT
    },
    alphabet={">", "<", "=", "!"},
    transition_function={
        ("q0", "<"): "q1",
        ("q0", "="): "q5",
        ("q0", ">"): "q6",

        ("q1", "="): "q2",
        ("q1", ">"): "q3",
        ("q1", None): "q4", # other "operation"

        ("q6", "="): "q7",
        ("q6", None): "q8", # other "operation"
    },
    start_state="q0",
    accept_states={"q2", "q3", "q4", "q5", "q7", "q8"},
)

# id_dfa
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
letters_digits = letters + digits

transition_function = {}

# Adicionando todos os inputs possíveis
for ch in letters:
    transition_function[("q9", ch)] = "q10"

for ch in letters_digits:
    transition_function[("q10", ch)] = "q10"

id_dfa = DFA(
    states={"q9", "q10"},
    alphabet=set(letters_digits),
    transition_function=transition_function,
    start_state="q9",
    accept_states={"q10"}
)
