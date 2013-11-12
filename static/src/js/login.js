Module('login', function() {
    function checkBtnPara(btn){
        if ($.is.Function(btn) || btn.length > 0){
            return true;
        }
        return false;
    }

    function getBtnPara(btn){
        if ($.is.Function(btn)){
            return btn()
        }
        return btn
    }

    this.init = function(config){
        var login_type = config.login_type || '',
            http_method = config.http_method || 'post',
            signUpBtn = config.signUpBtn,
            signInBtn = config.signInBtn,
            logoutBtn = config.logoutBtn;
            
        return {
            signUp: function() {
                checkBtnPara(signUpBtn);
                btn = $(getBtnPara(btn));
            },
            signIn: function() {
                checkBtnPara(signUpBtn);
                btn = $(getBtnPara(btn));
            },
            logout: function() {
                checkBtnPara(signUpBtn);
                btn = $(getBtnPara(btn));
            },
            config: config,
        }
    };
});
