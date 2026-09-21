import { Link, Outlet } from "react-router-dom";

function Layout() {
    return (
        <div>
            <header>
                <h2>Quotation Management System</h2>
            </header>

            <nav>
                <Link to="/dashboard">Dashboard</Link>
                {" | "}
                <Link to="/customers">Customers</Link>
                {" | "}
                <Link to="/quotations">Quotations</Link>
            </nav>

            <main>
                <Outlet />
            </main>
        </div>
    );
}

export default Layout;