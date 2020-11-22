# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin"
# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi

PATH=/home/kyle/programs/arm-none-eabi-hard/bin:$PATH
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions

prompt_char=$(echo -e "\u27a4")
text_color='\[\e[38;5;255m\]'
cmd_num_color='\[\e[38;5;75m\]'
user_color='\[\e[38;5;121m\]'
tty_num_color='\[\e[38;5;15m\]'
path_color='\[\e[38;5;145m\]'
# text_color=''
# cmd_num_color=''
# user_color=''
# tty_num_color=''
# path_color=''
ps1_string="${text_color}[${cmd_num_color}\\!${text_color}] ${user_color}\\u${text_color}::${tty_num_color}\\l ${path_color}\\w ${text_color}${prompt_char} "
export PS1=${ps1_string}
unset text_color cmd_num_color user_color tty_num_color path_color ps1_string lambda

export UBOOT_DIR=/mnt/harddisk/beagle/uboot/
export PYTHONSTARTUP=/home/kyle/.pythonstartupfile
export PYTHONPATH=/home/kyle/dev/Scripts/python-modules

export QSYS_ROOTDIR="/mnt/harddisk/quartus/20.1/quartus/sopc_builder/bin"
