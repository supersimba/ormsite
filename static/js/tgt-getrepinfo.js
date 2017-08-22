/**
 * ormmoni页面提取数据库监控数据
 */

function logs(str){
    console.log(str);
}


function setSyncStatus(val) {
    switch (val)
    {
        case -1:
            return "<i class=\"fa fa-remove\" style='color: red;'></i>";
        case 0:
            return "<i class=\"fa fa-stop-circle-o\" style='color: #31b0d5;'></i>";
        case 1:
            return "<i class=\"fa fa-arrow-up\" style='color: lawngreen;'></i>";
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


function setSyncActive(val) {
    switch (val)
    {
        case -1:
            return "进程异常";
        case 0:
            return "停止";
        case 1:
            return "待机";
        case 2:
            return "全量";
        case 3:
            return "增量";
    }
}
function getTargetInfo(queue_id,trobj,i,trobj_plus) {
    $.ajax({
                type:"POST",
                async:true,
                dataType:"json",
                data:{rid:queue_id},
                url: "/display_target_info/",
                beforeSend:function () {
                    console.log("begin to get info");
                },
                success:function (callback,status,xhr) {
                    if(callback["record_flag"]=='-1')
                    {
                        trobj.css({'background':'#FFFFCC','color':'black'});
                    }
                    else
                    {
                        if(callback["ssh_status"]==1 && callback["path_status"]==1 && callback["script_status"]==1)
                        {
                            trobj.css({'background':'white','color':'black'});
                            trobj.children().eq(9).html(setSyncStatus(callback["sync_status"]));
                            trobj.children().eq(10).text(setSyncActive(callback["active"]));
                            trobj.children().eq(11).text(callback["add_time"].substring(4));
                            trobj_plus.children().eq(0).children().eq(2).children('#span-vagnum').text(callback['collect_cnt']);
                            trobj_plus.children().eq(0).children().eq(2).children('#span-vagnum-err').text(callback['collect_err']);
                            trobj_plus.children().eq(0).children().eq(2).children('#span-loader-rate').text(callback['loader_rate']);
                            trobj_plus.children().eq(0).children().eq(2).children('#span-loader-s').text(callback['loader_s_cnt']);
                            trobj_plus.children().eq(0).children().eq(2).children('#span-loader-err').text(callback['loader_err']);
                            trobj_plus.children().eq(0).children().eq(2).children('#span-loader-time').text(callback['loader_time']);
                        }
                        else
                        {
                            if(callback["ssh_status"]==-1 || callback["path_status"]==-1)
                            {
                                trobj.children().eq(7).css({'color':'white','background':'red','font-weight':'600'});
                                trobj.children().eq(12).find('.span-link-tlog').css({'color':'white','background':'red'});
                                trobj.children().eq(12).find('.span-link-tlog').click(function () {
                                    return false;
                                });
                            }
                            if(callback["script_status"]==-1)
                            {
                                trobj.children().eq(8).css({'color':'white','background':'red','font-weight':'600'});
                            }
                        }
                    }

                },
                error:function (callback) {
                    console.log("数据抓取失败");
                    console.log(callback);
                }
            });
}

function displayTargetInfo() {
    for(var i=0;i<$("tbody").children().length;i++){
        if(i%2==0){            console.log("i="+i);
            var trobj=$("tbody").children().eq(i);
            var trobj_plus=$("tbody").children().eq(i+1);
            queueid=trobj.children().eq(0).children().eq(1).text();
            console.log("queue_id="+queueid);
            console.log(trobj.children().eq(1).text());
            console.log(trobj);
            getTargetInfo(queueid,trobj,i,trobj_plus);
        }
        else {
            $("tbody").children().eq(i).css('color','rgb(98,98,143)');
        }
    }
}
$(document).ready(function () {
    $("tbody").find('span.span-info').css({'font-size':'16px','color':'rgb(14,144,210)'});
    setInterval(displayTargetInfo,2000);
});