<?php

$connection = mysqli_connect("localhost", "ESP32","esp32io.com","strack", 3306);
$_SESSION['conn'] = $connection;

if ($connection->connect_error) {
  die("Connection failed: " . $connection->connect_error);
}
echo "Connected successfully";
?>

