'use client';

interface Stats {
  total_orders_this_month: number;
  pending_orders: number;
  shipped_orders: number;
  refunded_orders: number;
}

interface StatsCardsProps {
  stats: Stats;
}

export default function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      label: 'Total Orders This Month',
      value: stats.total_orders_this_month,
      dotColor: 'bg-blue-500',
    },
    {
      label: 'Pending Orders',
      value: stats.pending_orders,
      dotColor: 'bg-yellow-500',
    },
    {
      label: 'Shipped Orders',
      value: stats.shipped_orders,
      dotColor: 'bg-green-500',
    },
    {
      label: 'Refunded Orders',
      value: stats.refunded_orders,
      dotColor: 'bg-red-500',
    },
  ];

  return (
    <div className="grid grid-cols-4 divide-x divide-gray-200 border border-gray-200 rounded-xl mb-4">
      {cards.map((card, index) => (
        <div
          key={index}
          className="p-4"
        >
          <div className="flex items-center gap-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${card.dotColor}`}></div>
            <span className="text-sm text-gray-500">{card.label}</span>
          </div>
          <p className="text-2xl font-semibold text-gray-800">{card.value}</p>
        </div>
      ))}
    </div>
  );
}
