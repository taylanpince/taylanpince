/*
*	Comments
*	Comment submission and loading
*	
*	Requires jQuery library (http://www.jquery.com)
*	
*	Taylan Pince (taylanpince at gmail dot com) - November 25, 2008
*/

$.extend($.namespace("core.Comments"), {
    
    init_markdown_help : function() {
        $("#MarkdownHelp").append(' Check out the <a href="javascript:void(0);" onclick="core.Comments.launch_markdown_sheet();" id="MarkDownCheatSheetLink">cheat sheet</a> if you are not familiar.')
    },
    
    launch_markdown_sheet : function() {
        $("#MarkDownCheatSheet").fadeIn();
    },
    
    init_markdown_form : function() {
        
    },
    
    init : function() {
        this.init_markdown_form();
        this.init_markdown_help();
    }
    
});


$(function() {
    core.Comments.init();
});
