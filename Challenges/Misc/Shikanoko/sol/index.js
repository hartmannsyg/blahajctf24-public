const puppeteer = require('puppeteer');

(async () => {
	const browser = await puppeteer.launch({ headless: false });
	const page = await browser.newPage();
	await page.goto('http://188.166.198.74:30035'); // replace with actual url


    async function shikanokonokonokokoshitantan() {
        await page.click('#node_shi');
        await page.click('#node_ka');
        await page.click('#node_no');
        await page.click('#node_ko');
        await page.click('#node_no');
        await page.click('#node_ko');
        await page.click('#node_no');
        await page.click('#node_ko');
        await page.click('#node_ko');
        await page.click('#node_shi');
        await page.click('#node_ta');
        await page.click('#node_n');
        await page.click('#node_ta');
        await page.click('#node_n');
    }
    // note: this is really RNG, sometimes I get it consistently while other times I have to run this 10 times
    await shikanokonokonokokoshitantan()
    await shikanokonokonokokoshitantan()

    page.on('dialog', async dialog => {
        //get alert message
        console.log(dialog.message());
        //accept alert
        await dialog.accept();
        await browser.close();
    })

	
})();