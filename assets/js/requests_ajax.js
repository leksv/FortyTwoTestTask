var helloRequest = (function($){

  function handleRequest(data) {

    var items = [];
    var id = data[0];
    console.log(data[1]);
    $.each(JSON.parse(data[1]), function(i, val) {
        items.push('<tr>'
                    + '<td class="path">' + val.fields.path + '</td>'
                    + '<td>' + val.fields.method + '</td>'
                    + '<td>' + val.fields.date + '</td>'
                    + '</tr>'
        );
        
   });
   var title = $('title').text().split(')')[1] || $('title').text();
   var pre_titile = id ? '(' + id + ') ' : '';
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
    setInterval(helloRequest.loadRequest, 50);
});
