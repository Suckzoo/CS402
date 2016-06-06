import sys, os
import shutil
import re
from z3 import *

class InvalidException(Exception):
    def __init__(self, msg):
        self.msg = msg

class Node(object):
    def __init__(self, l_number):
        self.l_number = l_number
        self.edge = []

    def push_edge(self, condition, next_line):
        self.edge.append((condition, next_line))
    
class Pattern:
    ptn_declare = re.compile('(int .*;|byte .*;)')
    ptn_label = re.compile('^label[0-9]+:$')
    ptn_branch = re.compile('if .* goto')
    ptn_throw = re.compile('throw .*')
    ptn_testme = re.compile('public void testMe\(int(, int)*\)')
    ptn_goto = re.compile('^goto .*')
    ptn_expression = re.compile('[\$A-Za-z0-9]+ = .*')

class ShimpleInstance(object):

    def __init__(self, path):
        self.path = path
        self.generate_shimple()
        self.variables = {}
        self.labels = {}
        self.flow_graph = {}
        self.validity = True
        self.root = None

    def generate_shimple(self):
        if self.path.find('.java') == -1:
            raise
        self.file_name = self.path.split('/')[-1].split('.java')[0]
        shutil.copyfile(self.path, self.file_name + '.java')
        os.system('javac ' + self.file_name + '.java')
        os.system('./soot.sh ' + self.file_name)

    def cleanup_shimple(self):
        os.remove('./%s.java' % self.file_name)
        os.remove('./%s.class' % self.file_name)
        os.remove('./%s.shimple' % self.file_name)

    def declare_token(self, x):
        self.variables[x] = Int(x)

    def add_expression(self, expr, negation = False):
        def __wrap_variables(match):
            return 'self.variables[\'%s\']' % match.group(0)
        sub_expr = re.sub(r'[\$A-Za-z][\$A-Za-z0-9]+', __wrap_variables, expr)
        if negation:
            sub_expr = 'Not(' + sub_expr + ')'
        sub_expr = 'self.solver.add(' + sub_expr + ')'
        try:
            eval(sub_expr)
        except:
            return False
        return True

    def interpret(self):
        self.solver = Solver()
        def __dfs__(node):
            line = self.code[node.l_number]
            print '(%d) %s' % (node.l_number, line)
            if Pattern.ptn_declare.search(line):
                tokens = None
                if line[:3] == 'int':
                    tokens = line[4:-1].split(', ')
                else:
                    tokens = line[5:-1].split(', ')
                for x in tokens:
                    self.declare_token(x)
            elif Pattern.ptn_expression.search(line):
                self.add_expression(line.replace('=', '==')[:-1])
            elif Pattern.ptn_throw.search(line):
                if self.solver.check() == sat:
                    raise InvalidException(self.solver.model())
            for edge in node.edge:
                if edge[0]:
                    self.solver.push()
                    if self.add_expression(edge[0]):
                        __dfs__(self.flow_graph[edge[1]])
                    self.solver.pop()
                    self.add_expression(edge[0], True)
                __dfs__(self.flow_graph[edge[1]])

        __dfs__(self.root)

    def get_labels(self):
        test_me = 0
        for number, line in enumerate(self.code):
            if not test_me:
                if Pattern.ptn_testme.search(line):
                    test_me = 1
            else:
                if line == '}':
                    break
                elif Pattern.ptn_label.search(line):
                    self.labels[line[:-1]] = number

    def construct_graph(self):
        test_me = 0
        for number, line in enumerate(self.code):
            if not test_me:
                if Pattern.ptn_testme.search(line):
                    test_me = 1
            elif test_me == 1:
                if not self.root:
                    self.root = Node(number)
                    current_node = self.root
                else:
                    current_node = Node(number)
                self.flow_graph[number] = current_node
                if line == '}':
                    break
                elif Pattern.ptn_branch.search(line):
                    condition = line.split('if')[1].split('goto')[0].strip()
                    l_number = self.labels[line.split('goto')[1][:-1].strip()]
                    current_node.push_edge(condition, l_number + 1)
                elif Pattern.ptn_goto.search(line):
                    l_number = self.labels[line[5:-1]]
                    current_node.push_edge(None, l_number + 1)
                    continue
                current_node.push_edge(None, number + 1)

    def scan(self):
        shimple_file = open(self.file_name + '.shimple')
        lines = shimple_file.readlines()
        self.code = [x.strip() for x in lines]
        self.get_labels()
        self.construct_graph()
        shimple_file.close()


def main():
    instance = ShimpleInstance(sys.argv[1])
    instance.scan()
    instance.interpret()
    # instnace.cleanup_shimple()

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise
        main()
        print 'VALID'
    except InvalidException as e:
        print 'INVALID'
        print e.msg
    # except:
    #     print 'Usage: python verifier.py <file_name>.java'

