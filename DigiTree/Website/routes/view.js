var express = require('express');
var router = express.Router();
var database = require('../database');

const TOPIC1 = "5";
const TOPIC2 = "7";
const TOPIC3 = "8";
const TOPIC4 = "10";

router.get("/", function(request, response, next){

  const query1 = `SELECT * FROM current_topic`;

  database.query(query1, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      const topic_no = data[0].current_topic_no;
      const topic_text = data[0].current_topic_text;

      const query2 = `SELECT * FROM comments WHERE topic_no = "${topic_no}"`;

      database.query(query2, function(error, data2) {
        if (error) {
          throw error;
        }
        else {
          var comment = "There are no responses yet! Please come back after a while."
          if (data2.length > 0) {
            var idx = Math.floor(Math.random() * data2.length)
            console.log(idx);
            comment = data2[idx].comment_text;
          }

          response.render("view", {topic:topic_text, comment:comment});
        }
      });
    }
  });

});


router.get("/1", function preset_topics(request, response, next) {
  const query_topic = `SELECT * FROM topics WHERE topic_no = "${TOPIC1}"`;

  database.query(query_topic, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      console.log(data);
      const topic_text = data[0].topic_text;

      const query = `SELECT * FROM comments WHERE topic_no = "${TOPIC1}"`;

      database.query(query, function(error, data) {
        if (error) {
          throw error;
        }
        else {
          var comment = "There are no responses yet! Please come back after a while."
          if (data.length > 0) {
            var idx = Math.floor(Math.random() * data.length)
            console.log(idx);
            comment = data[idx].comment_text;
          }

          response.render("view", {topic:topic_text, comment:comment});
        }
      });
    }
  });
});

router.get("/2",  function preset_topics(request, response, next) {
  const query_topic = `SELECT * FROM topics WHERE topic_no = "${TOPIC2}"`;

  database.query(query_topic, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      console.log(data);
      const topic_text = data[0].topic_text;

      const query = `SELECT * FROM comments WHERE topic_no = "${TOPIC2}"`;

      database.query(query, function(error, data) {
        if (error) {
          throw error;
        }
        else {
          var comment = "There are no responses yet! Please come back after a while."
          if (data.length > 0) {
            var idx = Math.floor(Math.random() * data.length)
            console.log(idx);
            comment = data[idx].comment_text;
          }

          response.render("view", {topic:topic_text, comment:comment});
        }
      });
    }
  });
});

router.get("/3",  function preset_topics(request, response, next) {
  const query_topic = `SELECT * FROM topics WHERE topic_no = "${TOPIC3}"`;

  database.query(query_topic, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      console.log(data);
      const topic_text = data[0].topic_text;

      const query = `SELECT * FROM comments WHERE topic_no = "${TOPIC3}"`;

      database.query(query, function(error, data) {
        if (error) {
          throw error;
        }
        else {
          var comment = "There are no responses yet! Please come back after a while."
          if (data.length > 0) {
            var idx = Math.floor(Math.random() * data.length)
            console.log(idx);
            comment = data[idx].comment_text;
          }

          response.render("view", {topic:topic_text, comment:comment});
        }
      });
    }
  });
});

router.get("/4",  function preset_topics(request, response, next) {
  const query_topic = `SELECT * FROM topics WHERE topic_no = "${TOPIC4}"`;

  database.query(query_topic, function(error, data) {
    if (error) {
      throw error;
    }
    else {
      console.log(data);
      const topic_text = data[0].topic_text;

      const query = `SELECT * FROM comments WHERE topic_no = "${TOPIC4}"`;

      database.query(query, function(error, data) {
        if (error) {
          throw error;
        }
        else {
          var comment = "There are no responses yet! Please come back after a while."
          if (data.length > 0) {
            var idx = Math.floor(Math.random() * data.length)
            console.log(idx);
            comment = data[idx].comment_text;
          }

          response.render("view", {topic:topic_text, comment:comment});
        }
      });
    }
  });
});



module.exports = router;
