import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
    getCustomers,
    deleteCustomer,
} from "../api/customer";

function Customers() {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [deletingId, setDeletingId] = useState(null);

    useEffect(() => {
        const loadCustomers = async () => {
            try {
                const data = await getCustomers();
                setCustomers(data);
            } catch (error) {
                console.error(error);
                setError("Failed to load customers.");
            } finally {
                setLoading(false);
            }
        };

        loadCustomers();
    }, []);

    const handleDelete = async (id) => {
        const confirmed = window.confirm(
            "Are you sure you want to delete this customer?"
        );

        if (!confirmed) {
            return;
        }

        setDeletingId(id);
        setError("");

        try {
            await deleteCustomer(id);

            setCustomers((currentCustomers) =>
                currentCustomers.filter(
                    (customer) => customer.id !== id
                )
            );
        } catch (error) {
            console.error(error);
            setError("Failed to delete customer.");
        } finally {
            setDeletingId(null);
        }
    };

    if (loading) {
        return <p>Loading customers...</p>;
    }

    return (
        <div>
            <h1>Customers</h1>

            <Link to="/customers/new">
                <button>Add Customer</button>
            </Link>

            <br />
            <br />

            {error && <p>{error}</p>}

            {customers.length === 0 ? (
                <p>No customers found.</p>
            ) : (
                <table border="1" cellPadding="8">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Company Name</th>
                            <th>Contact Person</th>
                            <th>Phone</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        {customers.map((customer) => (
                            <tr key={customer.id}>
                                <td>{customer.id}</td>
                                <td>{customer.company_name}</td>
                                <td>{customer.contact_person}</td>
                                <td>{customer.phone || "-"}</td>
                                <td>{customer.email || "-"}</td>

                                <td>
                                    <Link
                                        to={`/customers/${customer.id}/edit`}
                                    >
                                        <button>Edit</button>
                                    </Link>

                                    {" "}

                                    <button
                                        onClick={() =>
                                            handleDelete(customer.id)
                                        }
                                        disabled={
                                            deletingId === customer.id
                                        }
                                    >
                                        {deletingId === customer.id
                                            ? "Deleting..."
                                            : "Delete"}
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default Customers;