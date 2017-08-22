//点击链接展开tr
function linkCollpse() {
	//取得点击链接的行号,则隐藏行行号为rownum
	var rownum = this.parentNode.parentNode.rowIndex;
	//	console.log("当前点击行："+rownum);
	//取得隐藏行 tr对象
	var trobj = document.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
	for(var m=1;m<trobj.length;m+=2)
	{
		if(m!=rownum)
		{
			trobj[m].style.display="none";		
		}
	}
	if(trobj[rownum].style.display=="none") 
	{
		trobj[rownum].style.display = "";
		console.log(trobj[rownum].childNodes[0].nodeName);
	} 
	else
	{
		trobj[rownum].style.display = "none";
	}
}


window.onload = function() {
	$('.td-yc').css("display", "none");
	var links = document.getElementsByClassName("link-collose");
	//为每个链接添加事件
	for(var i = 0; i < links.length; i++) 
	{
		//console.log(i);
		links[i].addEventListener("click", linkCollpse, true);
	}
}