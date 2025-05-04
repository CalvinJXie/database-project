'use client';

import Navbar from "../components/Navbar";
import dynamic from "next/dynamic";
import { useState, useEffect } from "react";

const Chart = dynamic(() => import("../components/Chart"), { ssr: false });

export default function Portfolio() {
  const [userId, setUserId] = useState("");
  const [portfolio, setPortfolio] = useState([]);
  const [totalInvestments, setTotalInvestments] = useState(0);
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUserId = localStorage.getItem("userId") || "";
      setUserId(storedUserId);

      // Fetch portfolio data from the API
      fetchPortfolio(storedUserId);
    }
  }, []);

  const fetchPortfolio = async (userId) => {
    const response = await fetch('http://localhost:5001/portfolio', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId }),
    });

    const data = await response.json();

    if (response.ok) {
      setPortfolio(data.portfolio);
      setTotalInvestments(data.total_investments);
      setBalance(data.balance);
    } else {
      console.error('Error fetching portfolio:', data.message);
    }
  };

  return (
    <>
      <div className="flex justify-center items-center min-h-screen">
        <div className="w-[85rem] h-[50rem] flex items-center justify-evenly">
          <div>
            <Navbar />
          </div>
          <div className="bg-white border-1 border-[#f5f5f5] shadow-md rounded-2xl h-[48rem] w-[60rem] flex flex-col justify-center items-center p-8">
            <span className="text-3xl text-black mb-6 font-[500]">
              Account Balance: <span className="font-[700] text-green-700">${balance}</span>
            </span>
            <span className="text-xl text-black mb-10 font-[500]">
              Total Investments: <span className="font-[700] text-blue-700">${Number(totalInvestments).toFixed(2)}</span>
            </span>
            <Chart portfolio={portfolio} />
          </div>
        </div>
      </div>
    </>
  );
}
