/**
 * Created by root on 17-6-7.
 */

function chkProcess(ip,path,u,p)
{
    $.ajax({
        type:"POST",
        async:true,
        dataType:"text",
        data:{'ip':ip,'path':path,'u':u,'p':p},
        url: "/check_process/",
        success:function (callback) {
            // alert(callback);
            // document.write(callback);
            $('#div-display-log').html(callback)
        },
        error:function (callback) {
            $('#div-display-log').html('进程查看出错')
        }
    });
}


function getSyncLogs(ip,path,u,p,logname) {
    $.ajax({
        type:"POST",
        async:true,
        dataType:"text",
        data:{'ip':ip,'path':path,'u':u,'p':p,'logname':logname},
        url: "/display_log/",
        success:function (callback) {
            $('#div-display-log').html(callback);
            document.getElementById('div-display-log').scrollTop=document.getElementById('div-display-log').scrollHeight;
        },
        error:function (callback) {
            $('#div-display-log').html('日志查看出错')
        }
    });
}

$(document).ready(function () {
    //查看源端进程
    $('#btn-chk-src-pro').bind('click',function () {
        ip=$('.div-dbinfo').find('.span-dbinfo-ip').text();
        path=$('.div-dbinfo').find('.span-dbinfo-path').text();
        u=$('.div-dbinfo').find('.span-dbinfo-u').text();
        p=$('.div-dbinfo').find('.span-dbinfo-p').text();
        chkProcess(ip,path,u,p);
    });
    //查看T端进程
    $('#btn-chk-tgt-pro').bind('click',function () {
        ip=$('.div-dbinfo').find('.span-dbinfo-ip').text();
        path=$('.div-dbinfo').find('.span-dbinfo-path').text();
        u=$('.div-dbinfo').find('.span-dbinfo-u').text();
        p=$('.div-dbinfo').find('.span-dbinfo-p').text();
        chkProcess(ip,path,u,p);
    });
    // #查看vagentd日志
    $('#btn-vag-log').bind('click',function () {
        ip=$('.div-dbinfo').find('.span-dbinfo-ip').text();
        path=$('.div-dbinfo').find('.span-dbinfo-path').text();
        u=$('.div-dbinfo').find('.span-dbinfo-u').text();
        p=$('.div-dbinfo').find('.span-dbinfo-p').text();
        getSyncLogs(ip,path,u,p,'log.vagentd');
    });
    // 查看sender日志
    $('#btn-snd-log').bind('click',function () {
        ip=$('.div-dbinfo').find('.span-dbinfo-ip').text();
        path=$('.div-dbinfo').find('.span-dbinfo-path').text();
        u=$('.div-dbinfo').find('.span-dbinfo-u').text();
        p=$('.div-dbinfo').find('.span-dbinfo-p').text();
        getSyncLogs(ip,path,u,p,'log.sender');
    });

    var links_logs=$('.dropdown-logs-menu').find('a');

    for(var m=0;m<links_logs.length;m++)
    {
        links_logs.eq(m).bind('click',function (e) {
            var logname="log."+$(this).text();
            ip=$('.div-dbinfo').find('.span-dbinfo-ip').text();
            path=$('.div-dbinfo').find('.span-dbinfo-path').text();
            u=$('.div-dbinfo').find('.span-dbinfo-u').text();
            p=$('.div-dbinfo').find('.span-dbinfo-p').text();
            getSyncLogs(ip,path,u,p,logname);
        });
    }

    var links_logr=$('.dropdown-logr-menu').find('a');

    for(var m=0;m<links_logr.length;m++)
    {
        links_logr.eq(m).bind('click',function (e) {
            var logname="log."+$(this).text();
            ip=$('.div-dbinfo').find('.span-dbinfo-ip').text();
            path=$('.div-dbinfo').find('.span-dbinfo-path').text();
            u=$('.div-dbinfo').find('.span-dbinfo-u').text();
            p=$('.div-dbinfo').find('.span-dbinfo-p').text();
            getSyncLogs(ip,path,u,p,logname);
        });
    }
});
