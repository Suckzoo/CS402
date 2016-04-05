import sys
import copy
import re

handler = {}

class Node(object):
    def __init__(self, symbol, child1=None, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

def and_handler(index, size, polish):
    left_child = impl_free(index + 1, size, polish)
    right_child = impl_free(index + left_child[0] + 1, size, polish)
    node = Node('&', left_child[1], right_child[1])
    return (right_child[0], node)

def or_handler(index, size, polish):
    left_child = impl_free(index + 1, size, polish)
    right_child = impl_free(index + left_child[0] + 1, size, polish)
    node = Node('|', left_child[1], right_child[1])
    return (right_child[0], node)

def neg_handler(index, size, polish):
    left_child = impl_free(index + 1, size, polish)
    node = Node('-', left_child[1])
    return (left_child[0], node)

def rarrow_handler(index, size, polish):
    left_child = impl_free(index + 1, size, polish)
    right_child = impl_free(index + left_child[0] + 1, size, polish)
    left_wrapper = Node('-', left_child[1])
    node = Node('|', left_wrapper, right_child[1])
    return (right_child[0], node)

def larrow_handler(index, size, polish):
    left_child = impl_free(index + 1, size, polish)
    right_child = impl_free(index + left_child[0] + 1, size, polish)
    right_wrapper = Node('-', right_child[1])
    node = Node('|', left_child[1], right_wrapper)
    return (right_child[0], node)

def lrarrow_handler(index, size, polish):
    left_child = impl_free(index + 1, size, polish)
    right_child = impl_free(index + left_child[0] + 1, size, polish)
    left_neg = Node('-', left_child[1])
    right_neg = Node('-', right_child[1])
    left_wrapper = Node('|', left_neg, right_child[1])
    right_wrapper = Node('|', left_child[1], right_neg)
    node = Node('&', left_wrapper, right_wrapper)
    return (right_child[0], node)

def map_operator():
    handler['&'] = and_handler
    handler['|'] = or_handler
    handler['-'] = neg_handler
    handler['>'] = rarrow_handler
    handler['<'] = larrow_handler
    handler['='] = lrarrow_handler

def impl_free(index, size, polish):
    if bool(re.match('[A-Za-z0-9]+', polish[index])):
        node = Node(polish[index])
        return (node, index)
    return handler[polish[index]](index, size, polish)

def generate_nnf(head):
    node = None
    if head.symbol == '&':
        left_cnf = generate_nnf(head.child1)
        right_cnf = generate_nnf(head.child2)
        node = Node('&', left_cnf, right_cnf)
    elif head.symbol == '|':
        left_cnf = generate_nnf(head.child1)
        right_cnf = generate_nnf(head.child2)
        node = Node('|', left_cnf, right_cnf)
    elif head.symbol == '-':
        child = head.child1
        if child.symbol == '&':
            wrap_left = generate_nnf(Node('-', child.child1))
            wrap_right = generate_nnf(Node('-', child.child2))
            node = Node('|', wrap_left, wrap_right)
        elif child.symbol == '|':
            wrap_left = generate_nnf(Node('-', child.child1))
            wrap_right = generate_nnf(Node('-', child.child2))
            node = Node('&', wrap_left, wrap_right)
        elif child.symbol == '-':
            node = generate_nnf(child.child1)
        else:
            child_nnf = genertate_nnf(child)
            node = Node('-', child_nnf)
    else:
        node = Node(head.symbol)
    return node

def generate_cnf(head):
    pass

def main():
    n = sys.argc
    polish_notation = copy.deepcopy(sys.argv)
    map_operator()
    size, root = impl_free(0, n, polish_notation)
    nnf_root = generate_nnf(root)
    cnf_root = generate_cnf(nnf_root)

if __name__ == '__main__':
    main()


