
$(document).ready(function(){
    $('.side_bar').affix({
        offset: {
          top: 100
        , bottom: function () {
            return (this.bottom = $('.footer').outerHeight(true))
          }
        }
    });

    var today = new Date();
    var end_date = today.getFullYear()+"-"+(today.getMonth()+1)+"-"+today.getDate();
    $('.input-daterange').datepicker({
        format: "yyyy-mm-dd",
        endDate: end_date,
        language: "zh-CN",
        autoclose: true
    });
});

$(document).ready(function(){
    $("#time_range_submit_button").click(function(){
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();
        var time_interval;
        time_interval = $('#time_interval_group .active input').val();
        if(!start_date || !end_date || start_date>end_date || !time_interval){
            alert("请输入正确日期范围！");
            return;
        }
        console.log("Require date from " + start_date + " to "+ end_date +
            " interval by "+ time_interval);
    });
});