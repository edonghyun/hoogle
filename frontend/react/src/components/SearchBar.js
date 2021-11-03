import React, { useState } from 'react';

const BACKEND_SERVER_URL = 'http://localhost:8000/api/articles/';

export const SearchBar = ({ setArticles }) => {
    const [query, setQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const search = () => {
        setIsLoading(true);
        fetch(BACKEND_SERVER_URL)
            .then(setArticles)
            .catch((error) => {
                console.error(error);
                setArticles([]);
            })
            .finally(() => setIsLoading(false));
    };

    return (
        <div className="input-group mb-3 pl-5 pr-5">
            <input
                onChange={(e) => setQuery(e.target.value)}
                type="text"
                className="form-control"
                placeholder="Query to Search"
            />
            <div className="input-group-append">
                <button
                    onClick={search}
                    type="button"
                    className="input-group-text"
                    id="basic-addon2"
                >
                    search
                </button>
            </div>
        </div>
    );
};
