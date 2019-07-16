"use strict";

function year_change(year) {
  var attempts = document.getElementById('inputNumber').value
  get_nfl_reception_data_test({attempt: parseFloat(attempts), year: parseFloat(year)})
}

function attempt_change(attempts) {
  var year = document.getElementById('inputYear').value
  get_nfl_reception_data_test({attempt: parseFloat(attempts), year: parseFloat(year)})
}

function get_nfl_reception_data_test(obj) {
  
  $.ajax({
    method: 'POST',
    url: 'get-nfl-reception-data',
    data: JSON.stringify(obj),
    success: function success(data) {
      data = JSON.parse(data);
      console.log(data.__data__);
      var xD = [],
          yD = [];
      var axisOpts = [];
      var eChartsTest = echarts.init(document.getElementById('eChartsReceptions'));

      data.__data__.forEach(function (row) {
        
        for (let k in row) {
          let push = true
          axisOpts.forEach(header => {
            if (k === header) {
              push = false;
            }
          })
          if (push) {
            axisOpts.push(k);
          }
        }
        xD.push(row.Combination);
        yD.push(row.Efficiency);
      });

      console.log(axisOpts)

      // Create eChart
      var option = {
        title: {
          text: 'Quarterback/Receiver Efficiency Chart',
          textAlign: 'left',
          left: 425
        },
        tooltip: {},
        legend: {
          data: ['Data']
        },
        xAxis: {
          data: xD,
          axisLabel:{
            show:true,
            rotate: 45
          },
          name: 'QB-Receive Combination',
          nameLocation: 'center',
          nameGap: 150,
        },
        yAxis: {
          name: 'Efficiency',
          nameLocation: 'center',
          nameGap: 50
        },
        series: [{
          name: 'QB to Receiver Efficiency',
          type: 'bar',
          data: yD
        }],
        grid: {
          left: 150,
          top: 50,
          right: 150,
          bottom: 175
        },
        backgroundColor: '#ffffff'
      }; // use configuration item and data specified to show chart

      eChartsTest.setOption(option);
      document.getElementById('loader').style.display = 'none'
    },
    error: function error(err) {}
  });
  document.getElementById('loader').style.display = 'block'
}

// Initialize at 10 pass attempts
// get_nfl_reception_data(10);

get_nfl_reception_data_test({attempt: 10, year: 2016})