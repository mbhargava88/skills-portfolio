import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../auth/AuthContext';
import { getExpenses, getSummary } from '../services/api';
import ExpenseForm from '../components/ExpenseForm';
import ExpenseList from '../components/ExpenseList';
import CategoryChart from '../components/CategoryChart';

const DashboardPage = () => {
  const { user, logout } = useContext(AuthContext);
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    if (user) {
      fetchExpenses();
      fetchSummary();
    }
  }, [user]);

  const fetchExpenses = async () => {
    try {
      const data = await getExpenses();
      setExpenses(data);
    } catch (error) {
      console.error('Failed to fetch expenses', error);
    }
  };

  const fetchSummary = async () => {
    try {
      const data = await getSummary('monthly');
      setSummary(data);
    } catch (error) {
      console.error('Failed to fetch summary', error);
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-2xl font-bold">Expense Tracker</h1>
              </div>
            </div>
            <div className="flex items-center">
              <span className="mr-4">Hello, {user.username}</span>
              <button
                onClick={logout}
                className="px-3 py-2 rounded-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="py-10">
        <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2">
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Dashboard</h3>
                  {summary && <CategoryChart data={summary} />}
                </div>
              </div>
            </div>
            <div className="md:col-span-1">
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Add Expense</h3>
                  <ExpenseForm onExpenseAdded={fetchExpenses} />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <ExpenseList expenses={expenses} onExpenseDeleted={fetchExpenses} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;
