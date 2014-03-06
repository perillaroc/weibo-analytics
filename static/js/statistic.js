
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
    var one_month_day = new Date();
    one_month_day.setDate(today.getDate() - new Date(today.getFullYear(), today.getMonth()+1, 0).getDate());

    $('.input-daterange').datepicker({
        format: "yyyy-mm-dd",
        startDate: "2009-01-01",
        endDate: end_date,
        language: "zh-CN",
        autoclose: true
    });

    $('#start_date').val(one_month_day.getFullYear()+"-"+
        (one_month_day.getMonth()+1)+"-"+
        one_month_day.getDate());
    $('#end_date').val(end_date);
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

        // get records from API
        param = {
            "start_date": start_date,
            "end_date": end_date,
            "time_interval": time_interval
        }
        $.get('/api/statistic/status-count',param,function(data){
            console.log(data);

            var x_categories = new Array();
            var series_data = new Array();
            $.each(data.record, function(a_key, a_data){
                x_categories.push(a_data.date);
                series_data.push(a_data.count);
            });

            var x_tick_interval = 1;
            if(data.time_interval=="day")
                x_tick_interval = 10;
            else
                x_tick_interval = 1;

            $('#chart_container').highcharts({
                chart: {
                    type: 'line'
                },
                title: {
                    text: '统计'
                },
                xAxis: {
                    categories: x_categories,
                    tickInterval: x_tick_interval
                },
                yAxis: {
                    title: {
                        text: '发微博数'
                    },
                    min: 0
                },
                series: [{
                    name: '微博数',
                    data: series_data,
                    showInLegend: false
                }]
            });
        });

    });

    $("#time_range_submit_button").trigger("click");
});