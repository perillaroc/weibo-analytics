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
    $('#time_interval_group').children('label').on('click', function (event) {
        update_chart({
            time_interval: $(this).children('input').first().val()
        })
    });

    $('#time_range_submit_button').click(function(event){
        update_chart();
    });

    function update_chart(){
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();

        if(arguments[0])
        {
            var update_chart_options = arguments[0];
            if('start_date' in update_chart_options)
                start_date = update_chart_options.start_date;
            if('end_date' in update_chart_options)
                end_date = update_chart_options.end_date;
        }

        if(!start_date || !end_date || start_date>end_date ){
            alert("请输入正确日期范围！");
            return;
        }

        // get records from API
        param = {
            "start_date": start_date,
            "end_date": end_date
        };
        $.get('/api/statistic/punchcard',param,function(data){
            var x_categories = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'];
            var y_categories =['凌晨', '上午', '下午', '晚上'];
            var series_data = [];
            $.each(data.record, function(a_key, a_data){
                var a_point=[a_data.weekday, a_data.hour_type, a_data.count];
                series_data.push(a_point);
            });

            var x_tick_interval = 1;

            $('#main_chart_container').highcharts({
                chart: {
                    type: 'bubble',
                    zoomType:'xy'
                },
                title: {
                    text: '卡片'
                },
                xAxis: {
                    categories: x_categories
                },
                yAxis: {
                    categories: y_categories
                },
                series: [{
                    data: series_data
                }]
            });
        });
    }

    $("#time_range_submit_button").trigger("click");
});