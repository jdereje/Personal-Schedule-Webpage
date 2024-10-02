var stocks = new Stocks('M44LLZEMJOV1MHLK');



async function request() {
    var stockSymbol = document.getElementById('stockSymbol').value;

    
    var options = {
        symbol: stockSymbol,
        interval: 'daily',
        amount: 1 
    };

    try {
        var result = await stocks.timeSeries(options);
        if (result.length > 0) {
            var stockData = '';
            result.forEach(JSONdata => {
                stockData += `[\n {\n`;
                stockData += `  "open": ${JSONdata.open},\n`;
                stockData += `  "high": ${JSONdata.high},\n`;
                stockData += `  "low": ${JSONdata.low},\n`;
                stockData += `  "close": ${JSONdata.close},\n`;
                stockData += `  "volume": ${JSONdata.volume}\n`;
                stockData += `  "date": "${(JSON.stringify(JSONdata.date))}",\n`;
                stockData += ` }\n]\n\n`;
            });
            document.getElementById('quoteResult').value = stockData;
        } else {
            alert("No data found for the stock symbol");
        }
    } catch (error) {
        console.error('Error fetching stock data:', error);
        alert('Error fetching stock data. Please try again later.');
    }
}

