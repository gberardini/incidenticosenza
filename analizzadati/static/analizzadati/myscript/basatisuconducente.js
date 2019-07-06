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



/*var barchart;



$( document ).ready(function() {
    //console.log("hello world")
    getData().done(testPost)


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

    /*getData().done(createPiechart)
});

*/


/*function getData(){
        var endpoint = '/incidenticosenza/ajax/dashboard-conducenti'
        return $.ajax({
        method:"GET",
        url:endpoint
        success:function(data){
              alert("hi")
        },
        error:function(data){
            alert("neg")
        }

    });
}//getData



function testPos(){

    alert("hi")

}



function testNeg(){

    alert("neg")
}





function createPiechart(data){


    new Chart(document.getElementById("Piechart-Oltre 60"), {
    type: 'pie',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: [2478,5267,734,784,433]
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Predicted world population (millions) in 2050'
      }
    }
});





}
*/
