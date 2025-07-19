import axios from 'axios';
import { logger } from '../../utils/logger';
import { type FieldErrors, type SubmitHandler, type UseFormRegister } from 'react-hook-form';
import { useState } from 'react';
import { ANIMATION_DELAYS } from '../../constants';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type SignInFormData = {
    query: string;
    password: string;
}

type Props = {
    register: UseFormRegister<SignInFormData>;
    handleSubmit: (onValid: SubmitHandler<SignInFormData>) => (e?: React.BaseSyntheticEvent) => void;
    errors: FieldErrors<SignInFormData>;
    setSuccess: React.Dispatch<React.SetStateAction<boolean>>;
    setServerErr: React.Dispatch<React.SetStateAction<string>>;
}

const SignIn = ({register, handleSubmit, errors, setSuccess, setServerErr} : Props) => {
    
    const [showPw, setShowPw] = useState(false);
    const [showPwThrottle, setShowPwThrottle] = useState(false);

    const handleShowPW = () => {
        if (showPwThrottle) return;

        setShowPwThrottle(true);
        setShowPw(prev => !prev)
        setTimeout(() => setShowPwThrottle(false), ANIMATION_DELAYS.THROTTLE);
    }

    const submit: SubmitHandler<SignInFormData> = async (data) => {
        
        const user_data = new URLSearchParams();
        user_data.append("username", data.query);
        user_data.append("password", data.password);

        try {
            const res = await axios.post(`${API_BASE_URL}/auth/token`, user_data, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            });
            logger.log(res);
            setSuccess(true);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                logger.error(error.response?.data?.detail || error.message)
                setServerErr(error.response?.data?.detail || "Login failed. Please try again.");
            } else {
                logger.error("Unknown error")
                setServerErr("Unexpected error occurred. Please contact support.");
            }
        }
    } 

    return (
        <>
            <div className="flex justify-center">
                <p className="justify-center text-[2rem] pb-8 font-bold no-select"> Welcome Back </p>
            </div>
            <form onSubmit={handleSubmit(submit)}>
                <div className="inputs grid items-center pb-8 grid-cols-1 grid-rows-3 gap-3">
                    <input 
                        autoComplete="off"
                        id="query" 
                        placeholder="Username or Email" 
                        type="text" 
                        {...register("query", { required: "Username / Email is required" })}
                        required className="inputBox username/email
                        row-start-1 row-end-2 col-start-1 col-end-2"
                    />
                    <div className="pwContainer relative flex
                    row-start-2 row-end-3 col-start-1 col-end-2">
                        <input 
                            id="pw" 
                            placeholder="Password"
                            type={`${showPw ? "text" : "password"}`}
                            {...register("password", 
                                { 
                                    required: "Password is required",
                                    minLength: {
                                        value: 8,
                                        message: "Password must be at least 8 characters"
                                    }
                                }
                            )}
                            className="inputBox password w-[100%]"
                        />
                        <button type='button' onClick={handleShowPW} className="showPw absolute right-2 top-1/2 -translate-y-1/2 text-sm text-text bg-bg-primary px-2 py-1 rounded-full cursor-pointer">
                            {showPw ?  "Hide" : "Show"}
                        </button>
                    </div>
                    <label className="remember flex items-center gap-2 cursor-pointer justify-center
                    row-start-3 row-end-3 col-start-1 col-end-2">
                        <input type="checkbox" className="rememberMe" />
                        <span className="inline no-select"> Remember Me </span>
                    </label>
                </div>
                <div className="flex justify-center w-[50%] aspect-3/1 m-auto rounded-4xl cursor-pointer
                text-text bg-bg-secondary hover:text-text-dark hover:bg-bg-secondary-dark
                transition-all transition:300ms ease-in-out">
                    <button className="enter cursor-pointer w-full text-xl" type="submit">
                        <p className="no-select"> Login </p>
                    </button>
                </div>
            </form>
            <div className="fgPw mt-8 flex items-center justify-center">
                <a className="inline-block cursor-pointer no-select"> Forgot Password? </a>
            </div>
        </>
    )
}

export default SignIn