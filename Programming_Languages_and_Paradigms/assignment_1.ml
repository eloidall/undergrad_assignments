(* Question 1: Manhattan Distance *)
(* TODO: Write a good set of tests for distance. *)
let distance_tests = [ 
  
    (* input: two inputs, each a pair, so we have a pair of pairs *)
    (* output: the distance between (0,0) and (0,0) is 0 *)
    (* end each case with a semicolon *)
  ( ((0, 0), (0, 0)), 0);
  
    (* Your test cases go here *)
  ( ((1, 0), (0, 0)), 1); 
  ( ((3, 2), (1, 0)), 4);

  (* Distances should always be non-negative *)
  ( ((3, 1), (1, 6)), 7);
  ( ((1, 1), (5, 5)), 8);
  ( ((-1, 1), (5, -5)), 12);


  (* Symmetric distances should be equal *)
  ( ((1, 1), (0, 0)), 2);
  ( ((0, 0), (1, 1)), 2);
  
]
;;

(* TODO: Correct this implementation so that it compiles and returns
         the correct answers. *)
let distance (x1, y1) (x2, y2) = 
  abs(x1 - x2) + abs(y1 - y2)




(* Question 2: Binomial *)
(* TODO: Write your own tests for the binomial function.
         See the provided test for how to write test cases.
         Remember that we assume that  n >= k >= 0; you should not write test cases where this assumption is violated.
*)
let binomial_tests = [
  (* Your test cases go here. Correct this incorrect test case for the function. *)
  ((0, 0), 1);
  ((1, 0), 1);
  ((1, 1), 1);
  ((2, 1), 2);
  ((2, 2), 1); 
]

(* TODO: Correct this implementation so that it compiles and returns
         the correct answers.*) 
let binomial n k = 
  (* Tail-recursive inner helper-function *) 
  let factorial (n : int) : int = 
    let rec go acc n =
      if n = 0 then acc
      else go (n * acc) (n - 1)
    in go 1 n
  in 
  factorial n / ( factorial k * factorial (n - k) )
      

(* Question 3: Lucas Numbers *)

(* TODO: Write a good set of tests for lucas_tests. *)
let lucas_tests = [ 
  (0, 2);
  (1, 1);
  (2, 3);
  (3, 4);
  (4, 7);
  (5, 11);
  (6, 18);
  (7, 29);
  (8, 47);
  (9, 76);
  (10, 123);
]

(* TODO: Implement a tail-recursive helper lucas_helper. *) 
let rec lucas_helper prev1 prev2 n =
  if n = 0 then prev1
  else if n = 1 then prev2
  else
    lucas_helper prev2 (prev1 + prev2) (n - 1) 

(* TODO: Implement lucas by calling lucas_helper. *) 
let lucas = 
  lucas_helper 2 1

    


