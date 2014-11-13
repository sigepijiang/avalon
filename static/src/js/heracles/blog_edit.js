Module('blog_edit', function(){
    this.run = function(){
        $(function() {
            var editor = new EpicEditor(editorOpts);
            editor.load();
        });
    }
})

