$(function(){
    $('input[name="upload"]').click(function(){
        avalon.ajaxupload.upload(
            '/apis/aphrodite/image.json', 
            $('input[name="image"]')
        );
    });
})
