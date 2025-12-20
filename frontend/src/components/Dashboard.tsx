import React, { useEffect, useState } from 'react';
import {
    getExpensesByCategory,
    getExpensesOverTime
} from '../api/analytics';
import type {
    ExpensesByCategoryResponse,
    ExpenseOverTime
} from '../api/analytics';
import ExpenseByCategoryChart from './charts/ExpenseByCategoryChart';
import ExpenseOverTimeChart from './charts/ExpenseOverTimeChart';
import { TrendingDown, PieChart, Calendar, DollarSign } from 'lucide-react';

const Dashboard: React.FC = () => {
    const [byCategory, setByCategory] = useState<ExpensesByCategoryResponse | null>(null);
    const [overTime, setOverTime] = useState<ExpenseOverTime[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [categoryData, timeData] = await Promise.all([
                    getExpensesByCategory(),
                    getExpensesOverTime()
                ]);
                setByCategory(categoryData);
                setOverTime(timeData);
            } catch (err) {
                console.error('Error fetching dashboard data:', err);
                setError('Failed to load dashboard data. Please make sure the backend is running.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
                <strong className="font-bold">Error! </strong>
                <span className="block sm:inline">{error}</span>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
                    <div className="p-3 bg-indigo-50 rounded-lg text-indigo-600">
                        <DollarSign size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-500 font-medium">Total Expenses</p>
                        <p className="text-2xl font-bold text-gray-900">${byCategory?.total_amount.toLocaleString()}</p>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
                    <div className="p-3 bg-emerald-50 rounded-lg text-emerald-600">
                        <PieChart size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-500 font-medium">Categories</p>
                        <p className="text-2xl font-bold text-gray-900">{byCategory?.items.length}</p>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
                    <div className="p-3 bg-amber-50 rounded-lg text-amber-600">
                        <Calendar size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-500 font-medium">Days Tracked</p>
                        <p className="text-2xl font-bold text-gray-900">{overTime.length}</p>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
                    <div className="p-3 bg-rose-50 rounded-lg text-rose-600">
                        <TrendingDown size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-500 font-medium">Avg. Daily</p>
                        <p className="text-2xl font-bold text-gray-900">
                            ${overTime.length > 0 ? (byCategory!.total_amount / overTime.length).toFixed(2) : '0'}
                        </p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <h3 className="text-lg font-semibold text-gray-800 mb-6 flex items-center">
                        <PieChart className="mr-2 text-indigo-600" size={20} />
                        Expenses by Category
                    </h3>
                    {byCategory && <ExpenseByCategoryChart data={byCategory.items} />}
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <h3 className="text-lg font-semibold text-gray-800 mb-6 flex items-center">
                        <TrendingDown className="mr-2 text-indigo-600" size={20} />
                        Expenses Over Time
                    </h3>
                    <ExpenseOverTimeChart data={overTime} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
