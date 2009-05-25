;; gr-rss.scm -- download feeds from Google Reader
;; Copyright Eric Nichols <eric-n@is.naist.jp>
;; Nara Institute of Science and Technology, 2008

;; blog/category/date/title.{html,txt}

(use srfi-1 srfi-13 ssax rss http-client)

(define (category x) (string-join (string-split x " ") "-"))
(define (link x) x)
(define (pubDate x)
  (let* ((convm '(("Jan" "01")
		  ("Feb" "02")
		  ("Mar" "03")
		  ("Apr" "04")
		  ("May" "05")
		  ("Jun" "06")
		  ("Jul" "07")
		  ("Aug" "08")
		  ("Sep" "09")
		  ("Oct" "10")
		  ("Nov" "11")
		  ("Dec" "12")))
	 (s (string-split x))
	 (d (second s))
	 (m (cadr (assoc (third s) convm)))
	 (y (fourth s)))
    (string-join (list y m) "")))

(define (title link) 
  (let ((l (string-split link "/")))
     (last l)))
(define (blog link) 
  (let ((l (string-split link "/")))
    (second l)))

(define (file-stem item)
  (let* ((c (first item))
	 (d (second item))
	 (l (third item))
	 (b (blog l))
	 (t (title l)))
    (string-join (list b c d t) "/") ) )

(define (link+file-stem item)
  (let ((l (third item))
	(f (file-stem item)))
    (format "~a ~a" l f)))

(define (gi i)
  (let ((attrs (rss:item-attributes i) ))
    ((lambda (x y) 
       (map (lambda (z) (cons z x)) y) )
     (map (lambda (a) (list (car a) (cdr a)))
	  (filter (lambda (x) (member (car x)
				 ;; '(title link pubDate)
				 '(link pubDate) 
				 ) )
		  attrs ) )
     (map (lambda (a) (list (car a) (cdr a)))
	  (filter (lambda (x) (member (car x) '(category) ) )
		  attrs ) ) ) ) )

(define (fi i)
  (map (lambda (x) (map eval x))
       (gi i)))

;; (define (format-item i)
;;   ((lambda (x y) 
;;      (map (lambda (z) (cons z x)) y) )
;;    (list (rss:item-title i)
;; 	 (rss:item-link i)
;; 	 (rss:item-attribute i 'pubDate) )
;;    (rss:item-attribute/multi i 'category) ) )
 
(define (main args)
  (let ((url (car args))
	 ;; (port (open-input-resource url))
	)
    (define-values (h a i o)
      (http:send-request url))
    (begin 
      (let ( (feed (rss:read i)) )
	(map (lambda (i) 
	       (begin (write (link+file-stem i))
		      (newline)))
	     (append-map fi (rss:feed-items feed)) ) )
      (close-input-port i)
      (close-output-port o) ) ) )

;; usage: bs-rss <feed-url>
(cond-expand
 (compiling (main (command-line-arguments)))
 (else #f))