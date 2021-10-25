import React, { useState } from 'react';

export const SearchBar = ({ setArticles }) => {
    const [query, setQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const search = () => {
        setIsLoading(true);
        try {
            console.log(query, 'fetched');
            setArticles([
                {
                    title: 'test',
                    body: 'test',
                    date: 'test',
                },
                {
                    title: 'test',
                    body: 'test',
                    date: 'test',
                },
                {
                    title: 'test',
                    body: 'test',
                    date: 'test',
                },
                {
                    title: 'test',
                    body: 'test',
                    date: 'test',
                },
            ]);
        } catch (e) {
            console.error(e);
            setArticles([]);
        } finally {
            setIsLoading(false);
        }
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
