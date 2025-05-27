<?php
$connection = mysqli_connect("localhost", "ESP32", "esp32io.com", "strack", 3306);
$_SESSION['conn'] = $connection;

if ($connection->connect_error) {
  die("Connection failed: " . $connection->connect_error);
}
echo "Connected successfully";



#function
function select()
{
  $sql = "SELECT l_x,l_y FROM location order by l_Time DESC limit 1";

  $result = mysqli_query($_SESSION['conn'], $sql);
  while ($row = $result->fetch_assoc()) {
    //$finalResult =  array($row);

    //$array = array(intval($row["l_x"]),intval($row["l_y"]));
    $response = json_encode($row);
    echo $response;
  }
}
select();
$connection->close();
