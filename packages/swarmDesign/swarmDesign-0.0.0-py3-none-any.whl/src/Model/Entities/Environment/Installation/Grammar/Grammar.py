import os

POSSIBLE_BEHAVIORS = "(10,11,12,13,14,15,20,21,24,25,28,29,30,31,32,33,34,35,40,41,42,43,44,45,50,51,52,53,54,55)"
POSSIBLE_CONDITIONS = "(10,11,12,13,14,15,20,21,22,23,24,25,27,30,31,32,33,34,35,40,41,42,43,44,45,50,51,52,53,54,55)"
POSSIBLE_BEHAVIORS_CHOCOLATE = "(10,11,12,13,14,15)"
POSSIBLE_CONDITIONS_CHOCOLATE = "(10,11,12,13,14,15)"
POSSIBLE_BEHAVIORS_TUTTI = "(20,21,24,25,28,29)"
POSSIBLE_CONDITIONS_TUTTI = "(20,21,22,23,24,25,27)"
POSSIBLE_BEHAVIORS_COCO = "(30,31,32,33,34,35)"
POSSIBLE_CONDITIONS_COCO = "(30,31,32,33,34,35)"
POSSIBLE_BEHAVIORS_MAPLE = "(40,41,42,43,44,45)"
POSSIBLE_CONDITIONS_MAPLE = "(40,41,42,43,44,45)"
POSSIBLE_BEHAVIORS_HARLEQUIN = "(50,51,52,53,54,55)"
POSSIBLE_CONDITIONS_HARLEQUIN = "(50,51,52,53,54,55)"


class Grammar:

    def __init__(self, flags):
        global POSSIBLE_BEHAVIORS, POSSIBLE_CONDITIONS
        self.behavior = None
        self.condition = None
        self.fsm = flags[0]
        self.bt = flags[1]
        self.chocolate = flags[2]
        self.tuttifrutti = flags[3]
        self.coconut = flags[4]
        self.maple = flags[5]
        self.harlequin = flags[6]
        self.custom = self.create_custom_gram()
        if self.custom:
            self.construct_grammar()
            global POSSIBLE_BEHAVIORS, POSSIBLE_CONDITIONS
            POSSIBLE_BEHAVIORS = self.behavior
            POSSIBLE_CONDITIONS = self.condition
        print(POSSIBLE_BEHAVIORS)
        print(POSSIBLE_CONDITIONS)
        self.generate_grammar("new_grammar.txt")
        print(os.getcwd())

    def create_custom_gram(self):
        return self.chocolate or self.tuttifrutti or self.coconut or self.maple or self.harlequin

    def add_grammar(self, behavior, condition):
        if self.behavior is None:
            self.behavior = behavior
            self.condition = condition
        else:
            self.behavior = self.behavior[:-1] + "," + behavior[1:]
            self.condition = self.condition[:-1] + "," + condition[1:]

    def construct_grammar(self):
        if self.chocolate:
            self.add_grammar(POSSIBLE_BEHAVIORS_CHOCOLATE, POSSIBLE_CONDITIONS_CHOCOLATE)
        if self.tuttifrutti:
            self.add_grammar(POSSIBLE_BEHAVIORS_TUTTI, POSSIBLE_CONDITIONS_TUTTI)
        if self.coconut:
            self.add_grammar(POSSIBLE_BEHAVIORS_COCO, POSSIBLE_CONDITIONS_COCO)
        if self.maple:
            self.add_grammar(POSSIBLE_BEHAVIORS_MAPLE, POSSIBLE_CONDITIONS_MAPLE)
        if self.harlequin:
            self.add_grammar(POSSIBLE_BEHAVIORS_HARLEQUIN, POSSIBLE_CONDITIONS_HARLEQUIN)

    def generate_grammar_fsm(self):
        grammar = ['NumStates  "--nstates "   i (1,4)  | ARCH=="fsm-config"']  # first line
        for i in range(4):
            # state
            grammar.append(f'S{i}     "--s{i} "    c {POSSIBLE_BEHAVIORS}  | as.numeric(NumStates)>{i}')
            grammar.append(f'RWM{i}   "--rwm{i} "  i (1,100) | as.numeric(S{i}) %in% c(10,20,30,32,33,34,35,40)')
            grammar.append(f'ATT{i}   "--att{i} "  r (1,5) | as.numeric(S{i}) %in% c(14,24,34,44)')
            grammar.append(f'REP{i}   "--rep{i} "  r (1,5) | as.numeric(S{i}) %in% c(15,25,35,45)')
            grammar.append(f'VEL{i}   "--vel{i} "  c (1.0) | as.numeric(S{i}) %in% c(28,29)')
            grammar.append(f'CLE{i}   "--cle{i} "  c (0,4,5,6) | as.numeric(S{i}) %in% c(20,21,24,25,28,29)')
            grammar.append(f'CLR{i}   "--clr{i} "  c (1,2,3,4,5,6) | as.numeric(S{i}) %in% c(28,29)')
            grammar.append(f'EXP{i}   "--exp{i} "  c (0,1,2) | as.numeric(S{i}) %in% c(30,32,33,34,35)')
            grammar.append(f'MU{i}    "--mu{i} "   r (1,3) | as.numeric(S{i}) %in% c(30,32,33,34,35)')
            grammar.append(f'RHO{i}   "--rho{i} "  r (0,1) | as.numeric(S{i}) %in% c(30,32,33,34,35)')
            grammar.append(f'NumConnections{i} "--n{i} " i (1,4) | as.numeric(NumStates)>{i if i > 0 else 1}')
            for j in range(4):
                grammar.append(f'N{i}x{j}  "--n{i}x{j} " i   (0,3) | as.numeric(NumConnections{i})>{j}')
                grammar.append(f'C{i}x{j}  "--c{i}x{j} " c   {POSSIBLE_CONDITIONS} | as.numeric(NumConnections{i})>{j}')
                grammar.append(
                    f'P{i}x{j}  "--p{i}x{j} " r   (0,1) | as.numeric(C{i}x{j}) %in% c(10,11,12,15,20,21,22,25,27,30,31,32,35,40,41,42,45,50,51,52,55)')
                grammar.append(
                    f'B{i}x{j}  "--b{i}x{j} " i   (1,10) | as.numeric(C{i}x{j}) %in% c(13,14,23,24,33,34,43,44,53,54)')
                grammar.append(
                    f'W{i}x{j}  "--w{i}x{j} " r   (0,20) | as.numeric(C{i}x{j}) %in% c(13,14,23,24,33,34,43,44,53,54)')
                grammar.append(f'L{i}x{j}  "--l{i}x{j} " c   (1,2,3,4,5,6) | as.numeric(C{i}x{j}) %in% c(27)')
        return grammar

    def generate_grammar_bt(self):
        grammar = ['RootNode   "--nroot "   c (3) | ARCH=="bt-config"']
        grammar.append(f'NumChildsRoot   "--nchildroot "   i (1,4) | ARCH=="bt-config"')
        for i in range(4):
            grammar.append(f'N{i}     "--n{i} "  c   (0) | as.numeric(NumChildsRoot)>{i}')
            grammar.append(f'NumChild{i}   "--nchild{i} "  c (2) | as.numeric(N{i})==0')
            grammar.append(f'N{i}0 "--n{i}0 " c (6) | as.numeric(N{i})==0')
            grammar.append(f'C{i}0 "--c{i}0 "  c {POSSIBLE_CONDITIONS} | as.numeric(N{i})==0')
            grammar.append(f'L{i}0  "--l{i}0 " c   (1,2,3,4,5,6) | as.numeric(C{i}0) %in% c(27)')
            grammar.append(
                f'P{i}0  "--p{i}0 " r   (0,1) | as.numeric(C{i}0) %in% c(10,11,12,15,20,21,22,25,27,30,31,32,35,40,41,42,45,50,51,52,55)')
            grammar.append(f'W{i}0  "--w{i}0 " r   (0,20) | as.numeric(C{i}0) %in% c(13,14,23,24,33,34,43,44,53,54)')
            grammar.append(f'B{i}0  "--n{i}0 " i   (1,10) | as.numeric(C{i}0) %in% c(13,14,23,24,33,34,43,44,53,54)')
            grammar.append(f'N{i}1 "--n{i}1 " c (5) | as.numeric(N{i})==0')
            grammar.append(f'A{i}1 "--a{i}1 "  c   {POSSIBLE_BEHAVIORS} | as.numeric(N{i})==0')
            grammar.append(f'RWM{i}1   "--rwm{i}1 "  i (1,100) | as.numeric(A{i}1) %in% c(10,20,30,32,33,34,35,40)')
            grammar.append(f'ATT{i}1   "--att{i}1 "  r (1,5) | as.numeric(A{i}1) %in% c(14,24,34,44)')
            grammar.append(f'REP{i}1   "--rep{i}1 "  r (1,5) | as.numeric(A{i}1) %in% c(15,25,35,45)')
            grammar.append(f'VEL{i}1   "--vel{i}1 "  c (1.0) | as.numeric(A{i}1) %in% c(28,29)')
            grammar.append(f'CLE{i}1   "--cle{i}1 "  c (0,4,5,6) | as.numeric(A{i}1) %in% c(20,21,24,25,28,29)')
            grammar.append(f'CLR{i}1   "--clr{i}1 "  c (1,2,3,4,5,6) | as.numeric(A{i}1) %in% c(28,29)')
            grammar.append(f'EXP{i}1   "--exp{i}1 "  c (0,1,2) | as.numeric(A{i}1) %in% c(30,32,33,34,35)')
            grammar.append(f'MU{i}1    "--mu{i}1 "   r (1,3) | as.numeric(A{i}1) %in% c(30,32,33,34,35)')
            grammar.append(f'RHO{i}1   "--rho{i}1 "  r (0,1) | as.numeric(A{i}1) %in% c(30,32,33,34,35)')
        return grammar

    def build_header(self):
        header = f'ARCH  "--"  c ("fsm-config", "bt-config")\n'
        if self.fsm and not self.bt:
            header = f'ARCH  "--"  c ("fsm-config")\n'
        if self.bt and not self.fsm:
            header = f'ARCH  "--"  c ("bt-config")\n'
        return header

    def generate_grammar(self, file_name):
        with open(file_name, "w") as grammar_file:
            # TODO: first line
            grammar_file.write(self.build_header())
            if self.fsm or not self.bt:
                fsm_lines = self.generate_grammar_fsm()
                for line in fsm_lines:
                    grammar_file.write(line)
                    grammar_file.write("\n")
            if self.bt or not self.fsm:
                bt_lines = self.generate_grammar_bt()
                for line in bt_lines:
                    grammar_file.write(line)
                    grammar_file.write("\n")
