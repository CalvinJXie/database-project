"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function ResetPassword() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: "",
    newPassword: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5001/reset_password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.username,
          newPassword: formData.newPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess("Password updated successfully! Please login.");
        setFormData({ username: "", newPassword: "" });
        setTimeout(() => router.push("/sign-in"), 2000);
      } else {
        setError(data.message || "Failed to reset password.");
      }
    } catch (error) {
      console.error("Error:", error);
      setError("Failed to connect to the server.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md">
        <div className="bg-white border border-gray-200 shadow-lg rounded-2xl p-8">
          <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">Reset Password</h2>

          {error && (
            <div className="bg-red-50 text-red-500 p-3 rounded-lg mb-4 text-sm">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-50 text-green-600 p-3 rounded-lg mb-4 text-sm">
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
            <div>
              <label htmlFor="username" className="block text-gray-700 font-medium mb-2">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                value={formData.username}
                onChange={handleChange}
                disabled={isLoading}
                required
                className="text-black w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label htmlFor="newPassword" className="block text-gray-700 font-medium mb-2">
                New Password
              </label>
              <input
                id="newPassword"
                name="newPassword"
                type="password"
                value={formData.newPassword}
                onChange={handleChange}
                disabled={isLoading}
                required
                className="text-black w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              className={`bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors mt-4 font-medium flex justify-center ${isLoading ? "opacity-70 cursor-not-allowed" : "hover:cursor-pointer"}`}
              disabled={isLoading}
            >
              {isLoading ? "Updating..." : "Reset Password"}
            </button>

            <p className="text-center mt-4 text-gray-600 text-sm">
              Remembered your password?{' '}
              <Link href="/sign-in" className="text-blue-500 font-medium hover:underline">
                Sign In
              </Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
