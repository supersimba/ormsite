$(document).ready(function() {
	var links = $('.navbar-side').children('a');
	for(var m = 0; m < links.length; m++) {
		links.eq(m).bind('click', function(e) {
			console.log($(this).next('ul').length);
			if($(this).next('ul').length==1) 
			{
				if($(this).next().css('display') == 'none') 
				{
					$('.navbar-side').children('.sidebar-sub-menu').hide();
					$(this).next().show();
				} else 
				{
					$(this).next().hide();
				}
			}

		});
	}
});