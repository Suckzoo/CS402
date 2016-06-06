; available types
(declare-datatypes () ((crateState realApple realOrange realMixed)))

; distinct crates
(declare-const crate1 crateState)
(declare-const crate2 crateState)
(declare-const crate3 crateState)
(assert (distinct crate1 crate2 crate3))

; distinct crate labels
(declare-const label1 crateState)
(declare-const label2 crateState)
(declare-const label3 crateState)
(assert (distinct label1 label2 label3))

; wrong-labeling conditions
(assert (not (= crate1 label1)))
(assert (not (= crate2 label2)))
(assert (not (= crate3 label3)))

; crate1 was labeled as orange, but picked apple.
; when we pick apple, there are two cases: picked realApple, or picked realMixed.
(assert (or (= crate1 realMixed) (= crate1 realApple)))
(assert (= label1 realOrange))

; if another solution exists, crate2 or crate3 will be different
; from its original assigned state.
; create crate1p crate2p crate3p variable for our parallel universe!
(declare-const crate1p crateState)
(declare-const crate2p crateState)
(declare-const crate3p crateState)

; crate1p was labeled as orange, but picked apple.
; when we pick apple, there are two cases: picked realApple, or picked realMixed.
(assert (or (= crate1p realMixed) (= crate1p realApple)))

; distinct crate conditions
(assert (distinct crate1p crate2p crate3p))

; wrong-labeling conditions
(assert (not (= crate2p label2)))
(assert (not (= crate3p label3)))

; parallel-universe conditions
(assert (not (and (= crate1p crate1) (= crate2p crate2) (= crate3p crate3))))

(check-sat)
(get-model)
