   function show()
    {
      $.ajax({
    url: '/m/update/' + email_recipient,
    type: 'GET',
    dataType: 'html',
    success: function(html){
          $("#content").html(html);
          window.location.hash = "#pos";
        },
    error: function(err) {
        console.error(err);
    }
});
    }
show();
setInterval(show, 10000);
