/* hello */

$(document).ready(function(){
    $(".btn_update_weibo").click(function(){
        $.get("api/status/total-number",function(data,status){
            var total_number = data.total_number
            var count_per_page = data.count
            var page_count = Math.ceil(total_number / count_per_page)

            var current_page=1
            var update_url = "api/status/update"
            var param = {"page": current_page,
                         "count": count_per_page};
            $.get(update_url,param,get_weibo);
            function get_weibo(data){
                current_page++;
                if(current_page <= page_count){
                    var param = {"page": current_page,
                         "count": count_per_page};
                    $.get(update_url,param,get_weibo);
                    console.log("current page:", current_page/page_count)
                } else {
                    console.log("finish")
			    }
		    }

        });
    })
})
