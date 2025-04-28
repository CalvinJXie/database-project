const Button = ({ icon, label, onClick, isActive, textColor="" }) => {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 w-64 py-4 px-4 text-left transition-colors rounded-xl ${
        isActive 
          ? "bg-blue-400 text-white" 
          : "hover:bg-gray-100 text-gray-700 hover:cursor-pointer"
      } ${textColor}`}
    >
      {icon && <span className="text-lg">{icon}</span>}
      <span className="font-[700]">{label}</span>
    </button>
  );
};

export default Button;
