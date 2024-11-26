const jwt = require('jsonwebtoken');
const puppeteer = require('puppeteer');


// Retrieve the flag
const fs = require('fs')
const flag = fs.readFileSync("./flag.txt", { encoding: 'utf8' });


// Just your typical admin bot that reads the message
async function notify(msg) {
    // Launch the browser and open a new blank page
    const browser = await puppeteer.launch({
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ]
    });
    const page = await browser.newPage();

    // Navigate the page to a URL
    page.setExtraHTTPHeaders({
        'Authorization': 'Bearer ' + jwt.sign({
            message: msg,
            username: "admin"
        }, flag)
    });
    await page.goto('http://localhost:3000/read');
}

module.exports = { notify, flag }