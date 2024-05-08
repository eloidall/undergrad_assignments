(* Question 1: Tree Depth *)
(* TODO: Write a good set of tests for testing your tree depth function. *)
(* For the whole assignment, you only need to write tests for `int tree`s
   etc. However, your functions must still be suitably polymorphic, and the
   grader will check this. *)
let tree_depth_cps_test_cases : (int tree * int) list = [ 
  (Empty, 0); 
  (Tree (Empty, 2, Empty), 1); 
  (Tree (Tree (Empty, 2, Empty), 1, Tree (Empty, 3, Empty)) , 2); 
  (Tree (Tree (Tree (Empty, 4, Empty), 2, Tree (Empty, 5, Empty)),
         1, Tree (Empty, 3, Empty)) , 3); 
];;

(* These are the test cases that will actually be graded, but
   you don't have to modify this. Remember that you only need
   to test with the `id` continuation. `insert_test_continuations`
   (defined in the prelude) adds the `id` continuation to each of
   your test cases. *)
let tree_depth_cps_tests : ((int tree * (int -> int)) * int) list =
  insert_test_continuations tree_depth_cps_test_cases

(* An example of Non-CPS function to find depth of a tree: *)
let rec tree_depth t =
  match t with
  | Empty -> 0
  | Tree (l, _, r) -> 1 + max (tree_depth l) (tree_depth r)

(* TODO: Implement a CPS style tree_depth_cps function.*)
let rec tree_depth_cps (t : 'a tree) (return : int -> 'r) : 'r =
  match t with 
  | Empty -> return 0
  | Tree (l, _, r) -> 
      tree_depth_cps l (fun depth_l ->
          tree_depth_cps r (fun depth_r ->
              maxk (depth_l + 1) (depth_r + 1) return))
  
(* Question 2(a): Tree Traversal *)
(* TODO: Write a good set of tests for testing your tree traversal function. *)
let traverse_cps_test_cases : (int tree * int list) list = [ 
  (Tree (Tree (Empty, 2, Empty), 1, Tree (Empty, 3, Empty)), [1; 2; 3]);
  
  (Tree (Tree (Tree (Empty, 4, Empty), 2, Tree (Empty, 5, Empty)), 1,
         Tree (Empty, 3, Empty)), [1; 2; 4; 5; 3]); 
];;


let traverse_cps_tests : ((int tree * (int list -> int list)) * int list) list =
  insert_test_continuations traverse_cps_test_cases

(* TODO: Implement a CPS style preorder traversal function. *)
let rec traverse_cps (t : 'a tree) (return : 'a list -> 'r) : 'r = 
  match t with
  | Empty -> return []
  | Tree (l, v, r) -> 
      traverse_cps l (fun left_list ->
          traverse_cps r (fun right_list ->
              return (v :: left_list @ right_list)))

        
(* Question 2(b): Max Elements in a Tree *)
(* TODO: Write a good set of tests for testing your tree maximum function. *)
let tree_max_cps_test_cases : (int tree * int) list = [ 
  ((Tree (Tree (Empty, 3, Empty), 5, Tree (Empty, 6, Empty))), 6); 
  ((Tree (Tree (Empty, 2, Tree (Empty, 6, Empty)), 3, Tree (Empty, 4, Empty))), 6); 
  (Empty, -1); 
];;

let tree_max_cps_tests : ((int tree * (int -> int)) * int) list =
  insert_test_continuations tree_max_cps_test_cases

(* TODO: Implement a CPS style tree maximum function. *) 
let rec tree_max_cps (t : int tree) (return : int -> 'r) : 'r = 
  match t with
  | Empty -> return (-1)
  | Tree (l, v, r) -> 
      tree_max_cps l (fun max_l ->
          tree_max_cps r (fun max_r ->
              maxk v max_l (fun max_l_v ->
                  maxk max_l_v max_r return)))

        
(* Question 3: Finding Subtrees *)
(* TODO: Write a good set of tests for your finding subtrees function. *)
(* This time we have two continuations.
   `insert_test_option_continuations` will automatically
   insert the trivial continuations for testing:
   fun x -> Some x, and fun () -> None. *)
let find_subtree_cps_test_cases
  : ((int list * int tree) * int tree option) list = [ 
  (([], (Tree (Tree (Empty, 3, Empty), 5, Tree (Empty, 6, Empty)))), 
   Some (Tree (Tree (Empty, 3, Empty), 5, Tree (Empty, 6, Empty))));

  (([1;7;6], Empty), None);
    
  (([1], (Tree (Tree (Empty, 2, Empty), 1, Tree (Empty, 3, Empty)))), Some (Tree (Empty, 2, Empty)));
  
  (([5;6], (Tree (Tree (Empty, 3, Empty), 5, Tree (Empty, 6, Empty)))), 
   Some (Empty)); 
  
  (([1], (Tree (Tree (Empty, 1, Empty), 1, Tree (Empty, 1, Empty)))), Some (Tree (Empty, 1, Empty))); 
  
  (([1;2;4], (Tree (Tree (Empty, 2, Empty), 1, Tree (Empty, 3, Empty)))), None);
    
  (([1;4], (Tree (Tree (Empty, 2, Empty), 1, Tree (Empty, 3, Empty)))), None) 
];;

let find_subtree_cps_tests =
  insert_test_option_continuations find_subtree_cps_test_cases

(* TODO: Implement a CPS style finding subtrees function.*) 
let rec find_subtree_cps (ps : 'a list) (t : 'a tree)
    (succeed : 'a tree -> 'r) (fail : unit -> 'r) : 'r = 
  match ps, t with
  | [], _ -> succeed t
  | _, Empty -> fail ()
  | p :: ps', Tree (l, x, r) ->
      if p = x then
        find_subtree_cps ps' l succeed (fun () -> find_subtree_cps ps' r succeed fail)
      else
        find_subtree_cps ps l succeed (fun () -> find_subtree_cps ps r succeed fail)



