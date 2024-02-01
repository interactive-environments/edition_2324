
var express = require('express');

var router = express.Router();

var database = require('../database');

router.get("/", function(request, response, next){

    const query1 = `SELECT * FROM topics ORDER BY topic_no DESC`;
    const query2 = `SELECT * FROM current_topic`;
    const query3 = `SELECT COUNT(comment_waiting_no) AS count FROM comments_waiting`;

    Promise.all([
        new Promise((resolve, reject) => {
            database.query(query1, function(error, data) {
                if (error) {
                    reject(error);
                } else {
                    resolve(data);
                }
            });
        }),
        new Promise((resolve, reject) => {
            database.query(query2, function(error, data) {
                if (error) {
                    reject(error);
                } else {
                    resolve(data);
                }
            });
        }),
        new Promise((resolve, reject) => {
            database.query(query3, function(error, data) {
                if (error) {
                    reject(error);
                } else {
                    resolve(data);
                }
            });
        })
    ])
    .then(([topics, currentTopic, noComments]) => {
        response.render('admin', {
            title: 'Admin Page',
            action: 'list',
            topic: topics,
            current_topic: currentTopic,
            no_comments: noComments[0].count
        });
    })
    .catch(error => {
        console.error("Error:", error);
        response.status(500).send("Error fetching data");
    });
});

router.get("/add_topic", function(request, response, next){

	response.render("admin", {title:'Add a New Topic', action:'add_topic'});

});

router.post("/add_topic", function(request, response, next) {
    var topic_text = request.body.topic_text;

    var query = `INSERT INTO topics (topic_text) VALUES ("${topic_text}")`;

    database.query(query, function(error, data) {
        if (error) {
            throw error;
        }
        else {
            response.redirect("../admin");
        }
    });
});

router.get("/edit_topic/:topic_id", function(request, response, next){
    var topic_no = request.params.topic_id;
    console.log(topic_no)
	response.render("admin", {title:'Edit Topic', action:'edit_topic', topic_id:topic_no});

});

router.post("/edit_topic/", function(request, response, next) {
    var topic_no = request.body.topic_id;
    var new_topic_text = request.body.topic_text;
  
    var query = `UPDATE topics SET topic_text = "${new_topic_text}" WHERE topic_no = "${topic_no}"`;
  
    database.query(query, function(error, data) {
        if (error) {
            throw error;
        }
        else {
            response.redirect("../../admin");
        }
    });
  });

router.get("/mod_comments", function(request, response, next){
    var query = `SELECT * FROM comments_waiting ORDER BY topic_no DESC, comment_waiting_no`;

    database.query(query, function(error, data) {
        if (error) {
            throw error;
        }
        else {
            response.render("admin", {title:'Moderate Comments', action:'mod_comments', comments_mod:data});
        }
    });

});

router.get('/view_comments', function(request, response, next) {
    var query = `SELECT * FROM comments ORDER BY topic_no DESC, comment_no DESC`;
    database.query(query, function(error, data) {
        if (error) {
            throw error;
        }
        else {
            response.render('admin', {title: 'View All Comments', action:'view_comments', comments:data});
        }
    });
});

router.get('/delete/:entity/:id', function(request, response, next) {
    var entity = request.params.entity;
    var id = request.params.id;
    var query;
    if (entity == "topic") {
        query = `DELETE FROM topics WHERE topic_no = "${id}"`;
    }
    else if (entity == "comment") {
        query = `DELETE FROM comments WHERE comment_no = "${id}"`;
    }

    database.query(query, function(error, data) {
        if (error) {
            throw error;
        }
        else {
            var query2 = `DELETE FROM current_topic WHERE current_topic_no = "${id}"`;
            database.query(query2, function(error, data2) {
                if (error) {
                    throw error;
                }
                else{
                    if (entity == "topic") {
                        response.redirect("../../");
                    }
                    else if (entity == "comment") {
                        response.redirect("../../view_comments");
                    }
                }
            });
        }
    });
});

router.get('/select/:topic_no', function(request, response, next) {
    var topic_no = request.params.topic_no;
    var query = `DELETE FROM current_topic`;

    database.query(query, function(error, data) {
        if (error) {
            throw error;
        }
        else {
            var query2 = `SELECT topic_text FROM topics WHERE topic_no = "${topic_no}"`
            database.query(query2, function(error2, data2) {
                if (error2) {
                    throw error2;
                }
                else {
                    console.log(data2);
                    var query3 = `INSERT INTO current_topic (current_topic_no, current_topic_text) VALUES ("${topic_no}", "${data2[0].topic_text}")`

                    database.query(query3, function(error3, data3) {
                        if(error3) {
                            throw error3;
                        }
                        else {
                            response.redirect("../");
                        }
                    });
                }
            });

        }
    });
});

router.get('/confirm_comment/:cw_id/:pass', function(request, response, next) {
    var cw_id = request.params.cw_id;
    var pass = request.params.pass;
    var query1 = `
    INSERT INTO comments (topic_no, comment_text)
    SELECT topic_no, comment_waiting_text
    FROM comments_waiting WHERE comment_waiting_no = "${cw_id}"
    `;
    var query2 = `DELETE FROM comments_waiting WHERE comment_waiting_no = "${cw_id}"`;

    if (pass == "true") {
        console.log("pass");
        database.query(query1, function(error, data) {
            if (error) {
                throw error;
            }
        });
    }

    database.query(query2, function(error, data) {
        if (error) {
            throw error;
        }
        else {
            response.redirect("../../mod_comments")
        }
    });
});

module.exports = router;
