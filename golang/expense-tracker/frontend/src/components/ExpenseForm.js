import React, { useState } from 'react';
import { createExpense } from '../services/api';

const ExpenseForm = ({ onExpenseAdded }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState('1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed'); // Default to Food

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createExpense({ amount: parseFloat(amount), description, category_id: categoryId, date: new Date() });
      setAmount('');
      setDescription('');
      onExpenseAdded();
    } catch (error) {
      console.error('Failed to create expense', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 mt-4">
      <div>
        <label htmlFor="amount" className="block text-sm font-medium text-gray-700">
          Amount
        </label>
        <div className="mt-1">
          <input
            type="number"
            name="amount"
            id="amount"
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
      </div>
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <div className="mt-1">
          <input
            type="text"
            name="description"
            id="description"
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
      </div>
      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700">
          Category
        </label>
        <div className="mt-1">
          <select
            id="category"
            name="category"
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
          >
            <option value="1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed">Food</option>
            <option value="2b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed">Travel</option>
            <option value="3b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed">Rent</option>
            <option value="4b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed">Shopping</option>
          </select>
        </div>
      </div>
      <button
        type="submit"
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Add Expense
      </button>
    </form>
  );
};

export default ExpenseForm;
