
$(document).ready(function(){
    $('.side_bar').affix({
        offset: {
          top: 100
        , bottom: function () {
            return (this.bottom = $('.footer').outerHeight(true))
          }
        }
    });

    $('.input-daterange').datepicker({
        format: "yyyy年mm月dd日",
        endDate: "2014/03/04",
        language: "zh-CN",
        autoclose: true
    });
});
