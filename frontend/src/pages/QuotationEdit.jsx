import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
    getQuotationDetails,
    updateQuotation,
} from "../api/quotation";

function QuotationEdit() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [quotation, setQuotation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [quotationDate, setQuotationDate] = useState("");
    const [validUntil, setValidUntil] = useState("");
    const [status, setStatus] = useState("");
    const [vatPercentage, setVatPercentage] = useState("");

    useEffect(() => {
        const loadQuotation = async () => {
            try {
                const data = await getQuotationDetails(Number(id));
                setQuotation(data);
                setQuotationDate(data.quotation_date);
                setValidUntil(data.valid_until);
                setStatus(data.status);
                setVatPercentage(data.vat_percentage);
            } catch (error) {
                console.error(error);
                setError("Failed to load quotation.");
            } finally {
                setLoading(false);
            }
        };

        loadQuotation();
    }, [id]);

    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");
        setSaving(true);

        try {
            await updateQuotation(Number(id), {
                quotation_date: quotationDate,
                valid_until: validUntil,
                status: status,
                vat_percentage: vatPercentage,
            });

            navigate(`/quotations/${id}`);
        } catch (error) {
            console.error(error);

            if (error.response?.data?.detail) {
                setError(error.response.data.detail);
            } else {
                setError("Failed to update quotation.");
            }
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <p>Loading quotation...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    if (!quotation) {
        return <p>Quotation not found.</p>;
    }

    return (
        <div>
            <h1>Edit Quotation</h1>

            <p>
                <strong>Quotation Number:</strong>{" "}
                {quotation.quotation_number}
            </p>

            <p>
                <strong>Customer:</strong>{" "}
                {quotation.customer.company_name}
            </p>

            <p>
                <strong>Status:</strong> {quotation.status}
            </p>

            <hr />

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Quotation Date</label>
                    <br />
                    <input
                        type="date"
                        value={quotationDate}
                        onChange={(event) => setQuotationDate(event.target.value)}
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
                    />
                </div>

                <br />

                <div>
                    <label>Status</label>
                    <br />
                    <select
                        value={status}
                        onChange={(event) => setStatus(event.target.value)}
                    >
                        <option value="draft">Draft</option>
                        <option value="sent">Sent</option>
                        <option value="approved">Approved</option>
                        <option value="accepted">Accepted</option>
                        <option value="rejected">Rejected</option>
                        <option value="cancelled">Cancelled</option>
                    </select>
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
                    />
                </div>

                <br />

                {error && <p>{error}</p>}

                <button type="submit" disabled={saving}>
                    {saving ? "Saving..." : "Save Changes"}
                </button>
            </form>

            <br />

            <Link to={`/quotations/${quotation.id}`}>
                Cancel
            </Link>
        </div>
    );
}

export default QuotationEdit;
