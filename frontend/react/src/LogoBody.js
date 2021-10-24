import React from 'react';
import LogoImage from '/public/assets/images/logo.png';

export const LogoBody = () => {
    return (
        <div id="logo">
            <a href="/">
                <img src={LogoImage} />
            </a>
        </div>
    );
};
