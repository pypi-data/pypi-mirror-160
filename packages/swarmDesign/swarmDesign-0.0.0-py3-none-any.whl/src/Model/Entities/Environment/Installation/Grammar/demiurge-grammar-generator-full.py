POSSIBLE_BEHAVIORS = "(10,11,12,13,14,15,20,21,24,25,28,29,30,31,32,33,34,35,40,41,42,43,44,45,50,51,52,53,54,55)"
POSSIBLE_CONDITIONS = "(10,11,12,13,14,15,20,21,22,23,24,25,27,30,31,32,33,34,35,40,41,42,43,44,45,50,51,52,53,54,55)"


def generate_grammar_fsm():
    grammar = ['NumStates  "--nstates "   i (1,4)  | ARCH=="fsm-config"']   # first line
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
            grammar.append(f'P{i}x{j}  "--p{i}x{j} " r   (0,1) | as.numeric(C{i}x{j}) %in% c(10,11,12,15,20,21,22,25,27,30,31,32,35,40,41,42,45,50,51,52,55)')
            grammar.append(f'B{i}x{j}  "--b{i}x{j} " i   (1,10) | as.numeric(C{i}x{j}) %in% c(13,14,23,24,33,34,43,44,53,54)')
            grammar.append(f'W{i}x{j}  "--w{i}x{j} " r   (0,20) | as.numeric(C{i}x{j}) %in% c(13,14,23,24,33,34,43,44,53,54)')
            grammar.append(f'L{i}x{j}  "--l{i}x{j} " c   (1,2,3,4,5,6) | as.numeric(C{i}x{j}) %in% c(27)')
    return grammar



def generate_grammar_bt():
    grammar = ['RootNode   "--nroot "   c (3) | ARCH=="bt-config"']
    grammar.append(f'NumChildsRoot   "--nchildroot "   i (1,4) | ARCH=="bt-config"')
    for i in range(4):
        grammar.append(f'N{i}     "--n{i} "  c   (0) | as.numeric(NumChildsRoot)>{i}')
        grammar.append(f'NumChild{i}   "--nchild{i} "  c (2) | as.numeric(N{i})==0')
        grammar.append(f'N{i}0 "--n{i}0 " c (6) | as.numeric(N{i})==0')
        grammar.append(f'C{i}0 "--c{i}0 "  c {POSSIBLE_CONDITIONS} | as.numeric(N{i})==0')
        grammar.append(f'P{i}0  "--p{i}0 " r   (0,1) | as.numeric(C{i}0) %in% c(10,11,12,15,20,21,22,25,27,30,31,32,35,40,41,42,45,50,51,52,55)')
        grammar.append(f'B{i}0  "--b{i}0 " i   (1,10) | as.numeric(C{i}0) %in% c(13,14,23,24,33,34,43,44,53,54)')
        grammar.append(f'W{i}0  "--w{i}0 " r   (0,20) | as.numeric(C{i}0) %in% c(13,14,23,24,33,34,43,44,53,54)')
        grammar.append(f'L{i}0  "--l{i}0 " c   (1,2,3,4,5,6) | as.numeric(C{i}0) %in% c(27)')
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


def generate_grammar(file_name):
    with open(file_name, "w") as grammar_file:
        # TODO: first line
        grammar_file.write(f'ARCH  "--"  c ("fsm-config", "bt-config")\n')
        fsm_lines = generate_grammar_fsm()
        for line in fsm_lines:
            grammar_file.write(line)
            grammar_file.write("\n")
        bt_lines = generate_grammar_bt()
        for line in bt_lines:
            grammar_file.write(line)
            grammar_file.write("\n")


if __name__ == "__main__":
    generate_grammar("grammar-demiurge.txt")
