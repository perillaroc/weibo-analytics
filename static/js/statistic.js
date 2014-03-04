
$('.side_bar').affix({
    offset: {
      top: 100
    , bottom: function () {
        return (this.bottom = $('.footer').outerHeight(true))
      }
    }
  })
