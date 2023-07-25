import React from 'react'
import '../../App.css';
import './Banner.css';
import LeftBanner from './LeftBanner';
import RightBanner from './RightBanner';

function Banner() {
  return (
    <div className='container'>
       <div className='container-header'>
       </div>
       <LeftBanner />
       <RightBanner />

    </div>
  )
}

export default Banner