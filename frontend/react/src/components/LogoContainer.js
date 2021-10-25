import React from 'react';

import LogoImage from '/public/assets/images/logo.png';

export const LogoContainer = () => {
    return (
        <div
            id="logo"
            className="w-100 d-flex justify-content-center pt-5 pb-5"
        >
            <a href="/">
                <img src={LogoImage} />
            </a>
        </div>
    );
};
