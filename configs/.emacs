; c-mode
; asm-mode
;

(defvar g-nlines 2)
(defvar g-fwidth 3)
(defvar g-lfmt "hi")
(defvar testvar 15)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                           Pretty Line Numbering                                 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; (defun get-linum-border-string ()
;;   (let ((linum-border-face
;; 	 '((t :inherit (default)
;; 	      :background "#808080")
;; 	   "Face for border space between line numbers and text.")))
;;     (propertize " "
;; 		'face
;; 		linum-border-face)))

;; (defun (linum-format-custom-hook line)
;;     (let*
;; 	((num-file-lines (+ 1 0))
;; 	 (numfield-width (ceiling 4))
;; 	 (fmt (format " %%%dd "
;; 		      numfield-width)))
;;       (setq g-nlines num-file-lines)
;;       (setq g-fwidth numfield-width)
;;       (setq g-lfmt fmt)
;;       (format "%s%s"
;; 	      (propertize (format fmt line)
;; 			  'nil
;; 			  'linum)
;; 	      (get-linum-border-string))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                           Custom Variables                                 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ;; custom-set-variables, custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(auto-save-file-name-transforms
   '(("\\`/[^/]*:\\([^/]*/\\)*\\([^/]*\\)\\'" "/home/kyle/.emacs.d/auto-save-list/\\2" t)))
 '(backup-directory-alist '(("." . "/home/kyle/.emacs.d/backup-dir")))
 '(c-mode-hook '((lambda nil (linum-mode 't))))
 '(completion-auto-help 'lazy)
 ;;'(custom-enabled-themes '(deeper-blue))
 '(emacs-lisp-mode-hook '((lambda nil (linum-mode 't))))
 '(linum-format linum-format-custom-hook)
 '(show-paren-mode t)
 '(column-number-mode t))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                           Custom Faces                                 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(linum ((t (:inherit (shadow default) :background "#404040" :foreground "#a0a0a0")))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                        Convenient Eval Functions                             
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Eval and print-print the last sexpr
;; KEY-BIND to C-q
(defun pp-eval-at-point ()
  (interactive)
  (insert "\n")
  (pp-eval-last-sexp t))
(global-set-key (kbd "C-q") 'pp-eval-at-point)


;;
;; ;; Re-evaluate last manual command executed in the minibuffer
;;
;; (global-set-key (kbd "C-x C-z")
;; 		(lambda nil
;; 		  (interactive)
;; 		  (eval (car command-history))))


;; Evaluate a cons list at the point and print each element
;; one by one for a maximum number of times. Return the point
;; to where we issued the command.
(defun eval-list-at-point (&optional line-limit)
  (interactive)
  (let* ((list-length-limit (or line-limit 5))
	 (mylist (eval-last-sexp nil))
	 (curr-line (count-lines (point-min) (point))))
    (catch 'list-too-long
      (let ((i 0))
	(dolist (v mylist)
	  (insert (format "\n  %s" v))
	  (if (= i (- list-length-limit 1))
	      (progn (insert "\n  ...")
		     (throw 'list-too-long nil)))
	  (setq i (+ i 1)))))
    (goto-line (+ curr-line 1))))


;;
;; Trying to set-up some custom help window handling...
;;
;; ;; should already been in help-mode at the point this is called
;; (defvar custom-main-window nil)
;; (defun custom-help-setup ()
;;   (switch-to-buffer-other-window "*Help*")
;;   (let* ((window-height (window-body-height))
;; 	 (new-window-height (/ window-height 2)))
;;     (split-window-below)
;;     (switch-to-prev-buffer)
;;     (other-window 1)
;;     ;(shrink-window (- window-height new-window-height))
;;     ))


;;
;; Trying to setup some initial windows
;;
;; Set up windows
;; (progn (setq custom-main-window (car (window-list)))
;;        ;; Setup scratch in upper right
;;        (split-window-right)
;;        (other-window 1)
;;        (switch-to-buffer "*scratch*")
;;        ;; Setup messages in lower right
;;        (progn (split-window-below)
;; 	      (other-window 1)
;; 	      (switch-to-buffer "*Messages*")
;; 	      ;; Shrink it
;; 	      (let* ((window-height (window-body-height))
;; 		     (new-window-height (/ window-height 2)))
;; 		(setq new-window-height 12)
;; 		(shrink-window (- window-height new-window-height))))
;;        ;; Setup *Help* buffer in the main window
;;        (other-window -2)
;;        (let ((orig-buf-name (buffer-name)))
;; 	 (switch-to-buffer "*Help*")
;; 	 (switch-to-buffer orig-buf-name))
;;        ;; Setup the x
;;        (setq temp-buffer-window-setup-hook
;; 	     (cons 'custom-help-setup temp-buffer-window-setup-hook)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                Setup the custom theme and font coloring
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(defun set-custom-theme-faces ()
  (let* ((class '((class color) (min-colors 89)))
	 (face-a-list-pair
	  `((cursor                       ((,class (:background "#b0b0b0"))))
	    (font-lock-comment-face       ((,class (:foreground "#80e080"))))
	    (font-lock-builtin-face       ((,class (:foreground "#ffb040"))))
	    (font-lock-function-name-face ((,class (:foreground "#60c0ff"))))
	    (error                        ((,class (:foreground "#ff5050"))))
	    (font-lock-keyword-face       ((,class (:foreground "#d090ff"))))
	    (font-lock-preprocessor-face  ((,class (:background "#ff0000"))))
	    (font-lock-reference-face     ((,class (:background "#ff0000"))))
	    (font-lock-string-face        ((,class (:foreground "#607070"))))
	    (font-lock-type-face          ((,class (:background "#ff0000"))))
	    (font-lock-variable-name-face ((,class (:background "#ff00000")))))))
    ;; Construct a list of quoted face, attribute pairs
    (let* ((args (let ((result nil))
		   (dolist (arg face-a-list-pair result)
		     (setq result (cons `(quote ,arg) result)))))
	   ;; Construct command to set the faces collected above
	   (code `(custom-theme-set-faces 'deeper-blue ,@args)))
      (eval code t))))

(progn (load-theme 'deeper-blue)
	(set-custom-theme-faces)
	(custom-set-variables '(custom-enabled-themes '(deeper-blue))))


