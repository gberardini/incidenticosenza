  $( document ).ready(function() {
    console.log("hello world")

    labels = []
    values = []
    var endpoint = '/incidenticosenza/ajax/dashboard-data'
    $.ajax({
    method:"GET",
    url:endpoint,
        success: function(data){
        labels = data.datachart_day.labels
        values = data.datachart_day.values
        console.log(data)
        console.log("successo")
        var ctx = document.getElementById('myChart');
        var ctx2 = document.getElementById('myChart2');


        var barchart = new Chart(ctx, {
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

        labels = data.mesechart.labels
        values = data.mesechart.values




        var pie = new Chart(ctx2, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: "Population (millions)",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
            data: values
          }]
        },
        options: {
          title: {
            display: true,
            //text: 'Predicted world population (millions) in 2050'
          }
        }
        });//PieChart







        var canvas = document.getElementById('myChart');
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
        console.log(canvas.parentElement.clientWidth)
        console.log(canvas.parentElement.clientWidth)




    $("#btnsettimana").click(function () {
        var username = "ciao";
        var colors = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]



        $.ajax({
        url: '/incidenticosenza/ajax/dashboard-data',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (data) {

        labels= data.datachart_month_labels

        datasets= []

        var i = 0
        for (var key in data.datachart_month_data) {

            var dict = {
                    label: key,
                    backgroundColor: colors[i],
                    data: data.datachart_month_data[key]
                    // etc.
            };

            i++
            datasets.push(dict)
        }

        console.log("dtaset")

        console.log(datasets)





           barchart.data.labels=labels
           barchart.data.datasets=datasets
           barchart.update()

        },

        error: function(data){
            alert("not nice")
        }
      });
    });





    $("#btngiorno").click(function () {


        $.ajax({
        url: '/incidenticosenza/ajax/dashboard-data',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (data) {


           barchart.data.datasets=datasets
           barchart.update()

        },

        error: function(data){
            alert("not nice")
        }
      });
    });




    },//function success
    error : function(){
        console.log("errror")

    }//function error
    });









});



