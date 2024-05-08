Author: Éloi Dallaire

# HW7: Induction

## Question 1: Induction on lists

### Question 1.a

Prove that 
If `a,acc : int` and `ls : int list`, then
`a + sum_tr ls acc = sum_tr ls (a + acc)`

Proof.
Induction on ls.

CASE: ls = []
  WTS: a + sum_tr [] acc = sum_tr [] (a + acc)

  LHS: a + sum_tr [] acc
     = a + acc					-- definition of sum_tr

  RHS: sum_tr [] (a + acc)
     = a + acc					-- definition of sum_tr
     = LHS


CASE: ls = x :: xs
  WTS: a + sum_tr (x :: xs) acc = sum_tr (x :: xs) (a + acc)
  IH: a + sum_tr xs (acc) = sum_tr xs (a + acc)

  LHS: a + sum_tr (x :: xs) acc
     = a + sum_tr xs (x + acc)			-- definition of sum_tr
     = sum_tr xs (x + a + acc) 			-- IH
  
  RHS: sum_tr (x :: xs) (a + acc)
     = sum_tr xs (x + a + acc)			-- definiton of sum_tr
     = LHS


QED.



### Question 1.b

Prove that
If `l1,l2 : int list` and `acc : int` then
`sum_tr (l1 @ l2) acc = sum_tr l1 (sum_tr l2 acc)`


Proof.
Induction on l1.

CASE: l1 = []
  WTS: sum_tr ([] @ l2) acc = sum_tr [] (sum_tr l2 acc)

  LHS: sum_tr ([] @ l2) acc
     = sum_tr (l2) acc				-- definition of @

  RHS: sum_tr [] (sum_tr l2 acc)
     = sum_tr l2 acc				-- definition of sum_tr
     = LHS

CASE: l1 = x :: xs
  WTS: sum_tr ( (x :: xs) @ l2 ) acc = sum_tr (x :: xs) (sum_tr l2 acc)
  IH: sum_tr (xs @ l2) acc = sum_tr xs (sum_tr l2 acc)

  RHS: sum_tr (x :: xs) (sum_tr l2 acc)
     = sum_tr xs (x + sum_tr l2 acc)		-- definiton of sum_tr
     = sum_tr xs ( sum_tr l2 (x + acc) ) 	-- Theorem 1
     = sum_tr (xs @ l2) (x + acc)		-- IH

  LHS: sum_tr ( (x :: xs) @ l2 ) acc
     = sum_tr ( x :: (xs @ l2) ) acc		-- definition of @
     = sum_tr (xs @ l2) (x + acc)		-- definiton of sum_tr
     = RHS

QED.


### Question 1.c

Prove that
If `ls : int list` and `acc : int` then
`acc + sum ls = sum_tr (rev ls) acc`

Proof.
Induction on ls.

CASE: ls = []
  WTS: acc + sum [] = sum_tr (rev []) acc

  LHS: acc + sum []
     = acc + 0					-- definiton of sum
     = acc

  RHS: sum_tr (rev []) acc
     = sum_tr [] acc				-- definition of rev
     = acc					-- definition of sum_tr
     = LHS

CASE: ls = x :: xs
  WTS: acc + sum (x :: xs) = sum_tr ( rev (x :: xs) ) acc
  IH: acc + sum xs = sum_tr (rev xs) acc

  RHS: sum_tr ( rev (x :: xs) ) acc
     = sum_tr (rev xs @ [x]) acc		-- definition of rev
     = sum_tr (rev xs) (sum_tr [x] acc) 	-- Theorem 2
     = sum_tr (rev xs) (sum_tr (x :: []) acc)	-- rewriting [x]
     = sum_tr (rev xs) ( sum_tr [] (x + acc) )	-- definition of sum_tr
     = sum_tr (rev xs) (x + acc) 		-- definition of sum_tr
     = x + sum_tr (rev xs) acc			-- Theorem 1
     = x + (acc + sum xs)			-- IH

  LHS: acc + sum (x :: xs)
     = acc + x + sum xs				-- definition of sum
     = x + acc + sum xs				-- associativity
     = RHS

QED.


## Question 2

Prove that 
If `t : tree` then `height t = height' t`

Lemma 1: if a, b, x: int then x + (max a b) = max (a + x) (b + x) 

Proof.
Induction on t.

CASE: t = Empty
  WTS: height Empty = height' Empty

  LHS: height Empty
     = 0					-- definition height

  RHS: height' Empty
     = 0					-- definition height'
     = LHS


CASE: t = Node (t1, t2)
  WTS: height ( Node (t1, t2) ) = height' ( Node (t1, t2) )
  IH1: height t1 = height' t1
  IH2: height t2 = height' t2

  LHS: height ( Node (t1, t2) )
     = 1 + max (height t1) (height t2)		-- definiton height
     = 1 + max (height' t1) (height' t2) 	-- IH1 & IH2

  RHS: height' ( Node (t1, t2) )
     = max (height' t1 + 1) (height' t2 + 1)	-- definition height'
     = 1 + max (height' t1) (height' t2)	-- Lemma 1
     = LHS

QED.



## Question 3

Prove that
If `t : int tree` then

Goal: inorder_traversal_1 t = inorder_traversal_2 t []

Lemma 2: inorder_traversal_1 t @ acc = inorder_traversal_2 t acc

Proof.
Induction on t.

CASE: t = Empty
  WTS: inorder_traversal_1 Empty @ acc = inorder_traversal_2 Empty acc

  LHS: inorder_traversal_1 Empty @ acc
     = [] @ acc					-- definition of inorder_traversal_1
     = acc					-- definition of @

  RHS: inorder_traversal_2 Empty acc
     = acc					-- definition of inorder_traversal_2
     = LHS


CASE: t = Node (t1, x, t2)
  WTS: inorder_traversal_1 Node (t1, x, t2) @ acc = inorder_traversal_2 ( Node (t1, x, t2) ) acc
  IH1: for any acc, inorder_traversal_1 t1 @ acc = inorder_traversal_2 t1 acc
  IH2: for any acc, inorder_traversal_1 t2 @ acc = inorder_traversal_2 t2 acc

  LHS: inorder_traversal_1 Node (t1, x, t2) @ acc
     = (inorder_traversal_1 t1) @ [x] @ (inorder_traversal_1 t2) @ acc 	-- definition of inorder_traversal_1
  
  RHS: inorder_traversal_2 ( Node (t1, x, t2) ) acc
     = inorder_traversal_2 t1 ( x :: (inorder_traversal_2 t2 acc) )		-- definition of inorder_traversal_2
     = inorder_traversal_1 t1 @ ( x :: (inorder_traversal_2 t2 acc) )		-- IH1 with acc:= ( x :: (inorder_traversal_2 t2 acc) )
     = inorder_traversal_1 t1 @ ( x :: (in_order_traversal_1 t2 @ acc) )	-- IH2 with acc:= acc
     = inorder_traversal_1 t1 @ ( [x] @ (inorder_traversal_1 t2 @ acc) )	-- rewriting last term
     = (inorder_traversal_1 t1) @ [x] @ (inorder_traversal_1 t2) @ acc		-- associativity of @
     = LHS

QED.
