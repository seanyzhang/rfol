import axios from 'axios';
import React from 'react'
import type { PlaidLinkOptions } from 'react-plaid-link';
import { logger } from '../utils/logger';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type PlaidLinkButtonProps = {
    linkToken: string;
    onSuccess?: (res: ExchangePublicTokenResponse) => void;
}

type ExchangePublicTokenResponse = {
    message: string;
    item: {
        uuid: string;
        plaid_item_id: string;
        institution_name: string;
    };
    accounts: {
        name: string;
        uuid: string;
        type: string;
        plaid_item_uuid: string;
    }[];
}
const PlaidLinkButton: React.FC<PlaidLinkButtonProps> = ({ linkToken, onSuccess }) => {
    const config: PlaidLinkOptions = {
        token: linkToken,
        onSuccess: async (public_token, metadata) => {
            try {
                const res = await axios.post(
                    `${API_BASE_URL}/plaid/exchange_public_token`,
                    { public_token },
                    { withCredentials: true }
                );
                if (onSuccess) onSuccess(res.data)
            } catch (error) {
                logger.error("Error creating session:", error);
            }
        }
    }

    const { open, ready, error } = usePlaidLink(config);
    
    return (
        <div>PlaidLinkButton</div>
    )
}

export default PlaidLinkButton