Module('login', function() {
    function checkBtnPara(btn){
        if ($.is.Function(btn) || ($.is.String(btn) && btn.length > 0)){
            return true;
        }
        return false;
    }

    function getBtnPara(btn){
        if (!checkBtnPara(btn)){
            throw ('the element should be a str or function');
        }
        result = btn;

        if ($.is.Function(btn)){
            result = btn()
        }

        return result;
    }

    this.exports.init = function(config){
        config = config || {};

        var login_type = config.login_type || '',
            http_method = config.http_method || 'post',
            signUpBtn = config.signUpBtn,
            signInBtn = config.signInBtn,
            logoutBtn = config.logoutBtn;
            
        return {
            signUp: function() {
                btn = getBtnPara(btn);
            },
            signIn: function() {
                btn = getBtnPara(btn);
            },
            logout: function() {
                btn = getBtnPara(btn);
            },
            config: config,
        }
    };
});
