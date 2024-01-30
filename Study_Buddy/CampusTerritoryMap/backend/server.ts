import express from 'express';
//import * as express from 'express';
import * as http from 'http';
import { Server, Socket } from 'socket.io';
import { retrieveGrid, updateColor } from './gridController';
import { getIPList, updateOrGenerateTimeStamp } from './ipController';

const date = new Date();

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*", // replace with your frontend domain
    methods: ["GET", "POST"],
  },
});

// Define a connection event
io.on('connection', (socket: Socket) => {

  const IP = socket.handshake.headers['x-real-ip'];
  socket.emit('grid', JSON.stringify(retrieveGrid()));
  socket.emit('IP', IP);
  socket.emit('IPList', JSON.stringify(getIPList()), IP);

  // Handle events from the client
  socket.on('hexelPlaced', (newColor, index) => {

    const updatedGrid = updateColor(newColor, index);

    //! Comment here if server can't be deployed
    const ipList = updateOrGenerateTimeStamp(IP);

    io.emit('grid', JSON.stringify(updatedGrid));
    socket.emit('IPList', JSON.stringify(ipList), IP);
  });

})

const port = process.env.PORT || 5000;

server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
