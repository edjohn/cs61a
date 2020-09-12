(define (rle s)
  (define (helper s n prev)
    (cond ((null? s) (if (null? prev) nil (cons-stream (list prev n) nil)))
          ((null? prev) (helper (cdr-stream s) 1 (car s)))
          ((equal? prev (car s)) (helper (cdr-stream s) (+ n 1) (car s)))
          (else
            (cons-stream (list prev n) (helper (cdr-stream s) 1 (car s))))
          )
    )
  (helper s 1 nil)
  )


(define (group-by-nondecreasing s)
  (define (helper s prev sofar)
    (cond ((null? s) (if (null? prev) nil (cons-stream sofar nil)))
          ((null? prev) (helper (cdr-stream s) (car s) (list (car s))))
          ((< (car s) prev) (cons-stream sofar (helper (cdr-stream s) (car s) (list (car s)))))
          (else
            (helper (cdr-stream s) (car s) (append sofar (list (car s)))))
          )
    )
  (helper s nil (list nil))
  )



(define finite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 3
                (cons-stream 1
                    (cons-stream 2
                        (cons-stream 2
                            (cons-stream 1 nil))))))))

(define infinite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 2
                infinite-test-stream))))

