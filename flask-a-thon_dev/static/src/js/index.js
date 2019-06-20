"use strict";

function get_nfl_reception_data(v) {
  $.ajax({
    method: 'POST',
    url: 'get-nfl-reception-data',
    data: v.toString(),
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
    },
    error: function error(err) {}
  });
}

// Initialize at 10 pass attempts
get_nfl_reception_data(10);