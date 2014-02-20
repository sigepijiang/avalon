Module('blog', function(){
    this.run = function(){
        $(function() {
            $('.blog-pager-newer').hover(function(){
                $('.blog-pager-newer-arrow').css('background-position','0px -40px');
                $('.blog-pager-newer-text').css('color','.7f8284');
            }, function(){
                $('.blog-pager-newer-arrow').css('background-position','0px 0px');
                $('.blog-pager-newer-text').css('color','.b3b4b6');
            });
            
            $('.blog-pager-older').hover(function(){
                $('.blog-pager-older-arrow').css('background-position','-44px -40px');
                $('.blog-pager-older-text').css('color','.7f8284');
            }, function(){
                $('.blog-pager-older-arrow').css('background-position','-44px 0px');
                $('.blog-pager-older-text').css('color','.b3b4b6');
            });
            
            $('.social-facebook-wrap').hover(function(){
                $('.social-facebook-icon').css('background-position','0px -20px');
            }, function(){
                $('.social-facebook-icon').css('background-position','0px 0px');
            });
            
            $('.social-twitter-wrap').hover(function(){
                $('.social-twitter-icon').css('background-position','-20px -20px');
            }, function(){
                $('.social-twitter-icon').css('background-position','-20px 0px');
            });
            
            $('.social-google-wrap').hover(function(){
                $('.social-google-icon').css('background-position','-40px -20px');
            }, function(){
                $('.social-google-icon').css('background-position','-40px 0px');
            });
        });
    }
})
