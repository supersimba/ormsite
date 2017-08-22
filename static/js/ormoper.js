/**
 * Created by root on 17-6-12.
 */

function showMask() {
    $('#div-mask').css("height",$(document).height());
    $('#div-mask').css("width",$(document).width());
    $('#div-mask').show();
}
function hideMask() {
    $('#div-mask').hide();
}


$(document).ready(function () {
//
    var src_ip=$('#div-src-dbinfo').children('span').eq(0).text();
    var src_path=$('#div-src-dbinfo').children('span').eq(1).text();
    var src_u=$('#div-src-dbinfo').children('span').eq(2).text();
    var src_p=$('#div-src-dbinfo').children('span').eq(3).text();
    var tgt_ip=$('#div-tgt-dbinfo').children('span').eq(0).text();
    var tgt_path=$('#div-tgt-dbinfo').children('span').eq(1).text();
    var tgt_u=$('#div-tgt-dbinfo').children('span').eq(2).text();
    var tgt_p=$('#div-tgt-dbinfo').children('span').eq(3).text();

    // $('#div-mask').hide();
    hideMask();

    $('#btn-src-clean').bind('click',function () {
        // src clean
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':src_ip,'path':src_path,'u':src_u,'p':src_p,'runflag':3},
        url: "/sync_oper/",
        beforeSend:function () {
            var c=window.confirm('是否清除源端缓存?(清除缓存前需要停止进程)');
            if(c!=true)
            {
                return false;
            }
        },
        success:function (callback) {
            // alert(callback);
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });

    });

    $('#btn-tgt-clean').bind('click',function () {
        // tgt clean
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':tgt_ip,'path':tgt_path,'u':tgt_u,'p':tgt_p,'runflag':3},
        url: "/sync_oper/",
        beforeSend:function () {
            var c=window.confirm('是否清除目标端缓存?(清除缓存前需要停止进程)');
            if(c!=true)
            {
                return false;
            }
        },
        success:function (callback) {
            // alert(callback);
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });

    });

    $('#btn-src-startup').bind('click',function () {
        //    SRC启动  进程
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':src_ip,'path':src_path,'u':src_u,'p':src_p,'runflag':1},
        url: "/sync_oper/",
        beforeSend:function () {
          alert('启动进程');
        },
        success:function (callback) {
            // alert(callback);
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });
    });

    $('#btn-src-stop').bind('click',function () {
    //    SRC停止 进程
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':src_ip,'path':src_path,'u':src_u,'p':src_p,'runflag':2},
        url: "/sync_oper/",
        success:function (callback) {
            // alert(callback);
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });
    });

    $('#btn-tgt-startup').bind('click',function () {
        //    tgt启动  进程
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':tgt_ip,'path':tgt_path,'u':tgt_u,'p':tgt_p,'runflag':1},
        url: "/sync_oper/",
        beforeSend:function () {
          alert('启动目标端进程');
        },
        success:function (callback) {
            // alert(callback);
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });
    });

    $('#btn-tgt-stop').bind('click',function () {
    //    tgt停止 进程
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':tgt_ip,'path':tgt_path,'u':tgt_u,'p':tgt_p,'runflag':2},
        url: "/sync_oper/",
        success:function (callback) {
            // alert(callback);
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });
    });

    $('#btn-src-chk').bind('click',function () {
    //    执行进程检查
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':src_ip,'path':src_path,'u':src_u,'p':src_p,'runflag':0},
        url: "/sync_oper/",
        success:function (callback) {
            // alert(callback);
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });
    });

    $('#btn-tgt-chk').bind('click',function () {
    //    执行进程检查
        $.ajax({
        type:"POST",
        async:false,
        dataType:"text",
        data:{'ip':tgt_ip,'path':tgt_path,'u':tgt_u,'p':tgt_p,'runflag':0},
        url: "/sync_oper/",
        success:function (callback) {
            $('.div-cmd-display').html(callback);
            // document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        }
        });
    });
    // btn-src-dic------set dict导出 对象
    $('#btn-src-dic').bind('click',function () {
    //    执行进程检查
        $.ajax({
        type:"POST",
        async:true,
        dataType:"text",
        data:{'ip':src_ip,'path':src_path,'u':src_u,'p':src_p,'runflag':4},
        url: "/sync_oper/",
        beforeSend:function () {
            var c=window.confirm('源端vman导出对象?');
            if(c!=true)
            {
                return false;
            }
            else
            {
                showMask();
            }
        },
        success:function (callback) {
            hideMask();
            $('.div-cmd-display').html(callback);
            document.getElementById('id-cmd-display').scrollTop=document.getElementById('id-cmd-display').scrollHeight;
        },
        error:function (callback) {
            $('.div-cmd-display').html('操作出错')
        },
            completed:function () {
                hideMask();
            }
        });
    });

    // btn-src-fullsync src全同步数据
    $('#btn-src-fullsync').bind('click',function () {
    //    执行进程检查
        $.ajax({
        type:"POST",
        async:true,
        dataType:"text",
        data:{'ip':src_ip,'path':src_path,'u':src_u,'p':src_p,'runflag':5},
        url: "/sync_oper/",
        beforeSend:function () {
            var c=window.confirm('开始导出数据?');
            if(c!=true)
            {
                return false;
            }
            else
            {
                showMask();
            }
        },
        success:function (callback) {
            hideMask();
            $('.div-cmd-display').html(callback);
            document.getElementById('id-cmd-display').scrollTop=document.getElementById('id-cmd-display').scrollHeight;
        },
        error:function (callback) {
            hideMask();
            $('.div-cmd-display').html('操作出错');
        },
        complete:function () {
                hideMask();
            }
        });
    });

    $('#btn-edit-mapping').bind('click',function () {
    //    edit mapping.ini
        $.ajax({
        type:"POST",
        async:true,
        dataType:"text",
        data:{'ip':src_ip,'path':src_path,'u':src_u,'p':src_p,'runflag':6},
        url: "/sync_oper/",
        beforeSend:function () {
            var c=window.confirm('编辑同步表配置文件?');
            if(c!=true)
            {
                return false;
            }
            else
            {
                $('#div-zhezao').show();
            }
        },
        success:function (callback) {
            $('#edit-block').html(callback);
            document.getElementById('id-cmd-display').scrollTop=document.getElementById('id-cmd-display').scrollHeight;
        },
        error:function (callback) {
            // hideMask();
            $('.div-cmd-display').html('操作出错');
        },
        complete:function () {
                // $('#div-edit-block').hide();
            }
        });
    });

    $('#btn-edit').bind('click',function () {
        alert('功能后面版本开发!');
        $('#div-edit-block').hide();
    });

    $('#btn-edit-exit').bind('click',function () {
        $('#div-edit-block').hide();
    });
});