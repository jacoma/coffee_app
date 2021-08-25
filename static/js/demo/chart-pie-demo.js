// // Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

$(document).ready(function(){
    var $pieChart = $("#myPieChart");
    $.ajax({
        method: "GET",
        url: $pieChart.data("url"),
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
    // Pie Chart Example
    function setChart(){
        var ctx = $pieChart[0].getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: defaultData,
                    backgroundColor: ['#2F5061', '#4297a0', '#4297A0', '#D6CCC8'],
                    hoverBackgroundColor: ['#618293', '#6e9da2', '#74C9D2', '#F4EAE6'],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }],
            },
            options: {
                maintainAspectRatio: false,
                tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
                },
                legend: {
                display: false
                },
                cutoutPercentage: 80,
            },
        });
    }
});