document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("search-button");
    const stockTickerInput = document.getElementById("stock-ticker");
    const canvas = document.getElementById("graph-placeholder");
    const ctx = canvas.getContext("2d");

    let stockChart;

    // Function to fetch stock data from Yahoo Finance API
    async function fetchStockData(ticker) {
        try {
            const response = await fetch('http://localhost:5000/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: ticker
                })
            });
            const data = await response.json();

            if (data.chart.error) {
                throw new Error(data.chart.error.description);
            }

            const timestamps = data.chart.result[0].timestamp;
            const prices = data.chart.result[0].indicators.quote[0].close;

            return {
                labels: timestamps.map(ts => new Date(ts * 1000).toLocaleDateString()),
                data: prices
            };
        } catch (error) {
            console.error("Error fetching stock data:", error);
            alert("Failed to fetch stock data. Please check the ticker symbol and try again.");
            return null;
        }
    }

    // Function to render the stock graph
    function renderGraph(labels, data) {
        if (stockChart) {
            stockChart.destroy(); // Destroy the previous chart instance
        }

        stockChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Stock Price",
                    data: data,
                    borderColor: "#007BFF",
                    backgroundColor: "rgba(0, 123, 255, 0.1)",
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Date"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Price (USD)"
                        }
                    }
                }
            }
        });
    }

    // Event listener for the search button
    searchButton.addEventListener("click", async () => {
        const ticker = stockTickerInput.value.trim().toUpperCase();

        if (!ticker) {
            alert("Please enter a stock ticker.");
            return;
        }

        const stockData = await fetchStockData(ticker);

        if (stockData) {
            renderGraph(stockData.labels, stockData.data);
        }
    });
});