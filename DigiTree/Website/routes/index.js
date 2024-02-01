const express = require('express');
var router = express.Router();
const database = require('../database');
const mqtt = require('mqtt');
var counter = 0;

const client = mqtt.connect('mqtt://ide-education:Sy0L85iwSSgc1P7E@ide-education.cloud.shiftr.io', {
  clientid: 'digitree-main'
});

client.on('connect', function() {
  console.log("Successfully connected to MQTT Server");
});


router.get("/", function(request, response, next){
  const query = `SELECT * FROM current_topic`;
  
  database.query(query, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      response.render("index", {title:data[0].current_topic_text, action:'main'})
    }
  });
});

router.get("/comment", function(request, response, next) {
  const query = `SELECT * FROM current_topic`;
  
  database.query(query, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      response.render("index", {title:data[0].current_topic_text, action:'comment'})
    }
  });
});

router.post("/comment", function(request, response, next) {
  var comment = request.body.comment;
  
  if (!comment.trim()) {
    return response.send('<script>alert("Please type something."); window.history.back();</script>');
  }

  if (comment.length > 500) {
    return response.send(`<script>alert("Please write below the limit (500 characters). You wrote ${comment.length} characters."); window.history.back();</script>`);
  }

  var query = `SELECT * FROM current_topic`;
  
  database.query(query, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      query = `INSERT INTO comments_waiting (topic_no, comment_waiting_text) VALUES (?, ?)`;
      database.query(query, [data[0].current_topic_no, comment], function(error, data) {
        if (error) {
          throw error;
        } 
        else {
          response.render("index", {action: "thanks"});
        }
      });
    }
  });
});

router.get('/send-mqtt', function(request, response, next) {
  client.publish('MIE-DigiTree/Data', (counter).toString(), function(err) {
    if (err) {
      console.error('Error sending MQTT message:', err);
      response.status(500).send('Failed to send MQTT message');
    } else {
      console.log('MQTT message sent:', counter);
      response.status(200).send(`MQTT message sent: ${counter}`);
    }
  });

  counter = (counter + 1) % 5;
});

module.exports = router;
