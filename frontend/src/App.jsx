import { useState } from "react";
import api from "./api/axios";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";
import Customers from "./pages/Customer";
import AddCustomer from "./pages/AddCustomer";
import EditCustomer from "./pages/EditCustomer";
import Quotations from "./pages/Quotation";
import QuotationNew from "./pages/QuotationNew";
import QuotationDetails from "./pages/QuotationDetails";
import QuotationEdit from "./pages/QuotationEdit";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route element={<ProtectedRoute><Layout /></ProtectedRoute>} >
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/customers/new" element={<AddCustomer />} />
            <Route path="/customers/:id/edit" element={<EditCustomer />} />
            <Route path="/quotations" element={<Quotations />} />
            <Route path="/quotations/new" element={<QuotationNew />} />
            <Route path="/quotations/:id" element={<QuotationDetails />} />
            <Route path="/quotations/:id/edit" element={<QuotationEdit />} />
          </Route>
        </Routes>
      </BrowserRouter>


    </div>
  );

}




export default App;