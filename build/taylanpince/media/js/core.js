/*
*	Core
*	Global utility functions
*	
*	Requires jQuery library (http://www.jquery.com)
*	
*	Taylan Pince (taylanpince at gmail dot com) - October 31, 2008
*/

$.extend($.namespace("core"), {
    
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
        
		//$("hr").wrap('<div class="hr"></div>');
	},
	
	render_template : function(template, values) {
        for (val in values) {
            template = template.replace("%(" + val + ")", values[val]);
        }
        
        return template;
    },
    
    scroll_to : function(obj) {
        $("html, body").animate({
            "scrollTop" : parseInt($(obj).offset().top)
        }, 250);
    },
    
    init : function() {
        this.init_markers();
    }
    
});


$(function() {
    core.init();
});
