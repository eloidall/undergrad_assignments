(* Question 1 *)

(* Set of tests for q1a_nat_of_int. *)
let q1a_nat_of_int_tests : (int * nat) list = [
  (0, Z);
  (1, (S Z) );
  (2, (S (S Z)) );
  (8, (S (S (S (S (S (S (S (S Z)))))))) );
  (15, (S (S (S (S (S (S (S (S (S (S (S (S (S (S (S Z))))))))))))))) )
]

(* q1a_nat_of_int: function that converts a type int to type nat *)
let q1a_nat_of_int (n : int) : nat = 
  let rec nat_of_int_helper n acc = 
    if n = 0 then 
      acc
    else
      nat_of_int_helper (n - 1) (S acc)
  in nat_of_int_helper n Z
  
(* Set of tests for q1b_int_of_nat *)
let q1b_int_of_nat_tests : (nat * int) list = [
  (Z, 0);
  ((S Z),1);
  ((S (S Z)), 2);
  ((S (S (S (S (S (S (S (S Z)))))))), 8);
  ((S (S (S (S (S (S (S (S (S (S (S (S (S (S (S Z))))))))))))))), 15)

]

(* q1b_int_of_nat: function that converts a type nat to type int *) 
let rec q1b_int_of_nat (n : nat) : int =
  match n with
  | Z -> 0
  | S n1 -> 1 + q1b_int_of_nat n1
                
  
(* Set of tests for q1c_add *)
let q1c_add_tests : ((nat * nat) * nat) list = [ 
  (* Test with 0 + 0 *)
  ( (Z, Z),
    Z );
  (* Tests with 0 in 1st place *)
  ( ( Z, S (S (Z)) ),
    S (S (Z)) ); 
  (* Tests with 0 in 2nd place *) 
  ( ( S (S (Z)), Z),
    S (S (Z)) ); 
  (* Tests with 3 + 4 *) 
  ( 
    ( 
      S( S ( S ( S(Z) ))),
      S ( S ( S(Z) ))
    ), 
    S ( S ( S ( S ( S ( S ( S(Z) ))))))
  )
]

(* q1c_add: function that takes 2 type nat values and return the result
in a type nat *)
let rec q1c_add (n : nat) (m : nat) : nat = 
  match m with
  | Z -> n
  | S m1 -> q1c_add (S n) m1
  
(* Question 2 *) 

(* q2a_neg: function that takes an expression and returns the negation of
the given expression *)
let q2a_neg (e : exp) : exp =
  Times ( Const (-1.0), e)
  
(* q2b_minus: takes 2 expressions and returns an expression representing the
subtraction of the first expression by the second expression *) 
let q2b_minus (e1 : exp) (e2 : exp) : exp =
  Plus (e1 , (q2a_neg e2) ) 

(* q2c_pow: takes an expression and a nat, and forms an expression
representating the expression raised to the power of the nat *) 
let rec q2c_pow (e1 : exp) (p : nat) : exp = 
  match p with
  | Z -> Const 1.0
  | S x1 -> Times (e1, q2c_pow e1 x1)

              
(* Question 3 *) 
(* Set of tests for eval *)
let eval_tests : ((float * exp) * float) list = [
  
  ( 
    (3.0, 
     Plus (
       Plus (
         Times (
           Const 2.0,
           Var
         ),
         Times (
           Const (-1.0),
           Div (Var, Const 3.0)
         )
       ),
       Const 10.0
     )
    ), 15.0
  );
  
  ( (0.0, Var), 0.0)
  
  
  
  
]

(* eval: evaluate an expression with a given value for the variable x *)
let rec eval (a : float) (e : exp) : float = 
  if a = 0.0 then a 
  else
    match e with
    | Const f -> f
    | Var -> a 
    | Plus (e1, e2) -> eval a e1 +. eval a e2
    | Times (e1, e2) -> eval a e1 *. eval a e2
    | Div (e1, e2) -> eval a e1 /. eval a e2
  

(* Question 4 *)

(* Set of tests for diff_tests *)
let diff_tests : (exp * exp) list = [
  ( Times (Const 3.0, Var), Const 3.0 );
  ( Times (Var, Var), Times (Const 2.0, Var) );
  ( Times (Const 2.0, Var), Const 2.0 )

]

(* diff: symbolically compute the derivative of the given expression 
representing a single-variable function *)
let rec diff (e : exp) : exp = 
  match e with
  | Const _ -> Const 0.0
  | Var -> Const 1.0
  | Plus (e1, e2) -> Plus (diff e1, diff e2)
  | Times (e1, e2) -> Plus (Times (diff e1, e2), Times (e1, diff e2))
  | Div (e1, e2) -> Div ((Plus(Times(diff e1, e2), q2a_neg(Times(e1, diff e2)))), Times(e2, e2)) 

                      

