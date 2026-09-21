import { useState } from "react";
import { createCustomer } from "../api/customer";

function AddCustomer() {
    const [form, setForm] = useState({
        company_name: "",
        contact_person: "",
        phone: "",
        email: "",
    });

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setMessage("");
        setError("");
        setLoading(true);

        try {
            await createCustomer({
                company_name: form.company_name,
                contact_person: form.contact_person,
                phone: form.phone || null,
                email: form.email || null,
            });

            setMessage("Customer created successfully.");

            setForm({
                company_name: "",
                contact_person: "",
                phone: "",
                email: "",
            });
        } catch (error) {
            console.error(error);
            setError("Failed to create customer.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Add Customer</h1>

            {message && <p>{message}</p>}
            {error && <p>{error}</p>}

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Company Name</label>
                    <br />
                    <input
                        type="text"
                        name="company_name"
                        value={form.company_name}
                        onChange={handleChange}
                        required
                    />
                </div>

                <br />

                <div>
                    <label>Contact Person</label>
                    <br />
                    <input
                        type="text"
                        name="contact_person"
                        value={form.contact_person}
                        onChange={handleChange}
                    />
                </div>

                <br />

                <div>
                    <label>Phone</label>
                    <br />
                    <input
                        type="text"
                        name="phone"
                        value={form.phone}
                        onChange={handleChange}
                    />
                </div>

                <br />

                <div>
                    <label>Email</label>
                    <br />
                    <input
                        type="email"
                        name="email"
                        value={form.email}
                        onChange={handleChange}
                    />
                </div>

                <br />

                <button type="submit" disabled={loading}>
                    {loading ? "Creating..." : "Create Customer"}
                </button>
            </form>
        </div>
    );
}

export default AddCustomer;