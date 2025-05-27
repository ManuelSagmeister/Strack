import { useEffect, useRef, useState } from "react";
import styles from "./styles/Canvas.module.css";

const Canvas = (props) => {
  const [Loc, setLoc] = useState([]);

  useEffect(() => {
    let coordinateOrigin_x = 0; //Wert für die Nullpunktverschiebung in X-Achse
    let coordinateOrigin_y = 49.5; //Wert für die Nullpunktverschiebung in Y-Achse
    let fullMap_x = 300; //standard 300pixel
    let fullMap_y = 150; //standard 150pixel
    let imageInPixel_x = 231 ; // diese Variable muss hard-codiert werden.  231
    let imageInPixel_y = fullMap_y - coordinateOrigin_y;
    let getRangeFromDB_x = props.cx; //Location aus der DB 
    let getRangeFromDB_y = props.cy; //Location aus der DB
    let trackingAreaInMeter_x = 50; //Gesamtgröße der trackingfläche in Meter
    let trackingAreaInMeter_y = 40; //Gesamtgröße der trackingfläche in Meter
    

    let percent_x = (100 * getRangeFromDB_x) / trackingAreaInMeter_x;
    let percent_y = (100 * getRangeFromDB_y) / trackingAreaInMeter_y;

    let percentInMeter_x = (imageInPixel_x * percent_x) / 100;
    let percentInMeter_y = (imageInPixel_y * percent_y) / 100;

    let setListFromPixelPosition = [percentInMeter_x + coordinateOrigin_x,percentInMeter_y+coordinateOrigin_y]; //hier werden Werte dazu addiert, damit der Null-Punkt sich an einem beliebigen Punkt befindet
    setLoc(setListFromPixelPosition);
  });

  const canvasRef = useRef(null);

  const draw = (ctx) => {
    const size = 1;

    ctx.fillStyle = "Blue";
    ctx.beginPath();
    ctx.arc(Loc[0], Loc[1], size, 0, 2 * Math.PI);
    ctx.fill();
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);

    //Our draw come here
    draw(context);
  }, [draw]);

  return (
    <div className={styles.wrapper}>
      <div>
        <canvas className={styles.canvas} ref={canvasRef}></canvas>
      </div>
    </div>
  );
};

export default Canvas;
