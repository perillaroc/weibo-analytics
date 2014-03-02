/* update.js */

$(document).ready(function(){
    $(".btn_update_weibo").click(function(){

        $('#process_dialog .progress_bar').removeClass("progress-bar-success");
        $('#process_dialog .modal-title').text("获取微博中...")
        $('#process_dialog .btn-success').attr("disabled","disabled")
        change_process_dialog(5);
        $("#process_dialog").modal();

        $.get("api/status/total-number",function(data,status){
            var total_number = data.total_number;
            var count_per_page = data.count;
            var page_count = Math.ceil(total_number/count_per_page);

            var current_page=1;
            var update_url = "api/status/update";
            var param = {"page": current_page,
                         "count": count_per_page};

            var current_percent = 5;
            change_process_dialog(current_percent);

            $.get(update_url,param,get_weibo);
            function get_weibo(data){
                var current_percent = parseInt(current_page/page_count*100,10).toString();
                change_process_dialog(current_percent);
                current_page++;
                if(current_page <= page_count){
                    var param = {"page": current_page,
                         "count": count_per_page};
                    $.get(update_url,param,get_weibo);
                } else {
                    $('#process_dialog .modal-body div:first').removeClass("active");
                    $('#process_dialog .progress_bar').addClass("progress-bar-success");
                    $('#process_dialog .modal-title').text("成功获取微博！")

                    $('#process_dialog .btn-success').removeAttr("disabled")
                    $('#process_dialog .btn-success').click(function(){
                        $('#process_dialog').modal('hide')
                    })
			    }
		    }
        });

        function change_process_dialog(current_percent){
            $('#process_dialog_progress_bar').attr("aria-valuenow",current_percent);
            $('#process_dialog_progress_bar').attr("style","width:"+current_percent);
            $('#process_dialog_progress_bar').attr("style","width:"+current_percent+"%");
            $('#process_dialog_progress_bar').text(current_percent+"%");
        }
    });
});

$(document).ready(function(){

});
