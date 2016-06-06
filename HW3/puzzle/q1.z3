; available types
(declare-datatypes () ((crateState realApple realOrange realMixed)))

; crates
(declare-const crate1 crateState)
(declare-const crate2 crateState)
(declare-const crate3 crateState)
(assert (distinct crate1 crate2 crate3))

; crate labels
(declare-const label1 crateState)
(declare-const label2 crateState)
(declare-const label3 crateState)

; distinct crate conditions
(assert (distinct label1 label2 label3))

; wrong-labeling conditions
(assert (not (= crate1 label1)))
(assert (not (= crate2 label2)))
(assert (not (= crate3 label3)))

; crate1 was apple and labeled as mixed
(assert (= crate1 realApple))
(assert (= label1 realMixed))
(check-sat)
(get-model)
