"use client";

import { usePathname, useRouter } from "next/navigation";
import Button from "./Button";

const VerticalNavbar = () => {
  const pathname = usePathname();
  const router = useRouter();

  const menuItems = [
    { id: "/portfolio", label: "Portfolio", icon: "👤" },
    { id: "/orders", label: "Orders", icon: "✅" },
    { id: "/search-stocks", label: "Search Stocks", icon: "📊" },
  ];

  return (
    <nav className="bg-white shadow-md w-[18.5rem] h-[19rem] border-1 border-[#f5f5f5] rounded-2xl flex justify-center">
      <div className="flex flex-col justify-evenly h-full">
        {menuItems.map((item) => (
          <Button
            key={item.id}
            icon={item.icon}
            label={item.label}
            isActive={pathname === item.id}
            onClick={() => router.push(item.id)}
          />
        ))}
        <Button
          key={"sign-out"}
          icon={"❌"}
          label={"Sign Out"}
          isActive={pathname === "/sign-out"}
          onClick={() => {
            window.userId = ""; // 👈 Clear the userId
            router.push("/sign-in"); // Then navigate
          }}
          textColor="text-red-500"
        />
      </div>
    </nav>
  );
};

export default VerticalNavbar;
