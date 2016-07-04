var helloRequest = (function($){
   var data = [{
       path: '/requests/',
       method: 'GET',
       date: '2016-07-04'
   }, 
   {
       path: '/requests/',
       method: 'GET',
       date: '2016-07-04'
   },
   {
       path: '/requests/',
       method: 'GET',
       date: '2016-07-04'
   }];
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
   var pre_titile = '(3) ';
   $('#request').find('tbody').html(items);
   $('td').addClass('text-center');
   $('th').addClass('text-center');
   $('title').text(pre_titile + title);
}

 return {
     loadRequest: function(){
        
        handleRequest(data);
       
     }
};
})(jQuery);


$(document).ready(function(){
    helloRequest.loadRequest();
});
