//config display topic and payload
$(document).ready(function() {
    setInterval(function() {
      $.ajax({
        url: '/get_data',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
          $('#data').text(response.topic + ':'+response.payload);
        }
      });
    }, 5000);
});

//config chart temperature
$(document).ready(function () {
  const ctx = document.getElementById("chart-temperature").getContext("2d");

  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [{ label: "Temperature",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  function addData(label, data) {
    myChart.data.labels.push(label);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChart.update();
  }

  function removeFirstData() {
    myChart.data.labels.splice(0, 1);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 10;
  var socket = io.connect();

  //receive details from server
  socket.on("updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.temperature);
    $('#temp').text(msg.temperature);
    $('#hum').text(msg.humidity);
    // Show only MAX_DATA_COUNT data
    if (myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData();
    }
    addData(msg.date, msg.temperature);
  });
});

//Chart humidity
$(document).ready(function () {
  const ctx = document.getElementById("chart-humidity").getContext("2d");

  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [{ label: "Humidity",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['#54D7CE'],
    },
  });

  function addData(label, data) {
    myChart.data.labels.push(label);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChart.update();
  }

  function removeFirstData() {
    myChart.data.labels.splice(0, 1);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 10;
  var socket = io.connect();

  //receive details from server
  socket.on("updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.humidity);

    // Show only MAX_DATA_COUNT data
    if (myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData();
    }
    addData(msg.date, msg.humidity);
  });
});