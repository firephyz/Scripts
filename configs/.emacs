(require 'package)
(add-to-list 'package-archives
	     '("melpa" . "http://melpa.org/packages/"))

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages (quote (rust-mode neotree))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(font-lock-string-face ((t (:foreground "brightgreen")))))

;; Save emacs sessions
;;(desktop-save-mode t)
;;(setq desktop-path '("~/.emacs.d"))

;; Start neotree automatically
(add-to-list 'load-path "~/.emacs.d/elpa/neotree-20181121.2026/")
(require 'neotree)
(neotree)

;; column number mode
(column-number-mode)

;; Set backup directory
(setq backup-directory-alist (list (quote (".*" . "~/.emacs_backups"))))
