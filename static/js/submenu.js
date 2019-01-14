function showsubmenu(){
	$("#mainSubmenu").show();
	$("#mainSubmenu").bind("mouseleave", function(){$("#mainSubmenu").hide();});
}
function showsubmenuCAU(){
	$("#mainSubmenuCAU").show();
	$("#mainSubmenuCAU").bind("mouseleave", function(){$("#mainSubmenuCAU").hide();});
}


$(document).ready(function(){
	$("#reportes").bind("mouseover",showsubmenu);
	
});


$(document).ready(function(){
	$("#otcau").bind("mouseover",showsubmenuCAU);
	
});

