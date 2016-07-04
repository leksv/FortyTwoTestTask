var helloRequest = (function($){

  var items = [];
  function handleRequest(data) {
    $.each(data, function(i, val) {
        items.push('<tr>'
                    + '<td>' + val.path + '</td>'
                    + '<td>' + val.method + '</td>'
                    + '<td>' + val.date + '</td>'
                    + '</tr>'
        );
        
   });
   var title = $('title').text().split(')')[1] || $('title').text();
   var pre_titile = '';
   $('#request').find('tbody').html(items);
   $('td').addClass('text-center');
   $('th').addClass('text-center');
   $('title').text(pre_titile + title);
}

 return {
    loadRequest: function(){
         $.ajax({
            url: '/requests_ajax/',
            dataType : "json",
            success: function(data, textStatus) {
                handleRequest(data);
            },
            error: function(jqXHR) {
                console.log(jqXHR.responseText);
            }
         });
     }
};
})(jQuery);


$(document).ready(function(){
    helloRequest.loadRequest();
});
