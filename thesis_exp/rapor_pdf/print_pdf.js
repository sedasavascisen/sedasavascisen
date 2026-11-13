// Usage: node print_pdf.js in.html out.pdf  — prints an HTML file to A4 PDF with page numbers (Chromium).
const { chromium } = require('playwright');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + require('path').resolve(inp), { waitUntil: 'load' });
  await page.pdf({
    path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-family:DejaVu Sans,sans-serif;font-size:7pt;color:#5b6470;width:100%;text-align:center;">Tez deneyleri — kapsamlı teknik rapor · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '16mm', bottom: '16mm', left: '14mm', right: '14mm' },
  });
  await browser.close();
})();
