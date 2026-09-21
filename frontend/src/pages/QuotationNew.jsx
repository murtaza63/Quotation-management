import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createQuotation } from "../api/quotation";
import { getCustomers } from "../api/customer";

function QuotationNew() {
    const navigate = useNavigate();

    const [customers, setCustomers] = useState([]);

    const [customerId, setCustomerId] = useState("");
    const [quotationDate, setQuotationDate] = useState("");
    const [validUntil, setValidUntil] = useState("");
    const [vatPercentage, setVatPercentage] = useState("5.00");
    const [notes, setNotes] = useState("");

    const [loading, setLoading] = useState(false);
    const [loadingCustomers, setLoadingCustomers] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadCustomers = async () => {
            try {
                const data = await getCustomers();
                setCustomers(data);
            } catch (error) {
                console.error(error);
                setError("Failed to load customers.");
            } finally {
                setLoadingCustomers(false);
            }
        };

        loadCustomers();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await createQuotation({
                customer_id: Number(customerId),
                quotation_date: quotationDate,
                valid_until: validUntil,
                status: "draft",
                vat_percentage: vatPercentage,
                notes: notes || undefined,
            });

            navigate("/quotations");
        } catch (error) {
            console.error(error);

            if (error.response?.data?.detail) {
                setError(error.response.data.detail);
            } else {
                setError("Failed to create quotation.");
            }
        } finally {
            setLoading(false);
        }
    };

    if (loadingCustomers) {
        return <p>Loading customers...</p>;
    }

    return (
        <div>
            <h1>New Quotation</h1>

            {error && <p>{error}</p>}

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Customer</label>
                    <br />

                    <select
                        value={customerId}
                        onChange={(event) => setCustomerId(event.target.value)}
                        required
                    >
                        <option value="">Select customer</option>

                        {customers.map((customer) => (
                            <option key={customer.id} value={customer.id}>
                                {customer.company_name}
                            </option>
                        ))}
                    </select>
                </div>

                <br />

                <div>
                    <label>Quotation Date</label>
                    <br />

                    <input
                        type="date"
                        value={quotationDate}
                        onChange={(event) => setQuotationDate(event.target.value)}
                        required
                    />
                </div>

                <br />

                <div>
                    <label>Valid Until</label>
                    <br />

                    <input
                        type="date"
                        value={validUntil}
                        onChange={(event) => setValidUntil(event.target.value)}
                        required
                    />
                </div>

                <br />

                <div>
                    <label>VAT Percentage</label>
                    <br />

                    <input
                        type="number"
                        min="0"
                        max="100"
                        step="0.01"
                        value={vatPercentage}
                        onChange={(event) => setVatPercentage(event.target.value)}
                        required
                    />
                </div>

                <br />

                <div>
                    <label>Notes</label>
                    <br />

                    <textarea
                        value={notes}
                        onChange={(event) => setNotes(event.target.value)}
                        rows="4"
                    />
                </div>

                <br />

                <button type="submit" disabled={loading}>
                    {loading ? "Creating..." : "Create Quotation"}
                </button>

                {" "}

                <button
                    type="button"
                    onClick={() => navigate("/quotations")}
                    disabled={loading}
                >
                    Cancel
                </button>
            </form>
        </div>
    );
}

export default QuotationNew;