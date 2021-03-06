/* update.js */

$(document).ready(function(){
    $(".btn_update_weibo").click(function(){

        var process_dialog = $('#process_dialog');
        process_dialog.find('.progress-bar').removeClass().addClass("progress-bar");
        process_dialog.find('.modal-title').text("获取微博中...");
        process_dialog.find('.modal-footer').empty();
        process_dialog.find('.modal-footer').append(
            "<button type=\"button\" class=\"btn btn-success\">确定</button>"
        )
        process_dialog.find('.btn-success').attr("disabled","disabled");
        change_process_dialog(5);
        $("#process_dialog").modal();

        $.get("api/status/total-number")
            .done(function(data,status){
                var total_number = data.total_number;
                var count_per_page = data.count;
                var page_count = Math.ceil(total_number/count_per_page);

                var current_page=1;
                var update_url = "api/status/update";
                var param = {"page": current_page,
                             "count": count_per_page};

                var current_percent = 5;
                change_process_dialog(current_percent);

                $.get(update_url,param)
                    .done(get_weibo)
                    .fail(get_weibo_failed);


                function get_weibo(data){
                    var current_percent = parseInt(current_page/page_count*100,10).toString();
                    change_process_dialog(current_percent);
                    current_page++;
                    if(current_page <= page_count){
                        var param = {"page": current_page,
                             "count": count_per_page};
                        $.get(update_url,param)
                            .done(get_weibo)
                            .fail(get_weibo_failed);
                    } else {
                        get_weibo_successed();
                    }
                }
            })
            .fail(get_weibo_failed);

        function get_weibo_failed(jqXHR, textStatus, errorThrown){
            process_dialog.find('.modal-body div:first').removeClass("active");
                process_dialog.find('.progress_bar').addClass("progress-bar-danger");
                process_dialog.find('.modal-title').text("获取微博失败！");
                change_process_dialog(100);

                process_dialog.find('.btn-success').removeAttr("disabled");
                process_dialog.find('.btn-success').click(function(){
                    process_dialog.modal('hide');
                })
        }

        function get_weibo_successed(){
            process_dialog.find('.modal-body div:first').removeClass("active");
            process_dialog.find('.progress-bar').addClass("progress-bar-success");
            process_dialog.find('.modal-title').text("成功获取微博！");

            process_dialog.find('.btn-success').removeAttr("disabled");
            process_dialog.find('.modal-footer').append("<a href=\"/statistic\" " +
                "class=\"btn btn-primary\" data-toggle=\"tooltip\" title=\"分析已抓取的微博\">进入下一步</button>")
                .tooltip({
                    selector: "[data-toggle=tooltip]",
                    container: 'body'
                })
            process_dialog.find('.btn-success').click(function(){
                process_dialog.modal('hide');
            })
        }

        function change_process_dialog(current_percent){
            var process_dialog_progress_bar = $('#process_dialog_progress_bar');
            process_dialog_progress_bar.attr("aria-valuenow",current_percent);
            process_dialog_progress_bar.attr("style","width:"+current_percent);
            process_dialog_progress_bar.attr("style","width:"+current_percent+"%");
            process_dialog_progress_bar.text(current_percent+"%");
        }
    });
});

$(document).ready(function(){

});
