import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

export default function Chart({ portfolio }) {
  // Map portfolio to chart data
  const data = portfolio.map(stock => ({
    name: stock.ticker,
    value: stock.total_value,
    quantity: stock.quantity,  // Add quantity to the data for tooltip
  }));

  const COLORS = [
    '#0088FE', '#00C49F', '#FFBB28', '#FF8042', 
    '#FF6347', '#6A5ACD', '#FF1493', '#FFD700',
    '#32CD32', '#FF4500', '#A52A2A', '#DAA520', 
    '#ADFF2F', '#20B2AA', '#B8860B', '#8A2BE2', 
    '#7FFF00', '#D2691E', '#DC143C', '#F4A300',
    '#00CED1', '#FF00FF', '#4B0082', '#FF1493', 
    '#C71585', '#D3D3D3', '#FFB6C1', '#98FB98'
  ];

  return (
    <PieChart width={400} height={400}>
      <Pie
        data={data}
        cx="50%"
        cy="50%"
        labelLine={false}
        outerRadius={150}
        fill="#8884d8"
        dataKey="value"
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
      <Tooltip
        formatter={(value, name, props) => {
          const quantity = props.payload.quantity;  // Get the quantity from the payload
          return [`$${value.toFixed(2)} (Shares: ${quantity})`];  // Display the formatted string
        }}
      />
      <Legend />
    </PieChart>
  );
}
