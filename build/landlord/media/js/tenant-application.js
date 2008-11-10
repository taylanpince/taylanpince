/*
*	Tenant Application
*	Utility functions for the tenant application form
*	
*	Requires jQuery library (http://www.jquery.com),
*   DateJS (http://www.datejs.com)
*	
*	Taylan Pince (taylanpince at gmail dot com) - November 9, 2008
*/

$.extend($.namespace("core.TenantApplication"), {
    
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
	
	date_helper_text : "Enter a date relative to today, in a simple language<br />i.e. last year, 6 months ago, April 2008, etc.",
	date_helper_error : "Please make sure that this date is valid.",
	date_helper_box : '<div class="date-helper"></div>',
	
	init_date_pickers : function() {
	    $("li.date").each(function() {
	        $(this).find("p.help").html(core.TenantApplication.date_helper_text);
	        $(this).find("input").keyup(function() {
	            var parsed_date = Date.parse($(this).val());
	            
	            if (parsed_date == null) {
	                $(this).parent().find(".date-helper").addClass("date-invalid").removeClass("date-valid").text("");
	            } else {
	                $(this).parent().find(".date-helper").addClass("date-valid").removeClass("date-invalid").html(parsed_date.toString("MMMM d, yyyy"));
	            }
	        }).after(core.TenantApplication.date_helper_box);
	    });
	    
	    $("#TenantApplicationForm").submit(function() {
	        var validation = true;
	        
	        $("li.date-required").find("input").each(function() {
	            var parsed_date = Date.parse($(this).val());
	            
	            if (parsed_date == null) {
	                validation = false;
	                
	                if ($(this).parent().find("p.error").size() > 0) {
	                    $(this).parent().find("p.error").html(core.TenantApplication.date_helper_error);
	                } else {
	                    $(this).parent().prepend('<p class="error">' + core.TenantApplication.date_helper_error + '</p>');
	                }
	            } else {
	                $(this).val(parsed_date.toString("yyyy-MM-dd"))
	            }
	        });
	        
	        if (validation == false) {
	            alert("There were some errors in your application, please review the messages in the form.");
	        }
	        
	        return validation;
	    });
	},
    
    init : function() {
        this.init_markers();
        this.init_date_pickers();
    }
    
});

$(function() {
    core.TenantApplication.init();
});