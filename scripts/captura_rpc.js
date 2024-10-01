// scripts/captura_rpc.js

const puppeteer = require('puppeteer');

(async () => {
    try {
        // Inicializar o navegador
        const browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();

        // Definir o tamanho da viewport para melhor captura
        await page.setViewport({ width: 1280, height: 800 });

        // Acessar a página principal de Chains
        await page.goto('https://rpclist.com/chains', { waitUntil: 'networkidle2' });

        // Remover elementos indesejados (exemplo: menu, rodapé)
        await page.evaluate(() => {
            const elementosParaRemover = [
                'header',      // Cabeçalho
                'footer',      // Rodapé
                '.navbar',     // Menu de navegação
                // Adicione mais seletores conforme necessário
            ];

            elementosParaRemover.forEach(seletor => {
                const elementos = document.querySelectorAll(seletor);
                elementos.forEach(elemento => elemento.remove());
            });
        });

        // Adicionar espaço para a logo e frase
        await page.evaluate(() => {
            const body = document.querySelector('body');

            // Criar um container para a logo
            const logoContainer = document.createElement('div');
            logoContainer.style.position = 'fixed';
            logoContainer.style.bottom = '20px';
            logoContainer.style.right = '20px';
            logoContainer.style.zIndex = '1000';

            const logoImg = document.createElement('img');
            logoImg.src = 'https://seu-dominio.com/path-to-your-logo.png'; // URL pública da sua logo
            logoImg.alt = 'Logo';
            logoImg.style.width = '100px'; // Ajuste o tamanho conforme necessário
            logoImg.style.height = 'auto';

            logoContainer.appendChild(logoImg);
            body.appendChild(logoContainer);

            // Criar um container para a frase
            const fraseContainer = document.createElement('div');
            fraseContainer.style.position = 'fixed';
            fraseContainer.style.bottom = '20px';
            fraseContainer.style.left = '20px';
            fraseContainer.style.color = 'white';
            fraseContainer.style.fontSize = '24px';
            fraseContainer.style.fontFamily = 'Arial, sans-serif';
            fraseContainer.style.zIndex = '1000';

            fraseContainer.innerText = 'Sua frase aqui!'; // Altere para a frase desejada
            body.appendChild(fraseContainer);
        });

        // Esperar um pouco para garantir que os elementos foram adicionados
        await page.waitForTimeout(1000);

        // Capturar a imagem da página limpa com logo e frase adicionadas
        await page.screenshot({ path: '../assets/chains_captura.png', fullPage: true });

        // Fechar o navegador
        await browser.close();

        console.log('Captura de tela realizada com sucesso!');
    } catch (error) {
        console.error('Erro na captura de tela:', error);
        process.exit(1);
    }
})();
