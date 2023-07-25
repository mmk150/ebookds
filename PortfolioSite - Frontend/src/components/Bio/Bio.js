import React from 'react'
import MattBio from './MattBio'
import GeorgeBio from './GeorgeBio'
import './Bio.css'

function Bio() {
  return (
    <>
    <div className='bio-container'>
    <MattBio />
    <GeorgeBio />
    </div>
    </>
    
  )
}

export default Bio