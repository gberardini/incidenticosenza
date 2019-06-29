  $( document ).ready(function() {
    console.log("hello world")

    labels = []
    values = []
    var endpoint = '/incidenticosenza/ajax/dashboard-data'
    $.ajax({
    method:"GET",
    url:endpoint,
        success: function(data){
        labels = data.labels
        values = data.values
        console.log(data)
        console.log("successo")
        var ctx = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(ctx, {
        // The type of chart we want to create
         type: 'bar',
        // The data for our dataset
         data: {
        labels: labels,
        datasets: [{
            label: 'Numero incidenti',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: values,



        }]



        },//data

        options : {
            scales: {

                yAxes: [{

                  ticks: {
                    min: 0,
                    stepSize: 1


                  }
                }]
            }
        }//option
     })//chart





        var canvas = document.getElementById('myChart');
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
        console.log(canvas.parentElement.clientWidth)
        console.log(canvas.parentElement.clientWidth)
    },//function success
    error : function(){
        console.log("errror")

    }//function error
    });

});
