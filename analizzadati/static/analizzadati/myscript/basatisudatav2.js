$( document ).ready(function() {
    //console.log("hello world")
    getData().done(createBarchart, createPiechart,scalingdayview)
    /*scalingdayview()*/

   /* $("#btngiorno").click()
*/
});

/*
var palette = ["#C19648","#AD9845","#989946","#83984C","#6F9754","#5C945E","#4A9169","#3C8C73","#34877B","#358182","#3C7A86","#487387",#556B84,#61637F,#6B5B77]*/

var barchart;
var bubblechart;
var dati;
var color = Chart.helpers.color;
var btnpressed = "btn btn-default"
var btnreleased = "btn btn-default btn-outline"
var daysofweek = {

    0 : "Domenica",
    1 : "Lunedì",
    2 : "Materdì",
    3:  "Mercoledì",
    4:  "Giovedì",
    5:  "Venerdì",
    6:  "Sabato"
}


function getData(){
        var endpoint = '/incidenticosenza/ajax/dashboard-data'
        return $.ajax({
        method:"GET",
        url:endpoint

    });
}//getData




function toDate(){
    listofdate = dati.datachart_day.labels
    listret = []
    console.log("listofdate")
    console.log(listofdate)
    for( i = 0; i< listofdate.length; i++ ){


        var d = listofdate[i].split("/")

/*
        var tmp = d[0]
        d[0]=d[1]
        d[1] = tmp*/
        var stringa = d[1]+ "/" +d[0]+"/"+d[2]
        var dd = new Date(stringa)
        console.log(stringa)
        listret.push(dd)

    }
    return listret
}



function createBarchart(data){
        dati = data
        labels =[]
        values = []
        console.log("###data###")
        console.log(data)
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
        labels: labels, //date
        datasets: [{
            label: 'Numero incidenti',
            backgroundColor: "#EF2723",
            borderColor: "#EF2723" ,
            data: values,


        }]
        },//data
        options : {

           tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {

                   /* var label = data.datasets[tooltipItem.datasetIndex] || '';*/
                    console.log("label")
                    console.log(tooltipItem)


                    var stringadata = tooltipItem.label.split("/")
                    var giorno = stringadata[0]
                    //mesi partono da 0
                    var mese = parseInt(stringadata[1]-1)
                    /*var anno = stringadata[2]*/


                    var d = new Date("2013",mese,giorno)
                    var indexofday = d.getDay()

                  return daysofweek[indexofday];
                }
            }//callbacks

          },//tooltips

                 }//option
         })//chart

    $("#btnsettimana").attr("class", btnreleased)
    $("#btngiorno").attr("class", btnpressed)
    $("#btnfasciaoraria").attr("class",btnreleased)





}



function scalingdayview(){
    //scaling y


    console.log("creato barchart")
    barchart.options.scales = {
                yAxes: [{
                  ticks: {
                    min: 0,
                    max: findMax(barchart.data.datasets),
                    stepSize: 1
                  }
                }],


                xAxes: [{
                     ticks: {
                     // Include a dollar sign in the ticks
                        callback: function(value, index, values) {
                         var d = value.split("/")
                        /* console.log("## creo xAxes###")
                         console.log(d)*/
                        //mesi partono da 0

                        var lbl= d[0] + "/" + d[1]
                       /* console.log(lbl)*/
                         return lbl

                        }
                    }
                }]

    }
    barchart.update()

    /*scalingy()*/
    /*barchart.update()*/
}



function scalingy(){

    barchart.options.scales = {
                yAxes: [{
                  ticks: {
                    min: 0,
                    max: findMax(barchart.data.datasets),
                    stepSize: 1
                  }
                }]

}

barchart.update()
/*console.log("###OPTIONSBARCHART###")
console.log(barchart.options)*/
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


    return maxVal + 1
}


function findMaxBubblechart(datasets){
    console.log("datasets")
    console.log(datasets)
    var maxVal = 0
    for(i = 0; i< datasets.length; i++ ){
        console.log(datasets[i]["data"][0]["y"])



        maxTemp = parseInt(datasets[i]["data"][0]["y"])
        console.log("maxTemp")
        console.log(maxTemp)
        if (maxTemp > maxVal)
            maxVal = maxTemp


    }



    maxVal = maxVal+2

    console.log("maxVal")
    console.log(maxVal)

    var fstart = maxVal
    var fend = fstart + 2


    return maxVal

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
          console.log("###barchart###")
          console.log(barchart.data)
           barchart.data.labels=labels
           barchart.data.datasets=datasets
           barchart.update()
           scalingy()
           $("#btnsettimana").attr("class", btnpressed)
           $("#btngiorno").attr("class",btnreleased)
           $("#btnfasciaoraria").attr("class",btnreleased)



}


function dateToString(stringa){
  //y m d

  var d = stringa.split("/")

  console.log("##dateToString###")
  console.log(d)
  console.log(new Date(d[2],parseInt(d[1])-1,d[0]))

  return new Date(d[2],parseInt(d[1])-1,d[0])


}


function getBubbleDataset(data){
console.log("getBubbleDataset")
console.log(data.data_ora_freq)
console.log(data.data_ora_freq["01/02/2013"])
  datasets= []

        var i = 0
        for (var d in data.data_ora_freq) {
            /*console.log(fasciaA)
            var s = fasciaA.match(/^\d+|\d+\b|\d+(?=\w)/g)[0];
            console.log("replacing")
            console.log(s)*/
            // d.split("/")[0] + d.split("/")[1]

            console.log("#d#")
            console.log(d)
            if(Object.keys(data.data_ora_freq[d]).length==0){
                var dict = {
                    label: "Num inc",
                    backgroundColor: "rgba(255,221,50,0.2)",
                    borderColor: "rgba(255,221,50,1)",
                    data:[{
                     x :dateToString(d),
                     y:  0,
                     r: 0
                    }]
                    // etc.
            };

            datasets.push(dict)

            }else{
            console.log("qui")
            console.log(d)
            console.log(data.data_ora_freq[d])
            for (var orario in data.data_ora_freq[d]) {
              /* console.log(data.fascia_fascia_freq[fasciaA][fasciaB])*/

              console.log("#orario#")
              console.log(orario)
              console.log( orario.split("-").join().split(":"))
            var dict = {
                    label: "Num inc",
                    backgroundColor:  color("#FF5F5C").alpha(0.2).rgbString(),
                    borderColor: "#FF5F5C",
                    data:[{
                     x : dateToString(d),
                     y:  orario.split("-").join().split(":")[0],
                     r: data.data_ora_freq[d][orario]*7
                    }]
                    // etc.
            };
            /*console.log(dict)*/

           datasets.push(dict)

          }
      }
        console.log("#dict#")
        console.log(dict)

        }


    console.log("####DATASET BUBBLE CHART###")
    console.log(datasets)
    return datasets

}




function createBubblechart(data){
  console.log("createBubblechart ")
  datasets = getBubbleDataset(data)
  console.log(datasets)
  bubblechart = new Chart(document.getElementById("myChart"), {
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
      legend: false,
      title: {
        display: true,

      }, scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: "Fascia Oraria",

          }, ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, values) {
                        var fstart = parseInt(value)
                        var fend = fstart +2

                        fstart = addZeroToDigit(fstart)
                        fend = addZeroToDigit(fend)


                        return fstart + ":00-" + fend + ":00"


                    },

                    max: findMaxBubblechart(datasets),


                }//ticks


        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: "Data",

          } , ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, values) {
                        var d = new Date(value)
                        var m = parseInt(d.getMonth())+1

                        d = addZeroToDigit(d.getDate())
                        m = addZeroToDigit(m)

                        return d + "/" + m  ;
                    }
                }//ticks
        }]
      },

      tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    var label = data.datasets[tooltipItem.datasetIndex].label || '';



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


                    return label;
                }
            }

          }//tooltips
    }//options
});

  $("#btnsettimana").attr("class", btnreleased)
  $("#btngiorno").attr("class", btnreleased)
  $("#btnfasciaoraria").attr("class", btnreleased)


}


function addZeroToDigit(s){

  if(s >=0 && s <= 9 )
    return "0".concat(s)

  return s

}




function daysview(data){
    barchart.destroy()
    createBarchart(data)
    scalingdayview()

}


$("#btnsettimana").click(function () {
        /*getData().done(weekview)*/
         console.log($("#btnfasciaoraria").attr("class"))
        if(bubblechart){
            bubblechart.destroy()
            barchart.destroy()
            createBarchart(dati)
            scalingdayview()
        }

       weekview(dati)
       scalingy()

    });



$("#btngiorno").click(function () {
        /*getData().done(daysview)*/
       /* createBarchart(dati)*/
        console.log($("#btnfasciaoraria").attr("class"))
        if(bubblechart){
          console.log("#######distruzione bubblechart")
          bubblechart.destroy()
        }

        daysview(dati)

});


$("#btnfasciaoraria").click(function(){


    barchart.destroy()
    createBubblechart(dati)


});






/*

        var canvas = document.getElementById('myChart');
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
        console.log(canvas.parentElement.clientWidth)
        console.log(canvas.parentElement.clientWidth)

*/





