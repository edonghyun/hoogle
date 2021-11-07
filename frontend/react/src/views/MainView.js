import React, { useState, useEffect } from 'react';

import { Header, Article, LogoContainer, SearchBar } from '../components';

export const MainView = () => {
    const [articles, setArticles] = useState([]);

    return (
        <div id="main-body">
            <Header />
            <LogoContainer />
            <SearchBar setArticles={setArticles} />
            {articles.length > 0 && (
                <div className="searchResult" id="searchResult">
                    {articles.map((article) => (
                        <Article {...article} />
                    ))}
                </div>
            )}
        </div>
    );
};
