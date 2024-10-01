// scripts/captura_rpc.js

const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    try {
        // Launch the browser
        const browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();

        // Set viewport size for better capture
        await page.setViewport({ width: 1280, height: 800 });

        // Navigate to the Chains page
        await page.goto('https://rpclist.com/chains', { waitUntil: 'networkidle2' });

        // Remove unwanted elements (e.g., header, footer, navigation)
        await page.evaluate(() => {
            const selectorsToRemove = [
                'header',
                'footer',
                '.navbar',
                // Add more selectors as needed
            ];

            selectorsToRemove.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => element.remove());
            });

            // Hide all table rows beyond the first 5
            const tableBody = document.querySelector('tbody[role="rowgroup"]');
            if (tableBody) {
                const rows = tableBody.querySelectorAll('tr');
                rows.forEach((row, index) => {
                    if (index >= 5) { // Index starts at 0
                        row.style.display = 'none';
                    }
                });
            }
        });

        // Read the phrase from frase.txt (optional)
        let phrase = 'Connect with these top-tier providers now!';  // Default phrase
        const phrasePath = '../assets/frase.txt';
        if (fs.existsSync(phrasePath)) {
            phrase = fs.readFileSync(phrasePath, 'utf8').trim();
        }

        // Add space for the logo and phrase
        await page.evaluate((phraseText) => {
            const body = document.querySelector('body');

            // Create a container for the logo
            const logoContainer = document.createElement('div');
            logoContainer.style.position = 'fixed';
            logoContainer.style.bottom = '20px';
            logoContainer.style.right = '20px';
            logoContainer.style.zIndex = '1000';

            const logoImg = document.createElement('img');
            logoImg.src = 'https://your-username.github.io/rpc-automation/assets/logo.png'; // Public URL of your logo
            logoImg.alt = 'Logo';
            logoImg.style.width = '100px'; // Adjust size as needed
            logoImg.style.height = 'auto';

            logoContainer.appendChild(logoImg);
            body.appendChild(logoContainer);

            // Create a container for the phrase
            const phraseContainer = document.createElement('div');
            phraseContainer.style.position = 'fixed';
            phraseContainer.style.bottom = '20px';
            phraseContainer.style.left = '20px';
            phraseContainer.style.color = 'white';
            phraseContainer.style.fontSize = '24px';
            phraseContainer.style.fontFamily = 'Arial, sans-serif';
            phraseContainer.style.zIndex = '1000';

            phraseContainer.innerText = phraseText; // Adds the phrase from the file
            body.appendChild(phraseContainer);
        }, phrase);

        // Wait a bit to ensure elements are added
        await page.waitForTimeout(1000);

        // Capture the screenshot of the cleaned page with logo and phrase
        await page.screenshot({ path: '../assets/chains_captura.png', fullPage: true });

        // Close the browser
        await browser.close();

        console.log('Screenshot captured successfully!');
    } catch (error) {
        console.error('Error capturing screenshot:', error);
        process.exit(1);
    }
})();
