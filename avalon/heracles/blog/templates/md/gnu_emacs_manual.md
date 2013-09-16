# GNU Emacs Manual

## The Organization of the Screen 屏幕组织

### frame
GNU 和 终端下：
* X Window System: a graphical window
* text terminal: the entire terminal screen 

组织：
* a menu bar on the top(unusable in text terminal)  菜单栏
* a tool bar under the menu bar 工具栏
* a echo area at the very bottom of the frame 信息栏
* the area between the tool bar and echo area is called the window 窗口

### The Mode Line
每个窗口得最底部
    cs:ch-fr buf pos line (major minor)
* cs: 字符集设置。以-开头表示没有特殊的字符集设置，以=开头表示没有任何的转换。其他字符表示不同的字符集。在终端中，*cs*前会有两个厄外的字符，表示键盘输入和输出字符集。
* : 换行符标志，当在MS-DOS系统中会是一个`\`或者`(DOS)`，在旧的MAC系统中会是一个`/`或者`Mac`，某些系统中会显示为`(Unix)`。我的emacs显示的为普通的冒号。
* ch: 两个破折号(`--`)表示显示的文本和硬盘中的文件内容一致，如果已经被修改了，会显示为(`**`)。当文本为只读时显示为`%%`，如果文本修改了会显示`%*`（只读文本根本无法编辑，所以没有测试）。
* -: 如果默认路径是一个远程地址，会被`@`替换。
* fr: 选中的窗口的名称。（只会在终端模式中显示，为`F1`）
* buf: 窗口中显示的buffer缓冲区的名字，一般和文件的名字一样。
* pos: `nn%`, `TOP`, `BOT`, `ALL`
* line: L(\d), 
* major: 当前的模式
* minor: 一些其他的模式 

## 用户输入的种类

按下<ESC>然后放开 可以视为<Meta>键

## 命令

* 完成的命令
* 命令前缀

## 按键，命令与命令名

* 命令
* 命令名
* 命令与按键的绑定
* 变量

## 进入Emacs
* terminal: emacs, emacs &, %emacs
* start up screen 
* `c-h t`(help-with-tutorial)
* emacsclient
* `inhibit-startup-screen`设置是否显示欢迎页面
* `inhibit-buffer-choice`启动时显示的缓冲区

## 退出
* C-x C-c
* C-z suspend-frame(%emacs)
* confirm-kill-emacs
* M-x kil-emacs

## 基本编辑操作
#### 插入
* C-q <RET> <C-g> 可以输入这些按键代表的字符
* C-x 8 <RET> 可以以ascii或者unicode编码的方式输入字符

### 移动光标
* 方向键
* 鼠标左键
* C-f(forward-char), C-b(backward-char), C-n(next-line), C-p(previous-line), C-a(move-beginning-of-line), C-e(move-end-of-line)
* M-f(forward-word),  M/C-<right>(right-word)后移一个单词，与M-f的不同体现在当前文本为从右向左读的文本的时候
* M-b(backward-word), C/M-<left>(left-word)
* M-r(move-to-window-line-top), 在第一行，屏幕中间和最后一行之间跳转，加参数表示距离第一行多少行， -1表示最后一行
* M-<(beginnig-of-buffer), M->(end-of-buffer)
* C-v(scroll-up-command), M-v(scroll-down-command)
* *M-x(goto-char), 读取一个参数n，移动到一个文本的第n个字符*有问题
* M-g M-g, M-g g(goto-line)
* C-x C-n(set-global-column), C-u C-x C-n取消，这个命令在emacs 24.3中已经被默认**禁止**了，所以没做测试
* `line-move-visual, track-eol, next-line-add-newline`

### 删除文本
* <DEL>, <Backspace>(delete-backward-char)
* <DELETE>(delete-forward-char)
* C-d(delete-char)
* C-k(kill-line)
* M-d(kill-word)
* M-<DEL>(backword-kill-word), *不知道怎么用*

### 取消修改
C-/, C-x u, C-_, **24.3测试C-/无效**

### 文件
    C-x C-f file_name <RET>
    C-x C-s 

### 帮助
    C-h k key_name 

### 空白行
* C-o(open-line)
* C-x C-o(delete-blank-lines)

### 换行
一些有关强制换行的信息，这里描述的并不详细，稍后在其他章节介绍。

### 光标信息
* M-x what-line
* M-=(count-words-region), M-x count-words
* C-x =(what-cursor-position)
        Char: c (99, #o143, #x63) point=2 8062 of 36168()78% Column=53

### 参数
* M--(negative-argument), M-1 / M-2 (digit-argument)
* C-u, C-u== C-u 4(C-u C-n == C-u 4 C-n)

### 重复命令
C-x (z)+ 一个z重复一次

## Minibuffer(*未实用*)
### 文件名缓冲
insert-default-directory 设置默认的路径

### 编辑
(C-j(newline-and-indent))

values & command:

* resize-mini-windows
* max-mini-window-height
* C-M-v
* enable-recursive-minibuffers

### 自动补全

* <TAB>
* <RET>
* <SPC>

completion-styles *有兴趣的可以看看这个的设定，好复杂，以后再看*

还有一些变量，以后在描述


## 通过名字运行命令
M-x command <RET>

## 帮助 `C-h`
* C-h a [] <RET> 搜索命令
* C-h i d m emacs <RET> i [] <RET>
* C-h i d m emacs <RET> s [] <RET>
* C-h C-f Emacs FAQ
* C-h p 搜索emacs包

### 帮助小结

* C-h a, apropos-command
* C-h b, 按键绑定, describe-binding
* C-h c, 简要的描述关键字, describe-key-briefly
* C-h d [] <RET>, 通过文档查找, apropos-documentation
* C-h e, 显示信息拦, echo-area-messages
* C-h f [function] <RET>, 显示关于名为function的Lisp函数的信息, describe-function
* C-h h, 显示如何说hello文件(卖萌的么)
* C-h i, 运行Info, 
* C-h k [key], 显示关于一个命令的信息, describe-key
* C-h l, 显示历史300条命令, view-lossage
* C-h m, 显示当前模式的文档, describe-mode 
* C-h n, 显示emacs最新更新, view-emacs-news
* C-h p, 查找包,
* C-h P [Package] <RET>, 按名字查找包的文档, describe-package
* C-h r, 显示emac info 页面, info-emacs-manual
* C-h s, 显示当前模式的语法, describe-syntax
* C-h t, 用户引导页面, help-with-tutorial
* C-h v, 变量描述, describe-variable
* C-h w, 命令描述, where-is
* C-h C [coding] <RET>, 描述编码环境(coding system), describe-coding-system
* C-h C <RET>, 关于默认编码系统
* C-h F [command] <RET>, 进入Info并跳到command的介绍节点上, Info-goto-emacs-command-node
* C-h I [method] <RET>, 查看输入法的帮助 
* C-h K [key], 进入Info页面并跳到按键绑定key的节点上, Info-goto-emacs-key-command-node
* C-h L [language-env] <RET>, 关于字符集和可用输入法的介绍, describe-language-environment
* C-h S [symbol] <RET>, 关于symbol的文档, info-lookup-symbol
* C-h ., 在一个特殊的文本区域内显示帮助, display-local-help

### 关于按键序列的文档
C-h k/K/c 

### 关于命令和变量的帮助
C-h f/v/F

### Apropos 搜索适当的解释
* C-h a
* M-x apropos
* M-x apropos-variable 用户自定义变量
* M-x apropos-value 
* C-h d, 根据文档搜索, apropos-documentation

### 帮助模式
* <RET> 进入一个引用（超链接）, help-follow
* <TAB> 下一个超链接, forward-button
* S-<TAB> 地球人都知道, backward-button
* C-c C-c 显示所有文档, help-follow-symbol *未测试*
* C-c C-b 返回上个话题, help-go-back *未测试*

### 查询包
C-h p/P

### 国际化支持
* C-h L, describe-language-environment
* C-h h, hello file, view-hello-file
* C-h I, 描述输入法, describe-input-method
* C-h C, 描述字符集, 

### 其他命令
* C-h i 
* C-h F/K
* C-h S, 查找符号（方法，变量，按键组合）, info-lookup-symbol
* C-h l, 查看输入历史
* C-h e, 查看消息缓冲区
* C-h m, 查看当前模式下的说明文档
* C-h b, 查看按键绑定
* C-h s, 查看系统环境

### 帮助文件
* C-h C-c, 版权说明, describe-coping
* C-h C-d, debug模式的说明, view-emacs-debugging
* C-h C-e, 关于如何获取扩展包, view-external-packages
* C-h C-f,  FAQ, view-emacs-FAQ
* C-h g, 关于GNU Project的介绍, describe-gnu-project 
* C-h C-m, 关于本书的信息, view-order-manuals
* C-h C-n, emacs的更新, view-emacs-news
* C-h C-o, 关于如何下载最新的emacs, describe-distribution
* C-h C-p, 已知的问题, view-emacs-problems
* C-h C-t, emacs todo-list, view-emacs-todo
* C-h C-w, GNU Emacs的担保, describe-no-warranty

## 标记和选中区域
### 设置标记
* C-<SPC>, C-@, set-mark-command
* C-x, C-x, 返回设置标记的初始位置并保持标记, exchange-point-and-mark 
* C-g, 取消
* 利用 'C-@ C-@' 以及 'C-u C-@'在缓冲区内跳转
* M-@, 将当前位置到下一个单词结尾位置，且不移动光标, mark-word
* C-M-@, 感觉和M-@相似, mark-sexp *未测试*
* M-h, 标记本段, mark-paragraph
* C-M-h, 标记一段函数定义, mark-defun
* C-x C-p, 标记当前页, mark-page
* C-x h, 全部标记, mark-whole-buffer

### 对于标记的区域的操作
* C-w, 删除
* M-w, 拷贝到已删除列表
* C-x C-l, C-x C-u 转换大小写
* C-u C-/, C-\_, 撤销修改
* M-%, 替换
* 用C-x <TAB>, C-M-\ 缩进
* M-x fill-region, 填充内容
* M-$, 检查拼写,
* M-x eval-region, 以lisp代码方式对待
* C-x r s, 存储进一个寄存器
* 存储进一个文件

### 标记列表

* C-<SPC> C-<SPC>
* C-u C-<SPC>

### 全局标记列表 *未测试*
* C-x C-<SPC>, pop-global-mark

### Shift选择 *不知道为什么无效*

> Shift-selection only works if the Shifted cursor motion key is not already bound to a separate command.

### 取消临时标记模式

    M-x transient-mark-Mode

## 删除和移动文本

> In Emacs, killing means erasing text and coping it into the kill ring.

> Yanking means bringing text from the kill ring back to the buffer.

> Some applications user the terms "cutting" and "pasting" for similar operation.

### Kill and Delete

#### 移除(delete)

* <DEL>
* <Backspace>
* <Delete>
* C-d, delete-char
* M-\, delete-horizontal-space
* M-<SPC>, 只留一个空格, just-one-space
* C-x C-o, 删除附近的空白行, delete-blank-lines
* M-^, 删除两行之间的换行符, delete-indentation

#### 删除一行

* C-k, kill-Line
* C-S-backspace, kill-whole-line *无效*

#### 其他删除命令

* C-w, kill-region
* M-w, kill-ring-save
* M-d, kill-word
* M-<DEL> backward-kill-word
* C-x <DEL>, backward-kill-sentence
* M-k, kill-sentence
* C-M-k, kill-sexp
* M-z char, zap-to-char

#### 删除的选项

### Yanking
* C-y, yank
* M-y, yank-pop
* C-M-w, append-next-kill

#### 删除列表

### 剪切复制

#### 使用剪贴板

> Prior to Emacs 24,  the kill and yank commands used the primary 
> selection, not the clipboard

#### 使用其他其他窗口程序完成剪贴和复制

#### 添加文本
* M-x append-to-buffer
* M-x prepend-to-buffer
* M-x copy-to-buffer
* M-x insert-buffer
* M-x append-to-file

### 矩形区域
### CUA模式

## 寄存器
存放文本，矩形区域，位置和其他东西。

    M-x view-register <RET> r

### 位置
* C-x r <>
