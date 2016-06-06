# HW3: `z3` SMT Solver & Basic Program Verification
## 0. Authorship
- Author: [Seokju Hong](https://github.com/suckzoo)
- Student ID: 20130711

## 1. `z3` puzzle

### Question 1
- Datatype `crateState`: `realApple`, `realOrange`, `realMixed`
- Declared const crate1, 2, 3, and label1, 2, 3.
- Every crate has distinct item. Therefore I asserted distinct condition.
- Every label has distinct text. Therefore I asserted distinct condition.
- Every box's item is different from its label.
- There was an apple in `realMixed` box.
- This concludes that `realMixed` box has `realApple`.
- With `z3`, we could prove that there exists a combination of items.
  - `realMixed` box has `realApple`
  - `realOrange` box has `realMixed`
  - `realApple` box has `realOrange`

### Question 2
- Asserted same condition with Question 1.
- There was an apple in `realMixed` box.
- This concludes that `realMixed` box has `realApple`.
- We declared additional consts: `crate1p`, `crate2p`, `crate3p`.
- They are crates of parallel universe, whose item is different from `crate1`,
`crate2`, and `crate3`.
- If such parallel universe exists, `crate1 != crate1p` or `crate2 != crate2p` 
or `crate3 != crate3p` must be satisfied.
- With `z3`, we could prove that there does not exist another combination of
 items.
- Therefore we could conclude that there is an unique possible combination.

### Question 3
- Asserted same condition with Question 1.
- There was an apple in `realOrange` box.
- Two possible cases exist: `realOrange` has `realMixed`, or `realOrange` has
`realApple`.
- We declared additional consts: `crate1p`, `crate2p`, `crate3p`.
- They are crates of parallel universe, whose item is different from `crate1`,
`crate2`, and `crate3`.
- If such parallel universe exists, `crate1 != crate1p` or `crate2 != crate2p` 
or `crate3 != crate3p` must be satisfied.
- With `z3`, we could prove that there exists another combination of items.
- Therefore, we could conclude that not enough information is provided.

## 2. Program Verification

- Environment: OS X El Capitan
- Language: Python 2.7.x
- Dependencies: Java 1.7, z3 site packages.

### Usage
The `source_file` must have extension `.java`.
```
python verifier.py <source_file>
```
When the result is valid, the program will print `VALID`. Otherwise, it will
print `INVALID` and the list of arguments which make assertions invalid.

### Validity check
- If an assertion is valid,
  - The code is unsatisfiable when the control flow reaches `throw` statement.
- If an assertion is invalid,
  - There exists a satisfiable control flow which reaches `throw` statement.
- I hashed every labels to dictionary before the main algorithm begins.
- There is no `for-loop` or `while-loop`. So we can assume the control flow
graph is DAG.
- I concerned every line of code as a node, and constructed edge to the next
 line.
- If a line of code contains `if` or `goto` statement, I created another 
edge which reaches its destination label.
- After control flow graph is contructed, traversed the graph recursively
and added assertion when I meet `if` statement or expressions.
- If `throw` statement is encountered, I check the model with `z3` whether the
model is satisfiable or not.
- If it is satisfiable, then the assertion is not valid.

### Nested `if` Branch and Boolean Predicate Assertions
- Soot creates many `goto`s and labels when there is nested branch or predicate
assertions.
- As I did in the first task, I could easily prove whether the assertion is
valid or not.
- I passed `phi` value to the recursive graph traversing function. And if I
encounter Phi expression, I used the `phi` value I've passed before.

