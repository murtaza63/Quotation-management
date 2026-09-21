import { useEffect, useState } from "react";
import { getQuotations } from "../api/quotation";
import { Link } from "react-router-dom";


function Quotations() {
    const [quotations, setQuotations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadQuotations = async () => {
            try {
                const data = await getQuotations();

                setQuotations(data.items);
            } catch (error) {
                console.error(error);
                setError("Failed to load quotations.");
            } finally {
                setLoading(false);
            }
        };

        loadQuotations();
    }, []);

    if (loading) {
        return <p>Loading quotations...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div>
            <h1>Quotations</h1>
            <Link to="/quotations/new">Create New Quotation</Link>
            {quotations.length === 0 ? (
                <p>No quotations found.</p>
            ) : (
                <table border="1" cellPadding="8">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Quotation No.</th>
                            <th>Customer ID</th>
                            <th>Date</th>
                            <th>Valid Until</th>
                            <th>Status</th>
                            <th>Subtotal</th>
                            <th>VAT</th>
                            <th>Total</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        {quotations.map((quotation) => (
                            <tr key={quotation.id}>
                                <td>{quotation.id}</td>
                                <td>{quotation.quotation_number}</td>
                                <td>{quotation.customer_id}</td>
                                <td>{quotation.quotation_date}</td>
                                <td>{quotation.valid_until}</td>
                                <td>{quotation.status}</td>
                                <td>{quotation.subtotal}</td>
                                <td>{quotation.vat_amount}</td>
                                <td>{quotation.total_amount}</td>
                                <td>
                                    <Link to={`/quotations/${quotation.id}`}>
                                        View Details
                                    </Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default Quotations;