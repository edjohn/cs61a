(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cddr s))
)


(define (sign num)
  (cond
    ((< num 0) -1)
    ((= num 0) 0)
    ((> num 0) 1))
)


(define (square x) (* x x))

(define (pow x y)
  (cond
    ((= y 0) 1)
    ((even? y) (square (pow x (/ y 2))))
    (else
      (* x (pow x (- y 1)))))
)


(define (unique s)
  (if (null? s) nil
    (cons (car s) 
          (unique (filter (lambda (x) (not (eq? x (car s)))) 
                          (cdr s)))))
)


(define (replicate x n)
  (define (helper n lst)
    (if (= n 0)
      lst
      (helper (- n 1) (cons x lst))))
  (helper n nil)
)


(define (accumulate combiner start n term)
  (if (= n 0) 
    start
    (combiner (term n) 
              (accumulate combiner start (- n 1) term)))
)


(define (accumulate-tail combiner start n term)
  (define (helper n total)
    (if (= n 0) 
      total
      (helper (- n 1) (combiner (term n) total))))
  (helper n start)
)


(define-macro (list-of map-expr for var in lst if filter-expr)
    `(map (lambda (,var) ,map-expr) (filter (lambda (,var) ,filter-expr) ,lst)) 
)

