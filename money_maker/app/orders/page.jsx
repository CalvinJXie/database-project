'use client';

import Navbar from "../components/Navbar";
import { useState, useEffect } from "react";
import axios from 'axios';

export default function Orders() {
  const [userId, setUserId] = useState("");
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUserId = localStorage.getItem("userId") || "";
      setUserId(storedUserId);

      if (storedUserId) {
        axios.post('http://localhost:5001/transactions', { user_id: storedUserId })
          .then(response => {
            setOrders(response.data.transactions);
          })
          .catch(error => {
            console.error('Error fetching transactions:', error);
          });
      }
    }
  }, []);

  return (
    <>
      <div className="flex justify-center items-center min-h-screen">
        <div className="w-[85rem] h-[50rem] flex items-center justify-evenly">
          <Navbar />
          <div className="bg-white border-1 border-[#f5f5f5] shadow-md rounded-2xl h-[48rem] w-[60rem] flex flex-col items-center justify-start p-8 overflow-y-auto">
            <div className="w-[90%]">
              <table className="w-full text-left border-collapse text-black">
                <thead className="text-center">
                  <tr className="border-b-2 border-gray-200">
                    <th className="py-2">Stock</th>
                    <th className="py-2">Price</th>
                    <th className="py-2">Quantity</th>
                    <th className="py-2">Type</th>
                    <th className="py-2">Datetime</th>
                  </tr>
                </thead>
                <tbody className="text-black">
                  {orders.length > 0 ? (
                    orders.map((order) => (
                      <tr key={order.id} className="border-b border-gray-100 text-center">
                        <td className="py-4">{order.stock}</td>
                        <td className="py-4">${order.price.toFixed(2)}</td>
                        <td className="py-4">{order.quantity}</td>
                        <td className="py-4 font-bold">
                          <span className={order.type === 'BUY' ? 'text-green-500' : 'text-red-500'}>
                            {order.type}
                          </span>
                        </td>
                        <td className="py-4">{order.time}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" className="text-center py-10 text-gray-500">
                        No transactions found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
