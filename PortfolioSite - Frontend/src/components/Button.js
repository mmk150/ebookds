import React from 'react';
import {Link} from 'react-router-dom';

const STYLES= ['btnv--primary', 'btnv--outline'];
const SIZES = ['btnv--medium', 'btnv--large'];

export const Button = ({children,type,onClick,buttonStyle,buttonSize,link})=> {
    const checkButtonStyle = STYLES.includes(buttonStyle) ? buttonStyle : STYLES[0]
    const checkButtonSize = SIZES.includes(buttonSize) ? buttonSize: SIZES[0]
    const destination = link == null ? '/' : link
    return (
        <Link to={destination} className='btn-mobile'>
            <button
            className={`btnv ${checkButtonStyle} ${checkButtonSize}`}
            onClick={onClick}
            type={type}
            >
                {children}
            </button>
        </Link>
    )
};