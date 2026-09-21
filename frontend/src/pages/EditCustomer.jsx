import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
    getCustomer,
    updateCustomer,
} from "../api/customer";

function EditCustomer() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [form, setForm] = useState({
        company_name: "",
        contact_person: "",
        phone: "",
        email: "",
    });

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadCustomer = async () => {
            try {
                const customer = await getCustomer(Number(id));

                setForm({
                    company_name: customer.company_name,
                    contact_person: customer.contact_person || "",
                    phone: customer.phone || "",
                    email: customer.email || "",
                });
            } catch (error) {
                console.error(error);
                setError("Failed to load customer.");
            } finally {
                setLoading(false);
            }
        };

        loadCustomer();
    }, [id]);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setSaving(true);
        setError("");

        try {
            await updateCustomer(Number(id), {
                company_name: form.company_name,
                contact_person: form.contact_person,
                phone: form.phone || null,
                email: form.email || null,
            });

            navigate("/customers");
        } catch (error) {
            console.error(error);
            setError("Failed to update customer.");
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <p>Loading customer...</p>;
    }

    if (error && !form.company_name) {
        return <p>{error}</p>;
    }

    return (
        <div>
            <h1>Edit Customer</h1>

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

                <button type="submit" disabled={saving}>
                    {saving ? "Saving..." : "Update Customer"}
                </button>

                {" "}

                <button
                    type="button"
                    onClick={() => navigate("/customers")}
                >
                    Cancel
                </button>
            </form>
        </div>
    );
}

export default EditCustomer;