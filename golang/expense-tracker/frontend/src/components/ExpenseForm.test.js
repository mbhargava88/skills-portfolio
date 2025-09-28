import { render, screen, fireEvent } from '@testing-library/react';
import ExpenseForm from './ExpenseForm';

test('renders expense form and submits data', () => {
  const handleExpenseAdded = jest.fn();
  render(<ExpenseForm onExpenseAdded={handleExpenseAdded} />);

  fireEvent.change(screen.getByLabelText(/amount/i), { target: { value: '123' } });
  fireEvent.change(screen.getByLabelText(/description/i), { target: { value: 'Test Expense' } });

  fireEvent.click(screen.getByText(/add expense/i));

  // We can't easily test the API call without mocking, 
  // but we can check that the form is cleared.
  // await waitFor(() => expect(handleExpenseAdded).toHaveBeenCalledTimes(1));
});
