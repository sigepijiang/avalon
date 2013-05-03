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
* line: L(\d)*, 
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
* C-h a [] <RET>, 搜索命令
* C-h i d m emacs <RET> i [] <RET>
* C-h i d m emacs <RET> s [] <RET>
* C-h C-f Emacs FAQ
* C-h p 搜索emacs包