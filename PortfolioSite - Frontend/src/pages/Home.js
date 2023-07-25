import '../App.css'

import Banner from '../components/Banner/Banner.js'
import Bio from '../components/Bio/Bio';
import MarketAnalysis from '../components/MarketAnalysis/MarketAnalysis';
import Section from '../components/Section';
import './Home.css'
function Home () {
    return (
        <>
        <Section id='section1' title='Summary' >
            <Banner />
        </Section>
        <Section id='section2' title='Analysis'>
            <MarketAnalysis />
        </Section>
        <Section id='section3' title='About Us'>
            <Bio />
        </Section>
        </>
    )

}

export default Home;