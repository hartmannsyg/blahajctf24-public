// Importing Modules
const express = require('express')
const admin = require('./admin/admin')
const path = require("path");
const { expressjwt: jwt } = require("express-jwt");
const createDOMPurify = require('dompurify')
const { JSDOM } = require('jsdom');

// Retrieve the flag
const flag = admin.flag;

// Express App Settings
const app = express()
app.use(express.static('public'))
app.use(express.urlencoded({ extended: true }))


// View Engine Setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");


// DOM Purify Setup
const { window } = new JSDOM('');
const DOMPurify = createDOMPurify(window);


// First page that is seen
app.get('/', (req, res) => {
    res.render('index')
})

// Route to post the message
app.post('/send', (req, res) => {
    // Retrieve message details and sanitize the messages
    const message = {
        name: DOMPurify.sanitize(req.body['name']),
        title: DOMPurify.sanitize(req.body['title']),
        body: DOMPurify.sanitize(req.body['message']),
    }


    console.log(message.body)
    // Notify the admin of the message to read
    admin.notify(message)

    // Show the user the sent message
    res.render('view_message', { message })
})


// Read Site <MUST BE ADMIN>
app.get('/read', jwt({ secret: flag, algorithms: ["HS256"] }), (req, res) => {
    // Check if the user really is admin
    if (req.auth.username != "admin") return res.sendStatus(401);

    // Show message to user
    const message = req.auth.message;
    res.render('view_message', { message })
})

// Flag Site
app.post('/flag', jwt({ secret: flag, algorithms: ["HS256"] }), (req, res) => {
    // Check if the user really is admin
    if (req.auth.username != "admin") return res.sendStatus(401);

    return res.send(`Flag is ${flag}`);
})


app.listen(8000, () => {
    console.log('Listening on port 8000')
})