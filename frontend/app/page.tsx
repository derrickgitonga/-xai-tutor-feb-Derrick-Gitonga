'use client';

import { useState, useEffect, useCallback } from 'react';
import Layout from './components/layout/Layout';
import StatsCards from './components/orders/StatsCards';
import FilterTabs from './components/orders/FilterTabs';
import OrdersTable from './components/orders/OrdersTable';
import BulkActionBar from './components/orders/BulkActionBar';
import Pagination from './components/orders/Pagination';
import { Clock, FileText, Plus } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

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

interface Stats {
  total_orders_this_month: number;
  pending_orders: number;
  shipped_orders: number;
  refunded_orders: number;
}

interface OrdersResponse {
  orders: Order[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [stats, setStats] = useState<Stats>({
    total_orders_this_month: 0,
    pending_orders: 0,
    shipped_orders: 0,
    refunded_orders: 0,
  });
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [activeTab, setActiveTab] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [loading, setLoading] = useState(true);
  const itemsPerPage = 10;

  const fetchOrders = useCallback(async () => {
    try {
      const response = await fetch(
        `${API_BASE}/orders?status=${activeTab}&page=${currentPage}&limit=${itemsPerPage}`
      );
      const data: OrdersResponse = await response.json();
      setOrders(data.orders);
      setTotalPages(data.total_pages);
      setTotalItems(data.total);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    }
  }, [activeTab, currentPage]);

  const fetchStats = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/orders/stats`);
      const data: Stats = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  }, []);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchOrders(), fetchStats()]);
      setLoading(false);
    };
    loadData();
  }, [fetchOrders, fetchStats]);

  const handleSelectOrder = (id: string) => {
    setSelectedIds((prev: Set<string>) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const handleSelectAll = () => {
    if (selectedIds.size === orders.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(orders.map((o: Order) => o.id)));
    }
  };

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    setCurrentPage(1);
    setSelectedIds(new Set());
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    setSelectedIds(new Set());
  };

  const handleDuplicate = async () => {
    try {
      const response = await fetch(`${API_BASE}/orders/bulk/duplicate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_ids: Array.from(selectedIds) }),
      });
      if (response.ok) {
        setSelectedIds(new Set());
        await fetchOrders();
        await fetchStats();
      }
    } catch (error) {
      console.error('Failed to duplicate orders:', error);
    }
  };

  const handlePrint = () => {
    // Print functionality - button only as per requirements
    console.log('Print orders:', Array.from(selectedIds));
  };

  const handleBulkDelete = async () => {
    try {
      const response = await fetch(`${API_BASE}/orders/bulk`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_ids: Array.from(selectedIds) }),
      });
      if (response.ok) {
        setSelectedIds(new Set());
        await fetchOrders();
        await fetchStats();
      }
    } catch (error) {
      console.error('Failed to delete orders:', error);
    }
  };

  const handleDeleteOrder = async (id: string) => {
    try {
      const response = await fetch(`${API_BASE}/orders/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        await fetchOrders();
        await fetchStats();
      }
    } catch (error) {
      console.error('Failed to delete order:', error);
    }
  };

  const handleEditOrder = (id: string) => {
    // Edit functionality - not required for this exercise
    console.log('Edit order:', id);
  };

  const handleClearSelection = () => {
    setSelectedIds(new Set());
  };

  return (
    <Layout>
      {/* Orders Section */}
      <div className="bg-white rounded-xl border border-gray-200">
        {/* Header */}
        <div className="flex items-center justify-between p-4">
          <h2 className="text-lg font-semibold text-gray-800">All Orders</h2>
          <div className="flex items-center gap-2">
            <button className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50">
              <Clock className="w-4 h-4" />
              Bulk Update Status
            </button>
            <button className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50">
              <FileText className="w-4 h-4" />
              Export Orders
            </button>
            <button className="flex items-center gap-2 px-4 py-2 text-sm text-white bg-gray-800 rounded-lg hover:bg-gray-700">
              <Plus className="w-4 h-4" />
              Add Orders
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="px-4">
          <StatsCards stats={stats} />
        </div>

        {/* Filter Tabs */}
        <div className="px-4">
          <FilterTabs activeTab={activeTab} onTabChange={handleTabChange} />
        </div>

        {/* Table */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-800"></div>
          </div>
        ) : (
          <div className="p-4 pt-0">
            <OrdersTable
              orders={orders}
              selectedIds={selectedIds}
              onSelectOrder={handleSelectOrder}
              onSelectAll={handleSelectAll}
              onEditOrder={handleEditOrder}
              onDeleteOrder={handleDeleteOrder}
            />

            {/* Pagination */}
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              totalItems={totalItems}
              itemsPerPage={itemsPerPage}
              onPageChange={handlePageChange}
            />
          </div>
        )}
      </div>

      {/* Bulk Action Bar */}
      <BulkActionBar
        selectedCount={selectedIds.size}
        onDuplicate={handleDuplicate}
        onPrint={handlePrint}
        onDelete={handleBulkDelete}
        onClose={handleClearSelection}
      />
    </Layout>
  );
}
