$( document ).ready(function() {
    //console.log("hello world")
    /*getData().done(testPost)*/
     var endpoint = '/incidenticosenza/ajax/dashboard-conducenti'
     $.ajax({
        method:"GET",
        url:endpoint,
        success:function(data){
              alert("hi")
        },
        error:function(data){
            alert("neg")
        }

    });
    /*getData().done(createPiechart)*/
});
