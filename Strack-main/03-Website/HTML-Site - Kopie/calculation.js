$.ajax({
  type: "POST",
  url: './PHP-Files/connect.php',
  data: {"type":"check"},
  success: function(response){
      console.log(response);
  }
}); //funktioniert nicht




function calculateXY() {
  
  let lengthImage_x = 300; //pixel
  let lengthImage_y = 150; //pixel
  let rangeFromDB_x = 24; //m
  let rangeFromDB_y = 30; //m

  let x_PercentFromImageLength = (100 * rangeFromDB_x) / 50; //50 = gesamtlänge X der Halle
  let y_PercentFromImageLength = (100 * rangeFromDB_y) / 40; //40 = gesamtlänge Y der Halle

  let x_LengthInPixel = (lengthImage_x * x_PercentFromImageLength) / 100; //300 höchst mögliche Pixellänge in diesem Canvas
  let y_LengthInPixel = (lengthImage_y * y_PercentFromImageLength) / 100; //150 höchst mögliche Pixellänge in diesem Canvas

  let setListFromPixelPosition = [x_LengthInPixel, y_LengthInPixel];

  return setListFromPixelPosition; //
}


