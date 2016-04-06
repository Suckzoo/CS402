# HW2: CNF and Satisfiability
---
## 0. Authorship
- Author: [Seokju Hong](https://github.com/suckzoo)
- Student ID: 20130711

## 1. Conjunctive Normal Form

- Environment: OS X El Capitan
- Language: Python 2.7.x
- Dependencies: No dependencies at all.

### 구현 순서
1. 우선 주어진 polish notation을 parse하여 syntax tree를 만들었습니다.
2. 만들어진 syntax tree를 탐색하고, <, >, =를 |와 -를 이용하여 implication을
모두 eliminate 하여 다시 새로운 syntax tree를 만들었습니다.
3. 만들어진 impl-free form을 NNF로 만들었습니다.
4. 만들어진 NNF를 distr 함수를 이용하여 CNF로 만들었습니다.
5. 만들어진 CNF의 불필요한 괄호를 제거하였습니다.
6. CNF의 disjunction of literals D 별로 모두 Valid한지 체크했습니다.
7. Validity는 D 안에 -x와 x가 모두 들어있는 x가 존재하는지를 체크했습니다.

### 실행 방법
```shell
./cnf [formula]
```
\[formula\] 입력시 원래 <, >는 redirection, |는 pipe, &는 background execute의 
기능을 갖고있으므로 \\문자를 이용한 escape가 필요합니다.


## 2. Nonogram

- Environment: OS X El Capitan
- Language: Python 2.7.x
- Dependencies: No dependencies at all other than minisat.

### Instance
- n: # of rows
- m: # of cols

### Terminology
- 격자: nonogram board의 한 칸을 의미
  - 칠해짐: 격자에 #을 채워넣음.
  - 칠하지 않음: 격자에 .을 채워넣음.
- 규칙: 해당 row(column)에서 몇 개의 연속된 격자가 칠해지는지 나타내는 숫자. 
  - 규칙 r이 k에서 사용됨: [k, k+r)에 #을 채워넣음.

### Assigned literals
- 1-n\*m번 literal은 격자의 각 칸이 칠해지는지 여부를 나타는 literal입니다.
  - k번 literal은 ((k-1)/m, (k-1)%m)에 매칭됩니다.
- 그 외의 literal은 연속된 #이 어디에 놓일 것인지를 나타내는 literal입니다.
  - 예시: m=6, 규칙=2 -> 5 literals available!
    - ##....
    - .##...
    - ..##..
    - ...##.
    - ....##

### Clauses
- p\>q == -p|q임을 이용했다.
- \[격자\] \> \[규칙\]
  1. 이 격자가 칠해지면 이 격자를 사용하는 규칙들이 available하다는 implication
- \[규칙\] \> \[격자\]
  1. 규칙 r이 k에서 사용된다면 [r, r+k)에 있는 해당 격자가 반드시 칠해진다는
     implication
- \[규칙\] \> -\[격자\]
  1. 규칙 r이 k에서 사용된다면 r-1, r+k는 반드시 칠해지지 않는다는 implication
- \[규칙\] (| \[규칙\])+
  1. 해당 규칙은 어떤 위치에서든 반드시 한 번 이상 일어나야 한다는 implication
- \[규칙\] \> -\[규칙\]
  1. 어떤 위치에서 규칙이 사용된다면 다른 위치에서 해당 규칙은 절대로
     사용될 수 없다는 implication
- \[격자\]
  1. 모든 규칙이 어떤 격자를 칠하여, 그 격자는 칠할 수 밖에 없는 경우.
- -\[격자\]
  1. 모든 규칙이 어떤 격자를 칠하지 않아, 그 격자는 칠하지 않을 수 밖에 없는
     경우

### 실행하기
1. cwd 파일을 작성합니다.
2. 다음 command를 통해 실행합니다.
```shell
./nonogram
```

