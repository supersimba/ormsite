/**
 * Created by root on 17-5-31.
 */

function logs(str){
    console.log(str);
}


function setSrcSyncStatus(val) {
    console.log(val);
    switch (val)
    {
        case -1:
            return "<i class=\"fa fa-remove\" style='color: red;'></i>";
        case 0:
            return "<i class=\"fa fa-stop-circle-o\" style='color: #31b0d5;'></i>";
        case 1:
            return "<i class=\"fa fa-arrow-up\" style='color: lawngreen;'></i>";
            //return "<img src='/static/img/stop.png'></img>";
    }
}


function chkTargetConfig(ssh_status,path_status,script_status) {
    if(ssh_status==1 && path_status==1 && script_status==1)
    {
        return 1;
    }
    if(ssh_status==-1)
    {

    }
}


function setSrcSyncActive(val) {
    console.log(val);
    switch (val)
    {
        case 0:
            return "停止";
        case 1:
            return "待机";
        case 2:
            return "分析";
    }
}
function getSourceInfo(queue_id,trobj,i,trobj_plus) {
    // var dt=new Date().Format("MMdd hh:mm:ss");
    $.ajax({
                type:"POST",
                async:true,
                dataType:"json",
                data:{rid:queue_id},
                url: "/display_source_info/",
                beforeSend:function () {
                    //console.log("begin to get info from src_moni_info");
                },
                success:function (callback,status,xhr) {
                    console.log("success callback");
                    if(callback["record_flag"]=='-1')
                    {
                        trobj.css({'background':'#FFFFCC','color':'black'});
                    }
                    else
                    {
                        trobj.css({'background':'white','color':'black'});
                        if(callback["ssh_status"]==1 && callback["path_status"]==1 && callback["script_status"]==1)
                        {
                            //console.log("1111111111111111111111111111111111111");
                            // alert(callback["active"]);
                            trobj.children().eq(2).css({'color':'black','background':'white'});
                            trobj.children().eq(4).html(setSrcSyncStatus(callback["sync_status"]));
                            trobj.children().eq(5).text(setSrcSyncActive(callback["active"]));
                            trobj.children().eq(6).text(callback["add_time"].substring(4));
                            trobj_plus.children().eq(0).children().eq(0).children('#span-dbps-num').text(callback['dbps_cnt']);
                            trobj_plus.children().eq(0).children().eq(0).children('#span-vag-num').text(callback['capture_cnt']);
                            trobj_plus.children().eq(0).children().eq(0).children('#span-sender-num').text(callback['sender_cnt']);
                            trobj_plus.children().eq(0).children().eq(0).children('#span-vag-err').text(callback['capture_err']);
                            trobj_plus.children().eq(0).children().eq(0).children('#span-sender-err').text(callback['sender_err']);
                        // trobj_plus.children().eq(0).children().eq(2).children('#span-loader-time').text(callback['loader_time']);
                        }
                        else
                        {
                            if(callback["ssh_status"]==-1 || callback["path_status"]==-1)
                            {
                                trobj.children().eq(2).css({'color':'white','background':'red','font-weight':'600'});
                                trobj.children().eq(12).find('.span-link-slog').css({'color':'white','background':'red'});
                                trobj.children().eq(12).find('.span-link-slog').click(function () {
                                    return false;
                                });
                            }
                            if(callback["script_status"]==-1)
                            {
                                trobj.children().eq(3).css({'color':'white','background':'red','font-weight':'600'});
                            }
                        }
                    }



                },
                error:function (XMLResponse) {
                    console.log("数据抓取失败");
                    //console.log(XMLResponse.responseText);
                }
            });
}

function displaySourceInfo() {
    for(var i=0;i<$("tbody").children().length;i++){
        if(i%2==0){
            //console.log("i="+i);
            var trobj=$("tbody").children().eq(i);
            var trobj_plus=$("tbody").children().eq(i+1);
            queueid=trobj.children().eq(0).children().eq(1).text();
            // console.log(queueid);
            getSourceInfo(queueid,trobj,i,trobj_plus);
        }
        else {
            $("tbody").children().eq(i).css('color','rgb(98,98,143)');
        }
    }
}
$(document).ready(function () {
    setInterval(displaySourceInfo,2000);
    //displaySourceInfo();
});