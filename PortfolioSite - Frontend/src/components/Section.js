import React from 'react';
import './Section.css';

import { Fieldset } from 'primereact/fieldset';
        

function Section({ title, id, children }) {
  return (
    <>
    <div className='section-top' />
    <div className='section' id={id}>
        <Fieldset legend={title}>
               {children}
        </Fieldset>
    </div>
    <div className='section-filler' />
    </>
  )
}

export default Section;

