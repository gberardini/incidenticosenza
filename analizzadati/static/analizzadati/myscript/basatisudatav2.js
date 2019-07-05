$( document ).ready(function() {
    //console.log("hello world")
    getData().done(createBarchart,createPiechart)
});


var barchart;

function getData(){
        var endpoint = '/incidenticosenza/ajax/dashboard-data'
        return $.ajax({
        method:"GET",
        url:endpoint

    });
}//getData




function createBarchart(data){
        labels = []
        values = []
        labels = data.datachart_day.labels
        values = data.datachart_day.values
        console.log(data)
        console.log("successo")
        var ctx = document.getElementById('myChart');

        barchart = new Chart(ctx, {
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
}


function createPiechart(data){
    labels = data.mesechart.labels
    values = data.mesechart.values
    var ctx2 = document.getElementById('myChart2');
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
        })//PieChart


}

function weekview(data){
        var colors = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]
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

          // var barchart = document.getElementById('myChart');

           barchart.data.labels=labels
           barchart.data.datasets=datasets
           barchart.update()

}



function daysview(data){
    barchart.destroy()
    createBarchart(data)

}


$("#btnsettimana").click(function () {

        getData().done(weekview)

    });



$("#btngiorno").click(function () {
        getData().done(daysview)
});

/*

        var canvas = document.getElementById('myChart');
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
        console.log(canvas.parentElement.clientWidth)
        console.log(canvas.parentElement.clientWidth)

*/





