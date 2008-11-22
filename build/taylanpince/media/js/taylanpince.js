/*
*	Taylan Pince
*	Utility functions for taylanpince.com
*	
*	Requires jQuery library (http://www.jquery.com)
*	
*	Taylan Pince (taylanpince at gmail dot com) - June 20, 2008
*/

$.extend($.namespace("core.TaylanPince"), {
    
    init_markers : function() {
		$("html").addClass("has-js");
		
		$("li:last-child").addClass("last-child");
		$("li:first-child").addClass("first-child");
        
		$("input[@type=text]").addClass("text");
		$("input[@type=submit], input[@type=button]").addClass("submit");
		$("input[@type=password]").addClass("text");
		$("input[@type=file]").addClass("file");
		$("input[@type=radio]").addClass("radio");
		$("input[@type=checkbox]").addClass("checkbox");
		$("input[@type=image]").addClass("image");
        
		$("hr").wrap('<div class="hr"></div>');
	},
    
    init : function() {
        this.init_markers();
    }
    
});


$(function() {
    core.TaylanPince.init();
});
