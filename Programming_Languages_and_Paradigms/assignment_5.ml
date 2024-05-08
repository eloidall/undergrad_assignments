(* Question 1 : partition an int list into two lists of equal sum *)
(* TODO: test cases *) 
let partition_option_tests : (int list * (int list * int list) option) list = [ 
  ([], Some ([], [])); (* Empty list, valid partition *)
  ([1; 2; 3; 4; 5], None); (* No valid partition *) 
]


let partition (ns : int list) : (int list * int list) =
  let rec find_partition sum1 sum2 remaining_list =
    match remaining_list with
    | [] -> if sum1 = sum2 then ([], [])
        else raise NoPartitionFound
    | x :: xs ->
      (* Try including the current element in the first partition *)
        try
          let (partition1, partition2) = find_partition (sum1 + x) sum2 xs in
          (x :: partition1, partition2)
        with NoPartitionFound ->
        (* If no solution found for the first partition, backtrack and try the second partition *)
        (* Include the current element in the second partition *)
          let (partition1, partition2) = find_partition sum1 (sum2 + x) xs in
          (partition1, x :: partition2)
  in
  find_partition 0 0 ns
    

(* this function turns the output of partition into a type option *)
(* the tests you write will be tested against this function *)
(* this is meant to allow you to write success and failure tests *)  
let partition_option (ns : int list) : (int list * int list) option =
  try Some (partition ns) with
  | NoPartitionFound -> None


(* Question 2A: find a list of int from distinct tuples that add up to tot *)
(*TODO: test cases *) 

let choice_sum_option_tests : ((int * ((int * int) list)) * (int list) option) list =
  [ 
    ((0, [(1, 5); (2, 4); (3, 4)]), None); 
    ((6, [(1,5); (2,4); (3,4)]), Some [1; 2; 3]); 
    ((10, [(1,5); (2,4); (3,4)]), Some [5; 2; 3]); 
    ((3, [(0,0); (0,0); (0,0)]), None); 
  ]
  

let choice_sum (n : int) (tuples : (int * int) list) : int list =
  let rec go n tuples acc =
    match tuples with
    | [] -> if n = 0 then List.rev acc else raise NoSumFound
    | (x, y)::xs ->
        try go (n - x) xs (x::acc)
        with NoSumFound -> go (n - y) xs (y::acc)
  in go n tuples []


(* this function turns the output of choice_sum into a type option *)
(* the tests you write will be tested against this function *)
(* this is meant to allow you to write success and failure tests *) 

let choice_sum_option (n : int) (tuples : (int * int) list) : int list option =
  try Some (choice_sum n tuples) with
  | NoSumFound -> None

(* Question 2B: find a subset of tuple that add up to a given tuple *)
(* TODO: test cases *)

let subset_sum_option_tests : (((int * int) * ((int * int) list)) * ((int * int) list option)) list =
  [
    (((3, 3), [(1,1); (2,2); (3,3)]), Some [(1,1); (2,2)]);
    (((10, 10), [(1,1); (2,2); (3,3)]), None); 
    ((1, 1), [(1,0);(0,1)]), Some [(1,0);(0,1)]; 
    ((0, 0), []), Some [];

    ((3, 3), [(1,1);(1,1);(1,1);(2,2)]), Some [(1,1);(1,1);(1,1)] 

  ]


  
(* TODO: implement subset_sum_Q2B_helper *) 
  
let subset_sum (target: (int * int)) (tuples : (int * int) list) : (int * int) list =
  let rec aux target tuples acc =
    match tuples with
    | [] -> if target = (0, 0) then List.rev acc else raise NoSubsetFound
    | (x, y)::rest ->
        if x <= fst target && y <= snd target then
          try aux ((fst target) - x, (snd target) - y) rest ((x, y)::acc)
          with NoSubsetFound -> aux target rest acc
        else aux target rest acc
  in aux target tuples []

  
(* this function turns the output of subset_sum into a type option *)
(* the tests you write will be tested against this function *)        
(* this is meant to allow you to write success and failure tests *)
let subset_sum_option (target : int * int) (tuples : (int * int) list) : (int * int) list option =
  try Some (subset_sum target tuples) with
  | NoSubsetFound -> None
