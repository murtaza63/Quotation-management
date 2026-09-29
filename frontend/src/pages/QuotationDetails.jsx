import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
    getQuotationDetails,
    createQuotationItem,
    deleteQuotationItem,
    updateQuotationItem
} from "../api/quotation";

function QuotationDetails() {
    const { id } = useParams();

    const [quotation, setQuotation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [description, setDescription] = useState("");
    const [quantity, setQuantity] = useState("");
    const [unit, setUnit] = useState("");
    const [unitPrice, setUnitPrice] = useState("");
    const [addingItem, setAddingItem] = useState(false);
    const [editingItemId, setEditingItemId] = useState(null);
    const [editDescription, setEditDescription] = useState("");
    const [editQuantity, setEditQuantity] = useState("");
    const [editUnit, setEditUnit] = useState("");
    const [editUnitPrice, setEditUnitPrice] = useState("");
    const [updatingItem, setUpdatingItem] = useState(false);
    const [deletingItemId, setDeletingItemId] = useState(null);

    useEffect(() => {
        const loadQuotation = async () => {
            try {
                const data = await getQuotationDetails(Number(id));
                setQuotation(data);
            } catch (error) {
                console.error(error);
                setError("Failed to load quotation.");
            } finally {
                setLoading(false);
            }
        };

        loadQuotation();
    }, [id]);

    const handleAddItem = async (event) => {
        event.preventDefault();

        setError("");
        setAddingItem(true);

        try {
            await createQuotationItem(Number(id), {
                description,
                quantity,
                unit,
                unit_price: unitPrice,
            });

            setDescription("");
            setQuantity("");
            setUnit("");
            setUnitPrice("");

            const updatedQuotation = await getQuotationDetails(Number(id));
            setQuotation(updatedQuotation);
        } catch (error) {
            console.error(error);

            if (error.response?.data?.detail) {
                setError(error.response.data.detail);
            } else {
                setError("Failed to add quotation item.");
            }
        } finally {
            setAddingItem(false);
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
    const handleEditItem = (item) => {
        setEditingItemId(item.id);
        setEditDescription(item.description);
        setEditQuantity(item.quantity);
        setEditUnit(item.unit);
        setEditUnitPrice(item.unit_price);
    };
    const handleUpdateItem = async (event) => {
        event.preventDefault();

        setError("");
        setUpdatingItem(true);

        try {
            await updateQuotationItem(editingItemId, {
                description: editDescription,
                quantity: editQuantity,
                unit: editUnit,
                unit_price: editUnitPrice,
            });

            setEditingItemId(null);
            setEditDescription("");
            setEditQuantity("");
            setEditUnit("");
            setEditUnitPrice("");

            const updatedQuotation = await getQuotationDetails(Number(id));
            setQuotation(updatedQuotation);
        } catch (error) {
            console.error(error);

            if (error.response?.data?.detail) {
                setError(error.response.data.detail);
            } else {
                setError("Failed to update quotation item.");
            }
        } finally {
            setUpdatingItem(false);
        }
    };

    const handleDeleteItem = async (itemId) => {
        const confirmed = window.confirm("Are you sure you want to delete this item?"
        );
        if (!confirmed) {
            return;
        }
        setError("");
        setDeletingItemId(itemId);

        try {
            await deleteQuotationItem(itemId);
            const updatedQuotation = await getQuotationDetails(Number(id));
            setQuotation(updatedQuotation);
        } catch (error) {
            console.error(error);
            if (error.response?.data?.detail) {
                setError(error.response.data.detail);
            } else {
                setError("Failed to delete quotation item.");
            }
        } finally {
            setDeletingItemId(null);
        }
    };

    return (
        <div>
            <h1>Quotation Details</h1>

            <p>
                <strong>Quotation No:</strong>{" "}
                {quotation.quotation_number}
            </p>

            <p>
                <strong>Status:</strong> {quotation.status}
            </p>

            <p>
                <strong>Quotation Date:</strong>{" "}
                {quotation.quotation_date}
            </p>

            <p>
                <strong>Valid Until:</strong>{" "}
                {quotation.valid_until}
            </p>
            <br />

            <Link to={`/quotations/${quotation.id}/edit`}>
                Edit Quotation
            </Link>

            <hr />

            <h2>Customer</h2>

            <p>
                <strong>Company:</strong>{" "}
                {quotation.customer.company_name}
            </p>

            <p>
                <strong>Contact Person:</strong>{" "}
                {quotation.customer.contact_person}
            </p>

            <p>
                <strong>Phone:</strong>{" "}
                {quotation.customer.phone || "-"}
            </p>

            <p>
                <strong>Email:</strong>{" "}
                {quotation.customer.email || "-"}
            </p>

            <hr />

            <h2>Items</h2>

            {quotation.items.length === 0 ? (
                <p>No items added.</p>
            ) : (
                <table border="1" cellPadding="8">
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th>Quantity</th>
                            <th>Unit</th>
                            <th>Unit Price</th>
                            <th>Total</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        {quotation.items.map((item) => (
                            <tr key={item.id}>
                                <td>{item.description}</td>
                                <td>{item.quantity}</td>
                                <td>{item.unit}</td>
                                <td>{item.unit_price}</td>
                                <td>{item.total}</td>
                                <td>
                                    <button
                                        onClick={() => handleEditItem(item)}
                                        disabled={deletingItemId === item.id}
                                    >
                                        Edit
                                    </button>{" "}

                                    <button
                                        onClick={() => handleDeleteItem(item.id)}
                                        disabled={deletingItemId === item.id}
                                    >
                                        {deletingItemId === item.id ? "Deleting..." : "Delete"}
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {editingItemId && (
                <div>
                    <h3>Edit Item</h3>
                    <form onSubmit={handleUpdateItem}>
                        <div>
                            <label>Description</label>
                            <br />
                            <input
                                type="text"
                                value={editDescription}
                                onChange={(event) =>
                                    setEditDescription(event.target.value)
                                }
                                required
                            />
                        </div>

                        <br />

                        <div>
                            <label>Quantity</label>
                            <br />
                            <input
                                type="number"
                                min="0.01"
                                step="0.01"
                                value={editQuantity}
                                onChange={(event) =>
                                    setEditQuantity(event.target.value)
                                }
                                required
                            />
                        </div>

                        <br />

                        <div>
                            <label>Unit</label>
                            <br />
                            <input
                                type="text"
                                value={editUnit}
                                onChange={(event) =>
                                    setEditUnit(event.target.value)
                                }
                                placeholder="m2"
                                required
                            />
                        </div>

                        <br />

                        <div>
                            <label>Unit Price</label>
                            <br />
                            <input
                                type="number"
                                min="0.01"
                                step="0.01"
                                value={editUnitPrice}
                                onChange={(event) =>
                                    setEditUnitPrice(event.target.value)
                                }
                                required
                            />
                        </div>

                        <br />

                        <button type="submit" disabled={updatingItem}>
                            {updatingItem ? "Updating..." : "Update Item"}
                        </button>
                    </form>
                </div>
            )}

            <br />

            <h3>Add Item</h3>

            <form onSubmit={handleAddItem}>
                <div>
                    <label>Description</label>
                    <br />

                    <input
                        type="text"
                        value={description}
                        onChange={(event) =>
                            setDescription(event.target.value)
                        }
                        required
                    />
                </div>

                <br />

                <div>
                    <label>Quantity</label>
                    <br />

                    <input
                        type="number"
                        min="0.01"
                        step="0.01"
                        value={quantity}
                        onChange={(event) =>
                            setQuantity(event.target.value)
                        }
                        required
                    />
                </div>

                <br />

                <div>
                    <label>Unit</label>
                    <br />

                    <input
                        type="text"
                        value={unit}
                        onChange={(event) =>
                            setUnit(event.target.value)
                        }
                        placeholder="m2"
                        required
                    />
                </div>

                <br />

                <div>
                    <label>Unit Price</label>
                    <br />

                    <input
                        type="number"
                        min="0.01"
                        step="0.01"
                        value={unitPrice}
                        onChange={(event) =>
                            setUnitPrice(event.target.value)
                        }
                        required
                    />
                </div>

                <br />

                <button type="submit" disabled={addingItem}>
                    {addingItem ? "Adding..." : "Add Item"}
                </button>
            </form>

            <hr />

            <h2>Summary</h2>

            <p>
                <strong>Subtotal:</strong>{" "}
                {quotation.subtotal}
            </p>

            <p>
                <strong>
                    VAT ({quotation.vat_percentage}%):
                </strong>{" "}
                {quotation.vat_amount}
            </p>

            <p>
                <strong>Total Amount:</strong>{" "}
                {quotation.total_amount}
            </p>

            <p>
                <strong>Notes:</strong>{" "}
                {quotation.notes || "-"}
            </p>

            <br />

            <Link to="/quotations">
                ← Back to Quotations
            </Link>
        </div>
    );
}

export default QuotationDetails;