Module('login', function() {
    function checkElementPara(ele){
        if ($.is.Function(ele) || ($.is.String(ele) && ele.length > 0)){
            return true;
        }
        return false;
    }

    function getElementPara(ele){
        if (!checkElementPara(ele)){
            throw ('the element should be a str or function');
        }
        result = ele;

        if ($.is.Function(ele)){
            result = ele();
        }

        return result;
    }

    function setPasswordHash(form){
        var password = $(form).find('input[name="password_hash"]').val();
        var password_hash = password;

        if (password_hash != ''){
            password_hash = $.md5(password);
        }

        $(form).find('input[name="password_hash"]').val(password_hash);
        $(form).find('input[name="password_repeat"]').val(password_hash);
    } 

    this.exports.init = function(config){
        config = config || {};

        var login_type = config.login_type || '',
            http_method = config.http_method || 'post',
            form = config.form;
            
        return {
            signUp: function() {
                var cur_form = $(getElementPara(form));

                $('input[name^="password"]').focus(function(){
                    $(this).removeClass('error-input');
                }).change(function() {
                    var password = $('input[name="password_hash"]').val(),
                        password_repeat = $('input[name="password_repeat"]').val();
                    if (password != password_repeat){
                        $('input[name^="password"]').addClass('error-input')
                    }
                    else {
                        $('input[name^="password"]').removeClass('error-input')
                    }
                });

                cur_form.submit(function(){
                    var password = $(this).find('input[name="password_hash"]').val(),
                        password_repeat = $(this).find('input[name="password_repeat"]').val();
                    if (password != password_repeat){
                        return false
                    }
                    setPasswordHash(this);
                    return true;
                });
            },
            signIn: function() {
                var cur_form = $(getElementPara(form));

                cur_form.submit(function(){
                    setPasswordHash(this);
                    return true;
                });
            },
            config: config,
        }
    };
});
