import React from 'react'
import './LoadingIcon.css'

const LoadingIcon = () => {
  return (
    <div className="loading-icon m-0 flex bg-transparent justify-center ">
        <div className="bullet one"></div>
        <div className="bullet two"></div>
        <div className="bullet three"></div>
    </div>
  )
}

export default LoadingIcon