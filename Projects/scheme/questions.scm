(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.

(define (cons-all first rests)
  (map (lambda (x) (append (list first) x)) rests)
  )

(define (zip pairs)
    (list (map (lambda (x) (car x)) pairs) (map (lambda (x) (cadr x)) pairs))
)

;; Returns a list of two-element lists
(define (enumerate s)
  (define (helper s n)
    (if (equal? nil s) nil
      (cons (list n (car s)) (helper (cdr s) (+ n 1)))))
  (helper s 0)
  )

;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  (cond ((equal? nil denoms) nil)
        ((< total 0) nil)
        ((= 0 total) (list nil))
        (else
          (append (cons-all (car denoms)
                            (list-change (- total (car denoms)) denoms))
                  (list-change total (cdr denoms))))
        )
  )

;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         expr
         )
        ((quoted? expr)
         expr
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           (append (list form params)
                   (map (lambda (x) (let-to-lambda x)) body))
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           (append (list 
                         (append (list 'lambda (car (zip values)))
                                 (map (lambda (x) (let-to-lambda x)) body)))
                   (map (lambda (x) (let-to-lambda x)) (cadr (zip values))))
           ))
        (else
         (map (lambda (x) (let-to-lambda x)) expr)
         )))
