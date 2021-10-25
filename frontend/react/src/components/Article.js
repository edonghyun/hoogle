import React from 'react';

export const Article = ({ title, date, body }) => {
    return (
        <>
            <div className="resultRow">
                <div className="title">
                    <a href="" target="_blank">
                        {title}
                    </a>
                </div>
                <div className="publishingDate">
                    <span>Published : </span>
                    {date}
                </div>
                <div className="article">{body}</div>
            </div>
        </>
    );
};
