(require 'package)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Create a wrapper around package-install so we don't initialize
;; and refresh melpa before we need it, every time we start up...
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(fset 'my-package-install (symbol-function 'package-install))
(setq did-setup-package-install nil)
(defun package-install (pkg &optional DONT-SELECT)
  (if (not did-setup-package-install)	
      (progn (setq did-setup-package-install 't)
	     (add-to-list 'package-archives
			  '("melpa" . "https://melpa.org/packages/") t)
	     (package-initialize)
	     (package-refresh-contents)))
  (my-package-install pkg DONT-SELECT))


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
;;                            Mode Hooks                                 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(defun custom-makefile-mode-hook ()
  (setq indent-line-function 'indent-relative-first-indent-point))


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
 '(makefile-mode-hook '(custom-makefile-mode-hook))
 '(column-number-mode t)
 '(completion-auto-help 'lazy)
 '(custom-enabled-themes '(deeper-blue))
 '(emacs-lisp-mode-hook '((lambda nil (linum-mode 't))))
 '(enable-recursive-minibuffers t)
 '(linum-format linum-format-custom-hook)
 '(enable-recursive-minibuffers t)
 '(package-selected-packages
   '(nav rust-mode))
 '(prog-mode-hook '(toggle-truncate-lines))
 '(rust-indent-offset 2)
 '(show-paren-mode t))


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
;;                           Font and Visuals                                 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Set the font
;;(set-frame-font "-misc-fixed-medium-r-normal--20-*-75-75-c-100-iso8859-14" 't 't)
;;(set-frame-font "-misc-fixed-medium-r-normal--12-*-75-75-c-70-iso8859-1" 't 't)
(set-frame-font "-1ASC-Liberation Mono-normal-normal-normal-*-*-*-*-*-m-0-iso10646-1" 't 't)
(set-face-attribute 'default nil :height 85)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                           Keybindings                                 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Change how the buffer menu appears (open in the same window)
(global-set-key "\C-x\C-b" 'buffer-menu)

;; Bind 'revert-buffer'
(global-set-key "\C-x\C-r" 'revert-buffer)


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


;; Wrap the current line in a string and move the cursor
;; down to the next line.
(defun wrap-line-in-string ()
  (interactive)
  (move-beginning-of-line 1)
  (insert "\"")
  (move-end-of-line 1)
  (insert "\"")
  (move-beginning-of-line 2))
(global-set-key (kbd "C-M-S-s") 'wrap-line-in-string)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                Setup the custom theme and font coloring
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(defun set-custom-theme-faces ()
  (let* ((class '((class color) (min-colors 89)))
	 (face-a-list-pair
	  `((cursor                       ((,class (:background "#b0b0b0"))))
	    (font-lock-comment-face       ((,class (:foreground "#80e080"))))
	    (font-lock-doc-face           ((,class (:foreground "#90a0a0"))))
	    (font-lock-constant-face      ((,class (:foreground "#c0d0d0"))))
	    (font-lock-builtin-face       ((,class (:foreground "#ffb0b0"))))
	    (font-lock-function-name-face ((,class (:foreground "#80e080"))))
	    (error                        ((,class (:foreground "#ff5050"))))
	    (font-lock-keyword-face       ((,class (:foreground "#60c0ff"))))
	    (font-lock-reference-face     ((,class (:background "#ff0000"))))
	    (font-lock-string-face        ((,class (:foreground "#90a0a0"))))
	    (font-lock-type-face          ((,class (:foreground "#f0b0ff"))))
	    (font-lock-preprocessor-face  ((,class (:foreground "#ffa0a0"))))
	    (font-lock-variable-name-face ((,class (:foreground "#ffe8c0"))))
	    (rust-builtin-formatting-macro-face ((,class (:foreground "#ffa0a0")))))))
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




;; EDITED, examine
;; Cycle through a list of fonts and try them out on the current
;; frame. Enter 'y' if you like the font and it will be recorded
;; below your point. Enter anything else and it will move onto the
;; next font. In the end, you'll have a list of fonts you liked
;; below the point.
;; (progn (insert "\n")
;;        ;;       (dolist (f (x-list-fonts "*"))
;;        (dolist (f c2)
;; 	 (progn (ignore-errors (set-frame-font "-misc-fixed-medium-r-normal--20-*-75-75-c-100-iso8859-14" 't't))
;; 		(ignore-errors (set-frame-font f 't 't))
;; 		(kill-line)
;; 		(insert f)
;; 		(move-beginning-of-line nil)
;; 		(let ((op (read-string "")))
;; 		  (if (string-match-p "y" op)
;; 		      (progn (move-beginning-of-line 2)
;; 			     (insert (format "%s\n" f))
;; 			     (move-beginning-of-line -1)))))))
;;
;; Potential Like Fonts
;;
;; "-CYRE-Comfortaa-light-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-bitstream-Courier 10 Pitch-bold-italic-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-adobe-courier-bold-o-normal--10-*-75-75-m-60-iso8859-1"
;; "-adobe-courier-bold-r-normal--14-*-100-100-m-90-iso8859-9"
;; "-adobe-courier-bold-r-normal--14-*-75-75-m-90-iso8859-1"
;; "-adobe-courier-medium-r-normal--17-*-100-100-m-100-iso8859-9"
;; "-adobe-courier-medium-r-normal--18-*-75-75-m-110-iso8859-1"
;; "-b&h-lucida-bold-r-normal-sans-17-*-100-100-p-108-iso8859-9"
;; "-b&h-lucidatypewriter-bold-r-normal-sans-11-*-100-100-m-70-iso8859-1"
;; "-b&h-lucidatypewriter-bold-r-normal-sans-17-*-100-100-m-100-iso8859-9"
;; "-b&h-lucidatypewriter-medium-r-normal-sans-14-*-100-100-m-80-iso8859-1"
;; "-b&h-lucidatypewriter-medium-r-normal-sans-17-*-100-100-m-100-iso8859-9"
;; "-b&h-lucidatypewriter-medium-r-normal-sans-18-*-75-75-m-110-iso8859-1"
;; "-b&h-lucidatypewriter-medium-r-normal-sans-20-*-100-100-m-120-iso10646-1"
;; "-misc-fixed-bold-r-normal--13-*-100-100-c-80-iso8859-1"
;; "-misc-fixed-medium-r-normal--13-*-75-75-c-80-koi8-r"
;; "-misc-fixed-medium-r-normal--15-*-75-75-c-90-koi8-r"
;; "-misc-fixed-medium-r-normal--18-*-100-100-c-90-iso8859-8"
;; "-misc-fixed-medium-r-normal--20-*-75-75-c-100-iso8859-14"
;; "-misc-fixed-medium-r-semicondensed--12-*-75-75-c-60-iso8859-9"
;; "-schumacher-clean-medium-r-normal--12-*-75-75-c-60-koi8-r"
;; "-ADBO-Source Code Pro-semibold-normal-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-GOOG-Noto Sans Mono CJK KR-bold-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-ULA -Montserrat-light-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-bitstream-Courier 10 Pitch-bold-italic-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-UKWN-Nimbus Mono PS-normal-normal-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-UKWN-Latin Modern Sans Quotation-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-1ASC-Droid Sans Mono-normal-normal-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-1ASC-Liberation Mono-bold-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-ADBO-Source Code Pro-normal-normal-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-PfEd-DejaVu Sans Mono-normal-normal-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-PfEd-DejaVu Sans Mono-bold-oblique-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-ABAT-Cantarell-light-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-POOP-Fixedsys Excelsior 3.01-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-UKWN-Latin Modern Sans-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-urw-Nimbus Mono PS-normal-normal-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-tyPL-Carlito-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-PfEd-DejaVu Sans Mono-bold-normal-normal-*-*-*-*-*-m-0-iso10646-1"
;; "-CYRE-Comfortaa-bold-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-GOOG-Noto Sans CJK TC-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-PARA-PT Sans Caption-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-ULA -Montserrat-thin-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-ACE -Lohit Devanagari-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-1ASC-Droid Sans-bold-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-1ASC-Liberation Mono-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-PfEd-jsMath-cmr10-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-UKWN-Latin Modern Mono Prop-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-ABAT-Cantarell-normal-normal-normal-*-*-*-*-*-*-0-iso10646-1"
;; "-OOoH-Liberation Sans Narrow-bold-italic-condensed-*-*-*-*-*-*-0-iso10646-1"
;; "-UKWN-TeX Gyre Cursor-normal-italic-normal-*-*-*-*-*-*-0-iso10646-1"
