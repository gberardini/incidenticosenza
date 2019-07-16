$( document ).ready(function() {
    //console.log("hello world")
    getData().done(createBarchart,createPolarchart)
    /*getData().done(createPolarchart)*/
    $("#backtoglobal").attr("class",btnpressed)

});


/*var barchart;*/

var barchart
var polarchart
var dati
var btnpressed = "btn btn-default"
var btnreleased = "btn btn-default btn-outline"
var color = Chart.helpers.color;
/*var barchart;*/

colors = ['rgb(255, 99, 132)',
   'rgb(255, 159, 64)',
   'rgb(75, 192, 192)',
 'rgb(255, 205, 86)',
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
"#FF716E",
   'rgb(54, 162, 235)',
   'rgb(153, 102, 255)',
   'rgb(231,233,237)' , "#3e95cd",
   "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]



function getData(){
        var endpoint = '/incidenticosenza/ajax/dashboard-traffico'
        return $.ajax({
        method:"GET",
        url:endpoint

    });
}//getData




function canvasResize(){
    canvas = document.getElementById('myChart');


/*
    var w =  canvas.parentElement.clientWidth;
    var h = canvas.parentElement.clientHeight;

    console.log(w)
    console.log(h)
    //canvas.width = w
    //canvas.heigth = h

    var s = "display: block; width:" + w + "; height: " + h + ";"
    console.log(s)*/
    /*$('#myChart').attr("style",s)*/

}

function createBarchart(data){

    dati = data


    barchart = new Chart(document.getElementById("myChart"), {
          type: 'bar',
          data: {
            labels: data.traffico_freq.labels,
            datasets: [
              {
                label: "Numero incidenti",
                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                data: data.traffico_freq.values
              }
            ]
          },
          options: {
           onHover: function(event,elements){
            /*console.log("dati")
            console.log(dati)*/
            eventHover(event,elements,data)

            },
            /*scales: {
                yAxes: [{
                ticks: {
                    min: 0,
                    max: findMax()
                }
            }]
            },*/
            legend: { display: false },
            /*title: {
              display: true,
              text: 'Predicted world population (millions) in 2050',

            }*/
          }
      });

    scaling()
    canvasResize()
}



function findMax(datasets){
    console.log("datasets")
    console.log(datasets)
    maxVal = 0
    for(i = 0; i< datasets.length; i++ ){
        console.log("call")

        maxTemp = Math.max.apply(null,datasets[i]["data"])
        console.log("maxTemp")
        console.log(maxTemp)
        if (maxTemp > maxVal)
            maxVal = maxTemp


    }

    console.log("maxVal")
    console.log(maxVal)


    return maxVal + 5
}

function scaling(){
    //scaling y


    console.log("creato barchart")
    console.log("###barchart###")
    console.log(barchart)
    barchart.options.scales = {
                yAxes: [{
                  ticks: {
                    min: 0,
                    max: findMax(barchart.data.datasets),
                    stepSize: 5
                  }
                }],



    }
    barchart.update()

    /*scalingy()*/
    /*barchart.update()*/
}


function toAlphaColor(){
  var c = []
  for( i =0; i<colors.length; i++ ){
    c.push(color(colors[i]).alpha(0.2).rgbString())
  }
  return c
}

function createPolarchart(data){

    polarchart = new Chart(document.getElementById("myChart2"), {
    type: 'polarArea',
    data: {
      labels: data.fascia_freq.labels,
      datasets: [
        {

          borderColor: colors,
          backgroundColor: toAlphaColor() ,
          data: data.fascia_freq.values
        }
      ]
    },
    options: {
      title: {
        display: true

      }, legend: { display: false }
    }
});

    /*canvasResize()
*/


}





function updatePolarchart(l,v){
    polarchart.destroy()
    polarchart = new Chart(document.getElementById("myChart2"), {
    type: 'polarArea',
    data: {
      labels: l,
      datasets: [
        {
          borderColor: colors,
          backgroundColor:toAlphaColor() ,
          data: v
        }
      ]
    },
    options: {
      title: {
        display: true,

      }, legend: { display: false }
    }
});
}


var curBar


function eventHover(event,elements,data){

  if(elements.length){

        var fascia = elements[0]["_model"]["label"]



        if(curBar!=fascia){






         var labels = Object.keys(dati["entita_fascia_freq"][fascia])


         var values = Object.values(dati["entita_fascia_freq"][fascia])

        updatePolarchart(labels, values)
         /*console.log(values)*/
        /* console.log(Object.values(dati["entita_fascia_freq"][fascia]))*/
        $("#condizionitext").text(fascia)
         $("#backtoglobal").attr("class",btnreleased)
          /*var newText = fascia_selezionata.replace("fascia_", "")*/


          /*console.log($("#fasciatext").text(newText))*/

        }

        curBar=fascia
      }



}



$("#backtoglobal").click(function(){

    polarchart.destroy()
    createPolarchart(dati)
    $("#condizionitext").text("tutte")
    $("#backtoglobal").attr("class",btnpressed)





});
