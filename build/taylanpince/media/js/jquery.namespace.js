/*
*	Name Space
*	jQuery plug-in for managing JS name spaces.
*	
*	Requires jQuery library (http://www.jquery.com)
*	
*	Taylan Pince (taylan@trapeze.com) - June 16, 2007
*/

(function($) {
    
    $.extend({
        
        namespace : function(spaces) {
            var parent_space = window;
            var namespaces = spaces.split(".");

            for (var i = 0; i < namespaces.length; i++) {
                if (typeof parent_space[namespaces[i]] == "undefined") {
                    parent_space[namespaces[i]] = new Object();
                }

                parent_space = parent_space[namespaces[i]];
            }

            return parent_space;
        }
        
    });
    
})(jQuery);
