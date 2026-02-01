'use client';

interface Customer {
  name: string;
  email: string;
  avatar: string | null;
}

interface Order {
  id: string;
  order_number: string;
  customer: Customer;
  order_date: string;
  status: string;
  total_amount: number;
  payment_status: string;
}

interface OrdersTableProps {
  orders: Order[];
  selectedIds: Set<string>;
  onSelectOrder: (id: string) => void;
  onSelectAll: () => void;
  onEditOrder: (id: string) => void;
  onDeleteOrder: (id: string) => void;
}

export default function OrdersTable({
  orders,
  selectedIds,
  onSelectOrder,
  onSelectAll,
  onEditOrder,
  onDeleteOrder,
}: OrdersTableProps) {
  const allSelected = orders.length > 0 && orders.every((order) => selectedIds.has(order.id));

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  };

  const formatAmount = (amount: number) => {
    return `$${amount.toFixed(2)}`;
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      pending: 'bg-yellow-50 text-yellow-700',
      completed: 'bg-green-50 text-green-700',
      refunded: 'bg-red-50 text-red-700',
    };
    const style = styles[status as keyof typeof styles] || 'bg-gray-50 text-gray-700';
    const label = status.charAt(0).toUpperCase() + status.slice(1);
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${style}`}>
        {label}
      </span>
    );
  };

  return (
    <div className="overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-200">
            <th className="px-4 py-3 text-left w-12">
              <input
                type="checkbox"
                checked={allSelected}
                onChange={onSelectAll}
                className="w-4 h-4 rounded border-gray-300 bg-white text-gray-900 focus:ring-gray-500 accent-gray-900"
              />
            </th>
            <th className="px-4 py-3 text-left">
              <button className="flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Order Number
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              </button>
            </th>
            <th className="px-4 py-3 text-left">
              <button className="flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Customer Name
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              </button>
            </th>
            <th className="px-4 py-3 text-left">
              <button className="flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Order Date
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              </button>
            </th>
            <th className="px-4 py-3 text-left">
              <button className="flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Status
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              </button>
            </th>
            <th className="px-4 py-3 text-left">
              <button className="flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Total Amount
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              </button>
            </th>
            <th className="px-4 py-3 text-left">
              <button className="flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Payment Status
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              </button>
            </th>
            <th className="px-4 py-3 text-left">
              <span className="text-sm font-medium text-gray-500">Action</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr
              key={order.id}
              className={`border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                selectedIds.has(order.id) ? 'bg-blue-50' : ''
              }`}
            >
              <td className="px-4 py-3">
                <input
                  type="checkbox"
                  checked={selectedIds.has(order.id)}
                  onChange={() => onSelectOrder(order.id)}
                  className="w-4 h-4 rounded border-gray-300 bg-white text-gray-900 focus:ring-gray-500 accent-gray-900"
                />
              </td>
              <td className="px-4 py-3">
                <span className="text-sm font-medium text-gray-800">{order.order_number}</span>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-2">
                  <img
                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(order.customer.name)}&background=random&size=32`}
                    alt={order.customer.name}
                    className="w-8 h-8 rounded-full"
                  />
                  <span className="text-sm text-gray-700">{order.customer.name}</span>
                </div>
              </td>
              <td className="px-4 py-3">
                <span className="text-sm text-gray-600">{formatDate(order.order_date)}</span>
              </td>
              <td className="px-4 py-3">{getStatusBadge(order.status)}</td>
              <td className="px-4 py-3">
                <span className="text-sm text-gray-700">{formatAmount(order.total_amount)}</span>
              </td>
              <td className="px-4 py-3">
                <span className="text-sm text-gray-600 capitalize">{order.payment_status}</span>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onEditOrder(order.id)}
                    className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => onDeleteOrder(order.id)}
                    className="p-1 text-red-400 hover:text-red-600 hover:bg-red-50 rounded"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                  <button className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
