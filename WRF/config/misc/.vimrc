packadd! dracula
syntax enable
colorscheme dracula
" colorscheme desert
filetype indent on
set nu

" Use spaces for indentation
set tabstop=4       " Number of spaces per tab
set softtabstop=4   " Number of spaces for <Tab> key
set shiftwidth=4    " Number of spaces to (auto)indent
set expandtab       " Use spaces instead of tabs

" Go to the last cursor location when a file is opened, unless this is a
" git commit (in which case it's annoying)
au BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") && &filetype != "gitcommit" |
        \ execute("normal `\"") |
    \ endif
