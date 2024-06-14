import React, { useState, useEffect } from 'react';
import '../static/bootstrap.min.css';


function TableRow({ id, description, amount, category, loan, regularpayment, date, approved }) {
    let rowClassName = approved ? 'table-success' : 'table-warning';
    return (
        <tr key={id} className={rowClassName}>
            <td>{description}</td>
            <td>{amount}</td>
            <td>{category}</td>
            <td>{loan}</td>
            <td>{regularpayment}</td>
            <td>{date}</td>
            <td></td>
        </tr>
    )
};


const Expenses = () => {
    // State to hold the fetched blog posts
    const [expenses, setExpenses] = useState([]);
    let url = 'http://127.0.0.1:8000/backend/expenses/';

    useEffect(() => {
        fetch(url, {
                method: 'GET',
                modes: 'cors',
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
        .then(response => response.json())
        .then(data => {
            setExpenses(data)
        })
        .catch(error => console.error(error));
    }, []);
    
    // Render the fetched blog posts
    return (
        <div>
            <h1 key='heading'>Expenses for {sessionStorage.getItem('username')}</h1>
            <p>{Object.keys(expenses).length}</p>

            <table className="table table-hover">
                <thead>
                <tr>
                    <th scope="col">Description</th>
                    <th scope="col">Amount</th>
                    <th scope="col">Category</th>
                    <th scope="col">Loan</th>
                    <th scope="col">Regular Payment</th>
                    <th scope="col">Date</th>
                    <th scope="col"></th>
                </tr>
                </thead>
                <tbody>
                    {expenses.map((expense) => (
                        <TableRow
                            id = {expense.pk}
                            description = {expense.fields.description}
                            amount = {expense.fields.amount}
                            category = {expense.fields.category}
                            loan = {expense.fields.loan}
                            regularpayment = {expense.fields.regularpayment}
                            date = {expense.fields.date}
                            approved = {expense.fields.approved}
                        />
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default Expenses