"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

export default function SearchStocks() {
  const [userId, setUserId] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [stockInfo, setStockInfo] = useState(null);
  const [error, setError] = useState("");
  const [tradeAmount, setTradeAmount] = useState("");
  const [notification, setNotification] = useState({ message: "", type: "" }); // New state for notifications

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUserId = localStorage.getItem("userId") || "";
      setUserId(storedUserId);
      console.log("User ID:", storedUserId); // Debugging
    }
  }, []);

  const handleSearch = async () => {
    if (!searchInput.trim()) return;

    try {
      const response = await axios.post("http://localhost:5001/search_stock", {
        ticker: searchInput.trim(),
      });

      setStockInfo(response.data.stock);
      setError("");
      setNotification({ message: "", type: "" }); // Reset notification after new search
    } catch (err) {
      setError("An error occurred while searching");
      setStockInfo(null);
      setNotification({ message: "Error searching for stock.", type: "error" });
    }
  };

  const handleBuy = async () => {
    try {
      const response = await axios.post("http://localhost:5001/buy_stock", {
        user_id: userId, // Make sure userId is being set correctly
        ticker: stockInfo.ticker,
        quantity: tradeAmount, // Ensure tradeAmount is being properly passed
      });

      setNotification({ message: response.data.message, type: "success" });

      // Reset quantity after successful purchase
      setTradeAmount(""); 

      // Hide the notification after 2 seconds
      setTimeout(() => {
        setNotification({ message: "", type: "" });
      }, 2000);
    } catch (err) {
      // Show the error message from the backend or the default message
      const errorMessage = err.response?.data?.message || "Error purchasing stock";
      setNotification({ message: errorMessage, type: "error" });

      // Clear the quantity input even if there's an error (e.g., insufficient funds)
      setTradeAmount(""); 

      // Hide the error message after 2 seconds
      setTimeout(() => {
        setNotification({ message: "", type: "" });
      }, 2000);
    }
  };

  const handleSell = async () => {
    try {
      const response = await axios.post("http://localhost:5001/sell_stock", {
        user_id: userId,
        ticker: stockInfo.ticker,
        quantity: tradeAmount,
      });

      setNotification({ message: response.data.message, type: "success" });

      // Reset quantity after successful sale
      setTradeAmount(""); 

      // Hide the notification after 2 seconds
      setTimeout(() => {
        setNotification({ message: "", type: "" });
      }, 2000);
    } catch (err) {
      // Show the error message from the backend or the default message
      const errorMessage = err.response?.data?.message || "Error selling stock";
      setNotification({ message: errorMessage, type: "error" });

      // Clear the quantity input even if there's an error
      setTradeAmount(""); 

      // Hide the error message after 2 seconds
      setTimeout(() => {
        setNotification({ message: "", type: "" });
      }, 2000);
    }
  };

  return (
    <>
      <div className="flex justify-center items-center min-h-screen">
        <div className="w-[85rem] h-[50rem] flex items-center justify-evenly">
          <Navbar />
          <div className="bg-white border-1 border-[#f5f5f5] shadow-md rounded-2xl h-[35rem] w-[60rem] p-8 flex flex-col items-center">
            <div className="mb-6 w-full flex justify-center mt-7">
              <input
                type="text"
                placeholder="Enter Ticker Symbol (e.g., AAPL)"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                className="border text-black border-gray-300 rounded-lg px-4 py-2 w-80 text-center"
              />
            </div>

            <div className="w-full flex justify-center mt-4">
              {error && <div className="text-red-500 text-center">{error}</div>}
            </div>

            <div className="mt-8 w-full flex justify-center">
              {stockInfo && (
                <div className="p-6 rounded-xl w-[50rem] flex">
                  <div className="flex-1 text-left text-black">
                    <h2 className="text-3xl font-bold mb-4">
                      {stockInfo.company_name} ({stockInfo.ticker})
                    </h2>
                    <div className="text-lg space-y-2">
                      <p>
                        <strong>Sector:</strong> {stockInfo.sector}
                      </p>
                      <p>
                        <strong>Exchange:</strong> {stockInfo.exchange}
                      </p>
                      <p>
                        <strong>Current Price:</strong>{" "}
                        <span className="text-yellow-600 font-[800]">
                          ${stockInfo.price.toFixed(2)}
                        </span>
                      </p>
                      <p>
                        <strong>Volume:</strong>{" "}
                        {stockInfo.volume.toLocaleString()}
                      </p>
                      <p>
                        <strong>Last Updated:</strong> {stockInfo.data_time}
                      </p>
                    </div>
                  </div>

                  <div className="flex flex-col items-center justify-start ml-10">
                    <input
                      type="number"
                      placeholder="Amount"
                      value={tradeAmount}
                      onChange={(e) => setTradeAmount(e.target.value)}
                      className="border text-black border-gray-300 rounded-lg pl-7 px-4 py-2 mb-4 w-32 text-center"
                    />
                    <button
                      onClick={handleBuy}
                      className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-6 rounded-lg mb-4 w-32 hover:cursor-pointer"
                    >
                      Buy
                    </button>
                    <button
                      onClick={handleSell}
                      className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-6 rounded-lg w-32 hover:cursor-pointer"
                    >
                      Sell
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Notification display */}
      {notification.message && (
        <div
          className={`fixed bottom-10 left-1/2 transform -translate-x-1/2 p-4 rounded-lg w-[300px] text-center 
            ${notification.type === "success" ? "bg-green-500 text-white" : "bg-red-500 text-white"}`}
        >
          {notification.message}
        </div>
      )}
    </>
  );
}
