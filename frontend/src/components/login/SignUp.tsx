import React, { useState } from 'react'
import { ANIMATION_DELAYS } from '../../constants';
import axios from 'axios';
import { logger } from '../../utils/logger';
import { type FieldErrors, type SubmitHandler, type UseFormRegister } from 'react-hook-form';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type SignUpFormData = {
    firstname: string;
    lastname: string;
    username: string;
    email: string;
    password: string;
}

type Props = {
    register: UseFormRegister<SignUpFormData>;
    handleSubmit: (onValid: SubmitHandler<SignUpFormData>) => (e?: React.BaseSyntheticEvent) => void;
    errors: FieldErrors<SignUpFormData>;
    setHasAccount: React.Dispatch<React.SetStateAction<boolean>>;
    setServerErr: React.Dispatch<React.SetStateAction<string>>;
}

type User_Data = {
    first_name: string,
    last_name: string,
    username: string,
    email: string,
    password: string
}

const SignUp = ({register, handleSubmit, errors, setHasAccount, setServerErr}: Props) => {
    
    const [showPw, setShowPw] = useState(false);
    const [showPwThrottle, setShowPwThrottle] = useState(false);

    const handleShowPW = () => {
        if (showPwThrottle) return;

        setShowPwThrottle(true);
        setShowPw(prev => !prev)
        setTimeout(() => setShowPwThrottle(false), ANIMATION_DELAYS.THROTTLE);
    }

    const submit: SubmitHandler<SignUpFormData> = async (data) => {
        const user_data: User_Data = {
            first_name: data.firstname, 
            last_name: data.lastname,
            username: data.username,
            email: data.email,
            password: data.password,
        }

        try {
            const res = await axios.post(`${API_BASE_URL}/users/create`, user_data);
            logger.log(res)
            setHasAccount(true);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                logger.error(error.response?.data?.detail || error.message);
                setServerErr(error.response?.data?.detail || error.message);
            } else {
                logger.error("Unknown error")
                setServerErr("Unexpected error occurred. Please try again.");
            }
        }
    } 

    return (
        <>
            <div className="flex justify-center">
                <p className="justify-center text-[2rem] pb-8 font-bold no-select"> Create An Account </p>
            </div>
            <form onSubmit={handleSubmit(submit)}>
                <div className="inputs grid items-center pb-8 grid-cols-2 grid-rows-4 gap-3">
                    <input 
                        autoComplete="off" 
                        id="firstname" 
                        placeholder="First name" 
                        type="text" 
                        {...register("firstname", { required: "First name is required" })}
                        className="inputBox firstname 
                        row-start-1 row-end-2 col-start-1 col-end-2" />
                    <input 
                        autoComplete="off" 
                        id="lastname" 
                        placeholder="Last name" 
                        type="text" 
                        {...register("lastname", { required: "Last name is required" })}
                        className="inputBox lastname 
                        row-start-1 row-end-2 col-start-2 col-end-3" />
                    <input 
                        autoComplete="off" 
                        id="username" 
                        placeholder="Username" 
                        type="text"
                        {...register("username", { required: "Username is required" })}
                        className="inputBox username 
                        row-start-2 row-end-3 col-start-1 col-end-3" />
                    <input 
                        autoComplete="off" 
                        id="email"
                        placeholder="Email" 
                        type="text" 
                        {...register("email", { required: "Email is required" })}
                        className="inputBox email 
                        row-start-3 row-end-4 col-start-1 col-end-3" /> 
                    <div className="pwContainer relative flex
                    row-start-4 row-end-5 col-start-1 col-end-3">
                        <input 
                            placeholder="Password" 
                            id="password" 
                            type={`${showPw ? "text" : "password"}`} 
                            onCopy={(e) => e.preventDefault()}
                            onCut={(e) => e.preventDefault()}
                            onPaste={(e) => e.preventDefault()}
                            {...register("password", 
                                { 
                                    required: "Password is required",
                                    minLength: {
                                        value: 8,
                                        message: "Password must be at least 8 characters"
                                    },
                                    pattern: {
                                        value: /^(?=.*[!@#$%^&*])/,
                                        message: "Password must contain at least one special character (!@#$%^&*)"
                                    }
                                }
                            )}
                            className="inputBox password w-[100%]" /> 
                        <button type='button' onClick={handleShowPW} 
                        className="showPw absolute right-2 top-1/2 -translate-y-1/2 text-sm text-text bg-bg-primary px-2 py-1 rounded-full cursor-pointer">
                            {showPw ? "Hide" : "Show"}
                        </button>
                    </div>
                </div>
                <div className="flex justify-center w-[50%] aspect-3/1 m-auto rounded-4xl cursor-pointer
                text-text bg-bg-secondary hover:text-text-dark hover:bg-bg-secondary-dark
                transition-all transition:300ms ease-in-out">
                    <button type="submit" 
                    className="enter cursor-pointer w-full text-xl">
                        <p className="no-select"> Join </p>
                    </button>
                </div>
            </form>
        </>
    ) 
}

export default SignUp