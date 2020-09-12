(define (split-at lst n)
  (define (helper copy n sofar)
    (cond ((= 0 n) (cons sofar copy))
          ((null? copy) (cons lst nil))
          (else
            (helper (cdr copy) (- n 1) (append sofar (list (car copy)))))
          )
    )
  (helper lst n nil)
  )


(define-macro (switch expr cases)
	(cons 'cond
		(map (lambda (case) (cons `(equal? ,expr ',(car case)) (cdr case)))
    			cases))
)
