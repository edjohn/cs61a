
(define-macro (def func args body)
   (list 'define (append (list func) args) body)
)


(define (map-stream f s)
    (if (null? s)
    	nil
    	(cons-stream (f (car s)) (map-stream f (cdr-stream s)))))

(define all-three-multiples
  (map-stream 
    (lambda (n) (* n 3))
    (cons-stream 1 (map-stream
                    (lambda (n) (+ 1 (/ n 3))) 
                     all-three-multiples)))
)


(define (compose-all funcs)
  'YOUR-CODE-HERE
)


(define (partial-sums stream)
  'YOUR-CODE-HERE
  (helper 0 stream)
)

