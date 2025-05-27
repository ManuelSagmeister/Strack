import express from "express";
import { getRange,addRange, getLocation } from "./database.js";
//import { PythonShell } from "python-shell";
import dgram from "dgram";
import cors from "cors";

var PORT = 50000;
var HOST = "192.168.0.188";
var server = dgram.createSocket("udp4");

const app = express();

app.use(express.json()); //with this statement, its possible to also collect JSON Files
app.use(cors());

server.on("message", function (message, remote) {
  //With this function, on every UDP message we get, we are creating a new entry in our DB
  var i = JSON.parse(message);

  const fk_Tag_MAC = i.tagMac;
  i.links.forEach((element) => {
    const fk_Anchor_MAC = element.anchor;
    const r_Range = element.range;

    if (r_Range > 0) {
      addRange(r_Range, fk_Anchor_MAC, fk_Tag_MAC);
    }
  });
});

app.get("/getLocation", async (req, res) => {
  //With this get Statement, we are collecting all our Data from the Location table and use it in React
  let location = await getLocation();
 
   
  res.send(location);

});

app.listen(1437, () => console.log("Server has been started"));

server.on("listening", function () {
  var address = server.address();
  console.log(
    "UDP Server listening on " + address.address + ":" + address.port
  );
});

server.bind(PORT, HOST);