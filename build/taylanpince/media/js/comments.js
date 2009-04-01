/*
*	Comments
*	Comment submission and loading
*	
*	Requires jQuery library (http://www.jquery.com)
*	
*	Taylan Pince (taylanpince at gmail dot com) - November 25, 2008
*/

$.extend($.namespace("core.Comments"), {
    
    error_template : '<p class="%(type)">%(message)</p>',
    
    init_markdown_help : function() {
        $("#MarkdownHelp").append(' Check out the <a href="javascript:void(0);" onclick="core.Comments.launch_markdown_sheet();" id="MarkDownCheatSheetLink">cheat sheet</a> if you are not familiar.')
    },
    
    launch_markdown_sheet : function() {
        $("#MarkDownCheatSheet").fadeIn();
        
        core.scroll_to("#MarkDownCheatSheet");
    },
    
    render_comment : function(data) {
        $("#comments, #CommentsList").removeClass("hidden");
        $("#CommentsList li:last-child").removeClass("last-child");
        $("#CommentsList").append(data);
        $("#CommentsList li:last-child").addClass("last-child");
        $("#CommentForm").find("p.stand-by").fadeOut("slow");
        
        core.scroll_to("#CommentsList li:last-child");
        
        $("#CommentsListCount").text($("#CommentsList li").size());
    },
    
    parse_comment_form : function(data) {
        $("#CommentForm").find("p.stand-by").fadeOut("slow");
        
        if (data.errors) {
	        for (error in data.errors) {
	            if (error == "__all__") {
	                for (e in data.errors[error]) {
        	            $("#CommentForm").prepend(core.render_template(this.error_template, {
        	                "message" : data.errors[error][e],
        	                "type" : "error"
        	            }));
	                }
	            } else {
    	            $("#CommentForm-" + error).parent().prepend(core.render_template(this.error_template, {
    	                "message" : data.errors[error],
    	                "type" : "error"
    	            }));
	            }
	        }
	    } else {
	        if (data.notifications) {
	            for (n in data.notifications) {
	                $("#CommentForm").prepend(core.render_template(this.error_template, {
    	                "message" : data.notifications[n][1],
    	                "type" : data.notifications[n][0]
    	            }));
	            }
	        }
	        
	        if (data.comment) {
	            $("#CommentForm").prepend(core.render_template(this.error_template, {
                    "message" : "Adding your comment, please stand by.",
                    "type" : "stand-by"
                }));
                
                $.ajax({
                    url : data.comment,
                    type : "GET",
                    processData : false,
                    dataType : "html",
                    success : this.render_comment.bind(this)
                });
	        }
	        
	        $("#CommentForm").find("textarea").val("");
	    }
	    
	    $("#CommentForm").find("input[@type=submit]").attr("disabled", false);
    },
    
    submit_comment_form : function() {
        $("#CommentForm").find("p.error, p.warning, p.success, p.stand-by").fadeOut("slow");
	    $("#CommentForm").find("input[@type=submit]").attr("disabled", true);
        $("#CommentForm").prepend(core.render_template(this.error_template, {
            "message" : "Submitting your comment, please stand by.",
            "type" : "stand-by"
        }));
	    
        $.ajax({
            url : $("#CommentForm").attr("action"),
            type : "POST",
            processData : false,
            data : $("#CommentForm").serialize(),
            dataType : "json",
            contentType : "application/json",
            success : this.parse_comment_form.bind(this)
        });
        
        core.scroll_to("#add-comment");
        
        return false;
    },
    
    init : function() {
        this.init_markdown_help();
        
        $("#CommentForm").submit(this.submit_comment_form.bind(this));
    }
    
});


$(function() {
    core.Comments.init();
});
