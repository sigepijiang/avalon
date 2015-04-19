Module('adminList', function(){
    this.run = function(){
        $(function(){
            if (!window.operatorURI){
                return;
            }

            $('[data-action]').on('click', function(){
                var ele = $(this),
                    action = ele.attr('data-action'),
                    oid = ele.attr('data-oid'),
                    needConfirm = ele.attr('data-confirm'),
                    needPrompt = ele.attr('data-prompt'),
                    after = ele.attr('data-after'),
                    afterStyle = ele.attr('data-afterStyle')
                    parentEle = ele.closest('tr');
                
                if(needConfirm && !confirm('确定吗？')){
                    return;
                }

                if (needPrompt && prompt('请输入操作对象的ID：[' + oid +']：') != oid){
                    alert('输入错误！')
                    return;
                }

                $.post(operatorURI + oid + '/' + action + '/', function(){
                    if (after == 'remove'){
                        parentEle.remove()
                    }
                    else {
                    }
                })
            });
        })
    }
})

