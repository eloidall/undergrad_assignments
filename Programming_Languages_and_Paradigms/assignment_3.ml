(* Hi everyone. All of these problems are generally "one-liners" and have slick solutions. They're quite cute to think
   about but are certainly confusing without the appropriate time and experience that you devote towards reasoning about
   this style. Good luck! :-)  *)
let two : 'b church = fun s z -> s (s z) 
let three : 'b church = fun s z -> s (s (s z)) 
let four : 'b church = fun s z -> s (s (s (s z))) 
let five : 'b church = fun s z -> s (s (s (s (s z))))
let six : 'b church = fun s z -> s (s (s (s (s (s z)))))
    
let height : 'b church = fun s z -> s (s (s (s (s (s (s (s z)))))))

let ten : 'b church = fun s z -> s (s (s (s (s (s (s (s (s (s z))))))))) 
let twelve : 'b church = fun s z -> s (s (s (s (s (s (s (s (s (s (s (s z))))))))))) 
let thirteen : 'b church = fun s z -> s (s (s (s (s (s (s (s (s (s (s (s (s z))))))))))))

(* Question 1a: Church numeral to integer *)
(* TODO: Test cases *)
let to_int_tests : (int church * int) list = [ 
  (zero, 0); 
  (one, 1);
  (five, 5);
  (ten, 10);
  (thirteen, 13); 
];;

(* TODO: Implement
   Although the input n is of type int church, please do not be confused. This is due to typechecking reasons, and for
   your purposes, you could pretend n is of type 'b church just like in the other problems.
*)
let to_int (n : int church) : int = n (fun x -> x + 1) 0
  
(* Question 1b: Determine if a church numeral is zero *)
(* TODO: Test cases *)
let is_zero_tests : ('b church * bool) list = [
  (zero, true); 
  (one, false);
  (five, false);
  (ten, false);
  (thirteen, false); 
];;

(* TODO: Implement *)
let is_zero (n : 'b church) : bool = n (fun _ -> false) true

(* Question 1c: Determine if a church numeral is odd *)
(* TODO: Test cases *)
let is_odd_tests : ('b church * bool) list = [ 
  (zero, false); 
  (one, true);
  (two, false);
  (three, true);
  (four, false); 
  (five, true);
  (six, false); 
  (ten, false);
  (twelve, false);
  (thirteen, true); 
];;

let is_odd (n : 'b church) : bool = n (fun x -> not x) false 

(* Question 1d: Add two church numerals *)
(* TODO: Test cases *)
let add_tests : ( ('b church * 'b church) * 'b church) list = [ 
  ((zero, zero), zero); 
  ((zero, one), one);
  ((one, zero), one); 
  ((one, one), two);
  ((one, two), three);
  ((two, one), three);
  ((two, two), four);
  ((two, three), five);
  ((two, ten), twelve); 
  ((three, ten), thirteen);
];;

let add (n1 : 'b church) (n2 : 'b church) : 'b church = fun s z -> n1 s (n2 s z)

(* Question 1e: Multiply two church numerals *)
(* TODO: Test cases *)
let mult_tests : ( ('b church * 'b church) * 'b church) list = [ 
  ((zero, zero), zero); 
  ((zero, one), zero);
  ((one, zero), zero); 
  ((one, one), one);
  ((one, two), two);
  ((two, one), two);
  ((two, two), four);
  ((two, three), six); 
  ((two, five), ten);
  ((three, four), twelve);
  ((six, two), twelve); 
];;

let mult (n1 : 'b church) (n2 : 'b church) : 'b church = 
  fun s -> n1 (fun x -> n2 s x) 

(* Question 2a: Write a function taking an int and a church and returning the int to the power of the church *)
(* TODO: Test cases *)
let int_pow_church_tests : ((int * 'b church) * int) list = [ 
  ((1, zero), 1);
  ((4, zero), 1);
  ((5, zero), 1); 
  ((0, one), 0);
  ((1, one), 1);
  ((2, one), 2);
  ((3, one), 3);
  ((10, one), 10); 
  ((2, two), 4);
  ((4, two), 16);
  ((2, three), 8);
  ((4, three), 64);
  ((5, five), 3125);
  ((4, ten), 1048576); 
];;

let int_pow_church (x : int) (n : 'b church) : int = n (fun y -> x * y) 1


(* Question 2b: Write a function taking tuple of church and incrementing both values of the tuple of the value of the church *)
(* TODO: Test cases *)
let swap_add_tests : (('b church * 'b church) * ('b church * 'b church)) list = [
  (* test with 0 *)
  ((zero, zero), (zero, zero));
  ((zero, one), (one, one));
  ((one, zero), (zero, one)); 
  ((one, one), (one, two)); 
  ((one, two), (two, three)); 
  (* wrong order *) 
  ((two, one), (one, three)); 
  ((two, three), (three, five));
  (* wrong order *)
  ((three, two), (two, five)); 
];;

let swap_add (t : ('b church * 'b church)) : ('b church * 'b church) = 
  let (x, y) = t in (y, add x y)
  

(* Question 2c: Write a function computing the nth term of the Fibonacci suite *)
(* TODO: Test cases *)
let fibo_tests : ('a church * 'b church) list = [ 
  (zero, zero);
  (one, one);
  (two, one);
  (three, two); 
  (four, three);
  (five, five);
  (six, height);
];;

(* Should use swap_add *)
let fibo (n : 'a church) : 'b church = fst (n swap_add (zero, one))


