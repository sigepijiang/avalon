# Make your vim better
最近github 开始内测atom，看起来还是很不错的样子，让我又有了整理vim插件的冲动

所以，这里主要是Jade 的[Vim配置](https://github.com/rushsinging/vimrc)

## amix/vimrc
我的vim 配置是[amix/vimrc](https://github.com/amix/vimrc)的一份fork

## vimrc
### basic.vim
* 设置`,`为全局`mapleader`
* `:W` 为以最高权限保存
* `F5`为运行当前文件（python）
* `<leader>e`为`:vsplit`
* `<leader>E`为`:split`
* `wildignore`设置为`\*.o``\*.pyc``.git``.hg``.svn`
* `*\#`按键会选中当前单词，以顺序/倒序搜索
* Control + jkhl 可以在split的窗口之间移动
* `<leader>bd`关闭当前buffer，_不怎么常用_
* `<leader>tn/to/tc/te``t``T`标签操作
* 

### extend.vim
	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	" => Parenthesis/bracket
	""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	vnoremap $1 <esc>`>a)<esc>`<i(<esc>
	vnoremap $2 <esc>`>a]<esc>`<i[<esc>
	vnoremap $3 <esc>`>a}<esc>`<i{<esc>
	vnoremap $$ <esc>`>a"<esc>`<i"<esc>
	vno(rem)ap $q <esc>`>a'<esc>`<i'<esc>
	vnoremap $e <esc>`>a"<esc>`<i"<esc>

	" Map auto complete of (, ", ', [
	inoremap $1 ()<esc>i
	inoremap $2 []<esc>i
	inoremap $3 {}<esc>i
	inoremap $4 {<esc>o}<esc>O
	inoremap $q ''<esc>i
	inoremap $e ""<esc>i
	inoremap $t <><esc>i


### filetypes.vim
	au FileType python syn keyword pythonDecorator True None False self

	au BufNewFile,BufRead *.jinja set syntax=htmljinja
	au BufNewFile,BufRead *.mako set ft=mako

	au FileType python map <buffer> F :set foldmethod=indent<cr>

	au FileType python inoremap <buffer> $r return 
	au FileType python inoremap <buffer> $i import 
	au FileType python inoremap <buffer> $p print 
	au FileType python inoremap <buffer> $f #--- PH 	----------------------------------------------<esc>FP2xi
	au FileType python map <buffer> <leader>1 /class 
	au FileType python map <buffer> <leader>2 /def 
	au FileType python map <buffer> <leader>C ?class 
	au FileType python map <buffer> <leader>D ?def
### plugins_config.vim
将在插件内讲解

## 插件

### pathogen
使用pathogen 作为插件管理插件

`call pathogen#infect("path")` 设置插件管理路径

### 主题皮肤
* molokai
* solarized
* vim-tommorrow-theme


### 语法高亮
* nginx
* vim-jinja2
* python-vim
* vim-css-color
* vim-less
* vim-markdown

### 其他功能类

### bufexplorer                     

### syntastic
                             
### vim-bundle-mako  
  
### vim-indent-object
     
### vim-powerline        
### yankring
### closetag     
### open_file_under_cursor  
### tabular                               
### vim-coffee-script              
### vim-snipmate         
### ycm-vim
### ctrlp        
### tlib                                      
### vim-l9                
### vim-snippets         
### zencoding-vim
      
### rainbow-vim             
### vim-addon-manager-known-repositories  
### vim-expand-region  
              
### vim-surround
### mru          
### repeat-vim              
### vim-addon-mw-utils                    
### vim-flake8         
          

### nerdtree                   
### vim-autoclose                         
### vim-fugitivie      
### vim-multiple-cursors  
### yaml-vim