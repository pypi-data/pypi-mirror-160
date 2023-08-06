/// Features => [F1(A), F2(A), F3(B), F4(C), F5(B)]
/// 
/// A primitive of P1([[A]]) -> A, takes a feature of type A, and creates a feature of type A
/// 
/// So available inputs for P1(A) are [[F1(A)], [F2(A)]]. There are 2 sets, with each set having only a single input
/// 
/// A primitive of P2([[A,A]]) -> A, takes 2 features, the first of type A, and the second of type A
/// 
/// So available inputs for P2([[A,A]]) are [[F1(A), F2(A)]] (and maybe [[F2(A), F1(A)]]). There is 1 set, with 2 inputs
/// 
/// A primitive of P3([[A], [B]]), is a function that takes a single input, but it could be of type A or type B
/// P3([[A], [B]]) -> [[F1(A)], [F2(A)], [F3(B)], [F5(B)]]
/// 
/// P4([[A,A], [B,B]]) is a function that takes 2 arguments, either A and A, or B and B
/// P4([[A,A], [B,B]]) -> [[F1(A), F2(A)], [F3(B), F5(B)]]


# TODO:

- Investigate Greater Than Scalar, I think I need to parse primitives differently