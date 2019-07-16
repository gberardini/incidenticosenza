$( document ).ready(function() {
    //console.log("hello world")
    getData().done(createBarchart,canvasResize,createPiechart)
  /*  getData().done(canvasResize)
    getData().done(createPiechart)
    getData().done(createBubblechart)*/

});


/*var barchart;*/

var dougchart
var dati
/*var barchart;*/

var btnpressed = "btn btn-default"
var btnreleased = "btn btn-default btn-outline"
var color = Chart.helpers.color;
var colors = [

"#8FB4D9",
"#67CAE8",
"#FFF59A",
"#FF716E",
"#45DEE0",
"#67EEC1",
"#8B7356",
"#BE6C6F",
"#E49D22",
"#43698B",
"#1C4766",
"#6E3B00",
"#FF716E"




]

function getData(){
        var endpoint = '/incidenticosenza/ajax/dashboard-conducenti'
        return $.ajax({
        method:"GET",
        url:endpoint

    });
}//getData


function f1(data){

  console.log(data["datachart_Oltre 60"])

}



function canvasResize(){
    canvas = document.getElementById('myChart2');
   /* canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientWidth;*/
}


function getNum(stringa){
  var ris = stringa.match(/^\d+|\d+\b|\d+(?=\w)/g)[0]
  return ris;
}


function getBubbleDataset(data){

  datasets= []

        var i = 0
        for (var fasciaA in data.fascia_fascia_freq) {
            console.log(fasciaA)
            var s = fasciaA.match(/^\d+|\d+\b|\d+(?=\w)/g)[0];
            console.log("replacing")
            console.log(s)
            for (var fasciaB in data.fascia_fascia_freq[fasciaA]) {
               console.log(data.fascia_fascia_freq[fasciaA][fasciaB])
            var dict = {
                    label: fasciaA,
                    backgroundColor: "rgba(255,221,50,0.2)",
                    borderColor: "rgba(255,221,50,1)",
                    data:[{
                     x : fasciaA.match(/^\d+|\d+\b|\d+(?=\w)/g)[0],
                     y:  fasciaB.match(/^\d+|\d+\b|\d+(?=\w)/g)[0],
                     r: parseInt(data.fascia_fascia_freq[fasciaA][fasciaB])*7
                    }]
                    // etc.
            };
            /*console.log(dict)*/
            i++
            datasets.push(dict)
          }

        }

    return datasets

}


function createBubblechart(data){
  console.log("createBubblechart ")
  datasets = getBubbleDataset(data)
  console.log(datasets)
  new Chart(document.getElementById("myChart3"), {
    type: 'bubble',
    data: {
      labels: "Africa",
      datasets:

        datasets
       /* [{
          label: ["China"],
          backgroundColor: "rgba(255,221,50,0.2)",
          borderColor: "rgba(255,221,50,1)",
          data: [{
            x: 21269017,
            y: 5.245,
            r: 15
          }]
        }, {
          label: ["Denmark"],
          backgroundColor: "rgba(60,186,159,0.2)",
          borderColor: "rgba(60,186,159,1)",
          data: [{
            x: 258702,
            y: 7.526,
            r: 10
          }]
        }, {
          label: ["Germany"],
          backgroundColor: "rgba(0,0,0,0.2)",
          borderColor: "#000",
          data: [{
            x: 3979083,
            y: 6.994,
            r: 15
          }]
        }, {
          label: ["Japan"],
          backgroundColor: "rgba(193,46,12,0.2)",
          borderColor: "rgba(193,46,12,1)",
          data: [{
            x: 4931877,
            y: 5.921,
            r: 15
          }]
        }
        ]*/
    },
    options: {
      title: {
        display: true,
        text: 'Predicted world population (millions) in 2050'
      }, scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: "Happiness",

          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: "GDP (PPP)",

          } , ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, values) {
                        console.log("###ticks#####")
                        return 'oo' + value;
                    }
                }
        }]
      },

      tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    var label = data.datasets[tooltipItem.datasetIndex].label || '';

                    var x = data.datasets[tooltipItem.datasetIndex].data[0]["x"]
                    var y = data.datasets[tooltipItem.datasetIndex].data[0]["y"]
                    var r = data.datasets[tooltipItem.datasetIndex].data[0]["r"]/7




                    console.log(data.datasets[tooltipItem.datasetIndex].data[0]["x"])
                    /*console.log(tooltipItem.yLabel)
                    console.log(tooltipItem.rLabel)*/

                    if (label) {
                        label += ': ';
                    }
                    /*label += Math.round(tooltipItem.yLabel * 100) / 100;*/
                    label += "(" + x + "," + y + "," + r + ")"


                    return label;
                }
            }

          }//tooltips
    }//options
});

}






function createBarchart(data){

      dati = data
      barchart = new Chart(document.getElementById("myChart"), {
          type: 'horizontalBar',
          data: {
            labels: data.instogramma.labels,
            datasets: [
              {
                label: "Numero incidenti",
                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                data: data.instogramma.values
              }
            ]
          },
          options: {
           onHover: function(event,elements){
            /*console.log("dati")
            console.log(dati)*/
            prova(event,elements,data)
           /*s*/
            },


            legend: { display: false }
            /*title: {
              display: true,
              text: 'Predicted world population (millions) in 2050',

            }*/
          }
      });


    scaling()
}



function scaling(){

    //scaling y
    barchart.options.scales = {
                xAxes: [{
                  ticks: {
                    min: 0,
                    max: findMax(barchart.data.datasets),
                    stepSize: 1,
                    },//ticks
                    scaleLabel: {
                      display: true,
                      labelString: "Frequenza incidenti",

                    }//scaleLabel


                }],
                 yAxes: [{
                    scaleLabel: {
                      display: true,
                      labelString: "Fascia età",

                    }//scaleLabel


                }]

    }
    barchart.update()
}




function findMax(datasets){
   /* console.log("datasets")
    console.log(datasets)*/
    maxVal = 0
    for(i = 0; i< datasets.length; i++ ){
        maxTemp = Math.max.apply(null,datasets[i]["data"])
      /*  console.log("maxTemp")
        console.log(maxTemp)*/
        if (maxTemp > maxVal)
            maxVal = maxTemp
    }
    /*console.log("maxVal")
    console.log(maxVal)*/
    return maxVal + 1
}




function createPiechart(data){

 dougchart = new Chart(document.getElementById("myChart2"), {
    type: 'doughnut',
    data: {
      labels: data["tipocoll_freq"]["labels"],
      datasets: [{
        label: "Population (millions)",
        backgroundColor:colors,
        data: data["tipocoll_freq"]["values"]
      }]
    },
    options: {
      responsive : true,
      legend: {
        display: false
     },
    }
});



}

function updatePiechart(l,v){
  dougchart.destroy()
  dougchart = new Chart(document.getElementById("myChart2"), {
    type: 'doughnut',
    data: {
      labels: l,
      datasets: [{
        label: "Population (millions)",
        backgroundColor: colors,
        data: v
      }]
    },
    options: {
      responsive : true,
        legend: {
          display: false
          }
        }
});


  /*canvasResize()*/


}


var curBar
/*var changeBtn = false
*/
function prova(event,elements){

  console.log("CALLINGGG")
   if(elements.length){

        var fascia = elements[0]["_model"]["label"]



        if(curBar!=fascia){



          var fascia_selezionata = "fascia_".concat(fascia)

           /* console.log(arucu.data.labels)
            console.log(data)*/

          updatePiechart(dati[fascia_selezionata].labels, dati[fascia_selezionata].values)

          var newText = fascia_selezionata.replace("fascia_", "")

          console.log($("#fasciatext").text(newText))
          $("#backtoglobal").attr("class",btnreleased)

        }

        curBar=fascia
      }

    /*if(!changeBtn){*/
      /*$("#backtoglobal").attr("class",btnreleased)*/
    /*  changeBtn = true
    }*/
}

/*$("#myChart").mousemove(
    function(evt){
        var activePoints = barchart.getElementsAtEvent(evt);

        console.log("ciaoooooo")
        console.log(activePoints)
    }

);
*/

function tipocollisioneview(data){
        var colors = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]
        labels= data.instogrammacollisione

        datasets= []

        var i = 0
        for (var key in data.datachart_month_data) {

            var dict = {
                    label: key,
                    backgroundColor:'blue',
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

/*function createPiechart(data){

 new Chart(document.getElementById("Piechart-Oltre 60"), {
    type: 'pie',
    data: {
      labels: data["datachart_Oltre 60"]["labels"],
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: data["datachart_Oltre 60"]["values"]
      }]
    },
    options: {

    }
});
}
*/
/*
function createPiechart(data){

 new Chart(document.getElementById("myChart2"), {
    type: 'doughnut',
    data: {
      labels: data["tipocoll_freq"]["labels"],
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e99cd", "#9e7ea2","#2cba7f"],
        data: data["tipocoll_freq"]["values"]
      }]
    },
    options: {

    }
});
}
*/




$("#backtoglobal").click(function () {
        dougchart.destroy()
        createPiechart(dati)
        $("#fasciatext").text("Tutte le fasce")
        $("#backtoglobal").attr("class",btnpressed)
        /*changeBtn=false*/
});

