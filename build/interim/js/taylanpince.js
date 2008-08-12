/*
*	Taylan Pince
*	Utility functions for taylanpince.com
*	
*	Requires jQuery library (http://www.jquery.com)
*	
*	Taylan Pince (taylanpince@gmail.com) - June 20, 2008
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
	
	header_call : "",
	
	init_header : function() {
	    this.header_call = $("#HeaderCall").html();
	    
	    $("#Header").find("a").hover(function() {
	        $("#HeaderCall").animate({"opacity": 0}, {"complete": function() {
	            $("#HeaderCall").html('home <span class="arrow">&raquo;</a>').animate({"opacity": 1}, {"duration": "normal", "queue": true});
	        }, "duration": "normal", "queue": true});
	    }, function() {
	        $("#HeaderCall").animate({"opacity": 0}, {"complete": function() {
	            $("#HeaderCall").html(core.TaylanPince.header_call).animate({"opacity": 1}, {"duration": "normal", "queue": true});
	        }, "duration": "normal", "queue": true});
	    });
	},
	
	init_comments : function() {
	    if ($("#CommentForm").size() > 0) {
	        $("#MarkDownCheatSheetLink").click(function() {
	            $("#MarkDownCheatSheet").fadeIn();
	        }).attr("href", "javascript:void(0);");
	    }
	},
    
    init : function() {
        this.init_markers();
        this.init_header();
        this.init_comments();
    }
    
});

$(function() {
    core.TaylanPince.init();
});