import api from "./axios";

export interface Quotation {
    id: number;
    quotation_number: string;
    customer_id: number;
    quotation_date: string;
    valid_until: string;
    status: string;
    vat_percentage: string;
    subtotal: string;
    vat_amount: string;
    total_amount: string;
    notes: string | null;
    created_at: string;
}

export interface QuotationListResponse {
    items: Quotation[];
    total: number;
    skip: number;
    limit: number;
}

export const getQuotations = async (): Promise<QuotationListResponse> => {
    const response = await api.get<QuotationListResponse>("/quotations");

    return response.data;
};


export interface QuotationCreate {
    customer_id: number;
    quotation_date: string;
    valid_until: string;
    status?: string;
    vat_percentage: string;
    notes?: string;
}

export const createQuotation = async (
    quotation: QuotationCreate
): Promise<Quotation> => {
    const response = await api.post<Quotation>("/quotations", quotation);

    return response.data;
};

export interface QuotationUpdate {
    customer_id?: number;
    quotation_date?: string;
    valid_until?: string;
    status?: string;
    vat_percentage?: string;
}

export const updateQuotation = async (
    quotationId: number,
    quotation: QuotationUpdate
): Promise<Quotation> => {
    const response = await api.put<Quotation>(
        `/quotations/${quotationId}`,
        quotation
    );

    return response.data;
};

export interface CustomerDetails {
    id: number;
    company_name: string;
    contact_person: string;
    phone: string | null;
    email: string | null;
}

export interface QuotationItem {
    id: number;
    quotation_id: number;
    description: string;
    quantity: string;
    unit: string;
    unit_price: string;
    total: string;
}

export interface QuotationDetails extends Quotation {
    customer: CustomerDetails;
    items: QuotationItem[];
}

export const getQuotationDetails = async (
    quotationId: number
): Promise<QuotationDetails> => {
    const response = await api.get<QuotationDetails>(
        `/quotations/${quotationId}/details`
    );

    return response.data;
};

export interface QuotationItemCreate {
    description: string;
    quantity: string;
    unit: string;
    unit_price: string;
}

export interface QuotationItemUpdate {
    description?: string;
    quantity?: string;
    unit?: string;
    unit_price?: string;
}

export const createQuotationItem = async (
    quotationId: number,
    item: QuotationItemCreate
): Promise<QuotationItem> => {
    const response = await api.post<QuotationItem>(
        `/quotations/${quotationId}/items`,
        item
    );

    return response.data;
};

export const updateQuotationItem = async (
    itemId: number,
    item: QuotationItemUpdate
): Promise<QuotationItem> => {
    const response = await api.put<QuotationItem>(
        `/quotation-items/${itemId}`,
        item
    );

    return response.data;
};

export const deleteQuotationItem = async (itemId: number): Promise<void> => {
    await api.delete(`/quotation-items/${itemId}`);
}