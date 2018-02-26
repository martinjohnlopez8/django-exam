$('#link').click(function(){
    $.getJSON("{% url 'addressbook:testing' %}", function(data) {
        console.log(data)
    });
});