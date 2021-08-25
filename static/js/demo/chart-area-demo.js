// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

$(document).ready(function(){
  var $Chart = $("#myAreaChart");
  $.ajax({
      method: "GET",
      url: $Chart.data("url"),
      success: function(data) {
          labels = data.labels
          defaultData = data.data
          setChart()
      },
      error: function (error_data) {
          console.log("error")
          console.log(error_data)

      }
  })

  // Area Chart Example
  function setChart(){
    var ctx = $Chart[0].getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: "Rating Count",
          lineTension: 0.3,
          backgroundColor: "rgba(5,68,94, 0.05)",
          borderColor: "rgba(5,68,94, 1)",
          pointRadius: 2,
          pointBackgroundColor: "rgba(5,68,94, 1)",
          pointBorderColor: "rgba(5,68,94, 1)",
          pointHoverRadius: 3,
          pointHoverBackgroundColor: "rgba(5,68,94, 1)",
          pointHoverBorderColor: "rgba(5,68,94, 1)",
          pointHitRadius: 10,
          pointBorderWidth: 2,
          data: defaultData
        }],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              unit: 'month'
            },
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 12
            }
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              padding: 10,
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
        legend: {
          display: false
        },
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          titleMarginBottom: 10,
          titleFontColor: '#6e707e',
          titleFontSize: 14,
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          intersect: false,
          mode: 'index',
          caretPadding: 10,
          callbacks: {
            label: function(tooltipItem, chart) {
              var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
              return datasetLabel + ': ' + tooltipItem.yLabel;
            }
          }
        }
      }
    });
  }
});