import React from 'react'
import MarketAnalysisImageCloud from './MarketAnalysisImageCloud'
import LeftMarket from './LeftMarket'
import RightMarket from './RightMarket'
import '../../App.css';
import './MarketAnalysis.css'

function MarketAnalysis() {
  return (
    <>
    <div className='market-analysis-container'>
  
    <div>MarketAnalysis</div>
    <div className='market-cloud'>
    <MarketAnalysisImageCloud />
    </div>
    </div>
    <div className='market-container' id='section2'>
      <LeftMarket />
      <RightMarket />
    </div>
    
    </>
    
  )
}

export default MarketAnalysis