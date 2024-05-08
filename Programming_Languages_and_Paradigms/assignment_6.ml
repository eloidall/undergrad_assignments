(* SECTION 1 *)

(* Question 1.1 *)
let repeat (x : 'a) : 'a stream =
  let rec make_s () = { head = x; tail = mk_susp make_s } in
  make_s ()
  
(* Question 1.2 *)
let rec filter (f : 'a -> bool) (s : 'a stream) : 'a stream =
  if f s.head then
    { head = s.head; tail = mk_susp (fun () -> filter f (force s.tail)) }
  else
    filter f (force s.tail) 

(* Question 1.3 *)
let rec lucas1 = {
  head = 2;
  tail = Susp (fun () -> lucas2);
}
and lucas2 = {
  head = 1;
  tail = Susp (fun () -> zip_with (+) lucas1 lucas2);
}

(* Question 1.4 *)
let rec unfold (f : 'a -> 'b * 'a) (seed : 'a) : 'b stream =
  let x, next_seed = f seed in
  { head = x; tail = mk_susp (fun () -> unfold f next_seed) }

(* Question 1.5 *)
let unfold_lucas : int stream =
  let f (a, b) = (a, (b, a + b)) in
  let seed = (2, 1) in
  unfold (fun seed -> let x, next_seed = f seed in (x, next_seed)) seed 
(* SECTION 2 *) 

(* Question 2.1 *)
let rec scale (s1 : int stream) (n : int) : int stream =
  { head = n * s1.head; tail = mk_susp (fun () -> scale (force s1.tail) n) }

  
let rec merge (s1 : int stream) (s2 : int stream) : int stream =
  if s1.head = s2.head then
    { head = s1.head; tail = mk_susp (fun () -> merge (force s1.tail) (force s2.tail)) }
  else if s1.head < s2.head then
    { head = s1.head; tail = mk_susp (fun () -> merge (force s1.tail) s2) }
  else
    { head = s2.head; tail = mk_susp (fun () -> merge s1 (force s2.tail)) }
    

(* Question 2.2 *)
let rec s = {
  head = 1;
  tail = Susp (fun () ->
      let s2 = scale s 2 in
      let s3 = scale s 3 in
      let s5 = scale s 5 in
      merge s2 (merge s3 s5))
} 







