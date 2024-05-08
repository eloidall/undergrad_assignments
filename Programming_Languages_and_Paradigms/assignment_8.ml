(* SECTION 1: Laziness *) 
(* Question 1a *) 

let rec lazy_insert v = function
  | LNil -> LCons (v, mk_susp @@ fun () -> LNil)
  | LCons (x, xs) ->
      if v <= x then LCons (v, mk_susp @@ fun () -> LCons (x, xs))
      else LCons (x, mk_susp @@ fun () -> lazy_insert v (force xs)) 

(* Question 1b *) 
let rec lazy_ins_sort = function
  | LNil -> LNil
  | LCons (x, xs) -> lazy_insert x (lazy_ins_sort (force xs))


(* SECTION 2 : Backtracking *) 
(* Question 2a *) 

(* Option 1: Exception-based *)
let tree_sum (t : int tree) (n : int) : int list =
  let rec build_path t acc path =
    match t with
    | Empty -> if acc = n then List.rev path else raise NoTreeSum
    | Tree (l, x, r) ->
        try
          let left_path = build_path l (acc + x) (x :: path) in
          left_path
        with NoTreeSum -> let right_path = build_path r (acc + x) (x :: path) in
          right_path 
  in build_path t 0 [] 

    

(* Option 2: Option *) 
let rec tree_sum_opt (t : int tree) (n : int) : int list =
  let rec build_path t acc path : int list option =
    match t with
    | Empty -> if acc = n then Some (List.rev path) else None
    | Tree (l, x, r) ->
        match build_path l (acc + x) path with
        | Some left_path -> Some (x :: left_path)
        | None ->
            match build_path r (acc + x) path with
            | Some right_path -> Some (x :: right_path)
            | None -> None
  in match build_path t 0 [] with
  | None -> raise NoTreeSum
  | Some path -> path

  
                    
(* Section 3 : References *) 
(* Question 3a *)
let ( *= ) (x : int ref) (n : int) : int = 
  x := !x * n;
  !x

(* Question 3b *) 
let make_piggybank () : piggybank =
  
  let balance = ref 0 in
  let broken = ref false in
  
  let get_balance () =
    if !broken then raise BrokenPiggybank
    else !balance
  in
  
  let add_to_piggybank cash =
    if !broken then raise BrokenPiggybank
    else balance := !balance + cash
  in
  
  let break_piggybank () =
    if !broken then raise BrokenPiggybank
    else begin
      broken := true;
      !balance
    end
  in 
  { get_balance; add_to_piggybank; break_piggybank }


