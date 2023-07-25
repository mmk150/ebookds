import React, { useEffect } from 'react'
import '../App.css'
import { useNavigate } from 'react-router-dom'


function NotFound() {
  const navigate= useNavigate()
  useEffect(()=> {
    setTimeout(()=>{
      navigate("/",{replace:true})
    }
    ,2000)
  },[])
 


  return (
    <div className='notfound'>NotFound</div>
  )
}

export default NotFound