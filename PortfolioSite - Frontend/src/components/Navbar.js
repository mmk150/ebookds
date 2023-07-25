import React, { useState} from 'react';
import { Link, animateScroll as scroll } from 'react-scroll';
import './Navbar.css';

//


const Navbar =() => {
    const [click,setClick] = useState(false);
    const handleBurgerClick = () => setClick(!click);
    const closeMobileMenu= () => setClick(false); 
   
    

    const [button,setButton] = useState(true);
    const showButton = () => {
        if(window.innerWidth <=960){
            setButton(false);
        } else {
            setButton(true);
        }
    };

    window.addEventListener('resize',showButton);

    return (
        <>  
            <nav className='navbar'>
                <div className='navbar-container' id='section0'>
                    <Link to="/" className="navbar-logo">
                        EBOOK DATASCI <i className="fa-solid fa-book" />
                    </Link>
                    <ul className={click? 'nav-menu active': 'nav-menu'} >
                    <li className='nav-item'>
                        <Link
                        activeClass="active"
                        to="section1"
                        className='nav-links'
                        spy={true}
                        smooth={true}
                        offset={-70}
                        duration={500}
                        >
                        About
                        </Link>
                    </li>
                    <li className='nav-item'>
                    <Link
                        activeClass="active"
                        to="section2"
                        className='nav-links'
                        spy={true}
                        smooth={true}
                        offset={-70}
                        duration={500}
                        >
                        Thing
                    </Link>
                    </li>
                    <li className='nav-item'>
                    <Link
                        activeClass="active"
                        to="section3"
                        className='nav-links'
                        spy={true}
                        smooth={true}
                        offset={-70}
                        duration={500}
                        >
                        Merp
                    </Link>
                    </li>
                   

                    
                    </ul>
                    
                   </div>
            </nav>
        </>
    )
}

export default Navbar