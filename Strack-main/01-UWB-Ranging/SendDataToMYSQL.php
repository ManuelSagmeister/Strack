<?php

if(isset($_GET["espID"]) && isset($_GET["tagDistance"])) {
  $espIDHTTP = $_GET["espID"]; // get espID value from HTTP GET
  $tagDistanceHTTP = $_GET["tagDistance"];

//Diese Variablen müssen angepasst werden
$servername = "localhost";
$username = "ESP32";
$password = "esp32io.com";
$dbname = "db_esp32";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "INSERT INTO tbl_currentDistance(espID,tagDistance)
VALUES ($espIDHTTP,$tagDistanceHTTP)";

if ($conn->query($sql) === TRUE) {
  echo "New record created successfully";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
} else{
  echo "Parameter wurden nicht gesetzt";
}


?>