$( document ).ready(function() {
    //console.log("hello world")
    getData().done(createRadarchart)


});


var btnpressed = "btn btn-default"
var btnrelased = "btn btn-default btn-outline"
var dati
var radarcond
var radarstrada

var color = Chart.helpers.color;
window.chartColors = [
  'rgb(255, 99, 132)',
   'rgb(255, 159, 64)',
   'rgb(75, 192, 192)',
 'rgb(255, 205, 86)',
   'rgb(54, 162, 235)',
   'rgb(153, 102, 255)',
   'rgb(231,233,237)'
];

function getData(){
        var endpoint = '/incidenticosenza/ajax/dashboard-meteo'
        return $.ajax({
        method:"GET",
        url:endpoint

    });
}//getData


function canvasResize(){
    canvas = document.getElementById('myChart');
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
}


function createDataset(data){

    datasets= []

    backgroundcolors = ["rgba(179,181,198,0.2)","rgba(179,181,198,0.2)",'rgb(255, 159, 64)']
    bordercolors = ["rgba(179,181,198,0.2)","rgba(255,99,132,1)",'rgb(255, 159, 64)']
    i = 0
     for (var key in data.tipocoll_strada_freq.datasets) {

            var dict = {
                      label: key,
                      fill: true,
                      backgroundColor: color(window.chartColors[i]).alpha(0.2).rgbString(),
                      borderColor:window.chartColors[i],
                      pointBorderColor: window.chartColors[i],
                      pointBackgroundColor: window.chartColors[i],
                      data: data.tipocoll_strada_freq.datasets[key]
            };

            datasets.push(dict)
            i++
        }

        console.log(datasets)

        return datasets
}



function createRadarchart(data){

   dati = data

   radarcond = new Chart(document.getElementById("myChart"), {
    type: 'radar',
    data: {
      labels: data.tipocoll_strada_freq["labels"],
      datasets:
        /*[{
          label: "1950",
          fill: true,
          backgroundColor: "rgba(179,181,198,0.2)",
          borderColor: "rgba(179,181,198,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(179,181,198,1)",
          data: [8.77,55.61,21.69,6.62,6.82]
        }, {
          label: "2050",
          fill: true,
          backgroundColor: "rgba(255,99,132,0.2)",
          borderColor: "rgba(255,99,132,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(255,99,132,1)",
          pointBorderColor: "#fff",
          data: [25.48,54.16,7.61,8.06,4.45]
        }]*/
        createDataset(data)
    },
    options: {
    /*  title: {
        display: true,
        text: 'Distribution in % of world population'
      }*/
    }
});

   $("#btncondasf").attr("class",btnpressed)
   $("#btntipostrada").attr("class",btnrelased)

}


function createRadarchart2(data){



   radarstrada = new Chart(document.getElementById("myChart"), {
    type: 'radar',
    data: {
      labels: data.tipocoll_tipostrada_freq["labels"],
      datasets:
       /* [{
          label: "1950",
          fill: true,
          backgroundColor: "rgba(179,181,198,0.2)",
          borderColor: "rgba(179,181,198,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(179,181,198,1)",
          data: [8.77,55.61,21.69,6.62,6.82]
        }, {
          label: "2050",
          fill: true,
          backgroundColor: "rgba(255,99,132,0.2)",
          borderColor: "rgba(255,99,132,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(255,99,132,1)",
          pointBorderColor: "#fff",
          data: [25.48,54.16,7.61,8.06,4.45]
        }]*/
        createDataset2(data)
    },
    options: {
      /*title: {
        display: true,
        text: 'Distribution in % of world population'
      }*/
      tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    var label = data.datasets[tooltipItem.datasetIndex].label || '';

                    console.log(data.datasets[tooltipItem.datasetIndex])
/*
                    var x = new Date(data.datasets[tooltipItem.datasetIndex].data[0]["x"])
                    var y = data.datasets[tooltipItem.datasetIndex].data[0]["y"]
                    var r = data.datasets[tooltipItem.datasetIndex].data[0]["r"]/7


                    var d = x.getDate() + "/" + parseInt(x.getMonth())+1

                    var fstart = parseInt(y)
                    var fend = fstart +2


                    console.log("##TOOLTIPS##")
                    console.log(x)
                    console.log(y)
                    console.log(r)


                    if (label) {
                        label += ': ';
                    }

                    label += "(" + d + "," + fstart + ":00-" + fend + ":00" + "," + r + ")"


                    return label;*/
                }
            }

          }//tooltips




    }
});

}


function createDataset2(data){

    datasets= []

    backgroundcolors = ["rgba(179,181,198,0.2)","rgba(179,181,198,0.2)",'rgb(255, 159, 64)']
    bordercolors = ["rgba(179,181,198,0.2)","rgba(255,99,132,1)",'rgb(255, 159, 64)']
    i = 0
     for (var key in data.tipocoll_tipostrada_freq.datasets) {

            var dict = {
                      label: key,
                      fill: true,
                      backgroundColor: color(window.chartColors[i]).alpha(0.2).rgbString(),
                      borderColor:window.chartColors[i],
                      pointBorderColor: window.chartColors[i],
                      pointBackgroundColor: window.chartColors[i],
                      data: data.tipocoll_tipostrada_freq.datasets[key]
            };

            datasets.push(dict)
            i++
        }

        console.log(datasets)

        return datasets
}




 /*  $("#btncondasf").attr("class",btnpressed)

  /* canvasResize()*/











$("#btntipostrada").click(function(){


   radarcond.destroy()

   createRadarchart2(dati)

   $("#btncondasf").attr("class",btnrelased)
   $("#btntipostrada").attr("class",btnpressed)

});




$("#btncondasf").click(function(){

   radarstrada.destroy()

   createRadarchart(dati)

   $("#btncondasf").attr("class",btnpressed)
   $("#btntipostrada").attr("class",btnreleased)




});






