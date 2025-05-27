import { useEffect, useState } from "react";
import axios from "axios";
import Canvas from "./Canvas";

function Request() {
  const [data, setData] = useState([]);
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);

  useEffect(() => {
    axios
      .get("http://10.62.56.118:1437/getLocation")
      .then((res) => {
        //console.log(res.data)
        setData(res.data);
        console.log(res.data);
        let maxValue = Math.max(...data.map((o) => o.l_ID), 0);
        data.map((data) => {
          if (data.l_ID === maxValue) {
            setX(data.l_x);     
            setY(data.l_y);
          }
        });
      })
      .catch((err) => {
        console.log(err);
      });
  });

  return (
    <div>
      <Canvas cx={x} cy={y} />
    </div>
  );
}


export default Request;