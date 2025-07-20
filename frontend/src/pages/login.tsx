import { useEffect, useState } from "react"
import PageWrapper from "../components/PageWrapper"
import "./login.css"
import { ANIMATION_DELAYS } from "../constants"
import PillToggle from "../components/login/PillToggle"
import SignUp from "../components/login/SignUp"
import SignIn from "../components/login/SignIn"
import { Link, useNavigate } from "react-router-dom"
import { useForm } from "react-hook-form"
import { useUser } from "../UserContext"

type SignInFormData = {
    query: string;
    password: string;
}

type SignUpFormData = {
    firstname: string;
    lastname: string;
    username: string;
    email: string;
    password: string;
}

const Login = ({ isExiting }: { isExiting: boolean }) => {
    /* Authentication */ 
    const [serverErr, setServerErr] = useState("");
    const [hasAccount, setHasAccount] = useState(false);
    const { currentUser } = useUser();
    const navigate = useNavigate(); 

    const {
        register: registerSignIn, 
        handleSubmit: handleSubmitSignIn, 
        formState: {errors: errorsSignIn},
        reset: resetSignIn,
    } = useForm<SignInFormData>();

    const {
        register: registerSignUp, 
        handleSubmit: handleSubmitSignUp,
        formState: {errors: errorsSignUp},
        reset: resetSignUp
    } = useForm<SignUpFormData>();


    /* Sign Up and Sign In Pill Effects*/
    const [throttling, setThrottling] = useState(false);

    useEffect(() => {
        if (hasAccount) {
          resetSignIn();
        } else {
          resetSignUp();
        }
      }, [hasAccount]);

    useEffect(() => {
        if (currentUser) {
            navigate("/")
        }
    }, [currentUser])

    return (
        <PageWrapper isExiting={isExiting}>
            <section className="main flex justify-center">            
                {(serverErr || Object.keys(hasAccount ? errorsSignIn : errorsSignUp).length > 0) && (
                    <div className="errmsgcontainer flex translate-y-8 bg-red-200 mt-auto rounded-3xl items-center w-fit px-4 py-2 text-sm text-text transition-all" style={{ transitionProperty: 'transform', transitionDuration: '300ms' }}>
                        <ul className="list-disc list-inside space-y-1">
                        {serverErr && <li> {serverErr} </li>}
                        {Object.entries(hasAccount ? errorsSignIn : errorsSignUp).map(([key, val]) => (
                            <li key={key}>
                                {typeof val === "object" && "message" in val
                                ? val.message
                                : String(val)}
                            </li>
                            ))
                        }
                        </ul>
                    </div>
                    )
                }
                {
                    currentUser ? 
                    (<div>
                        <p> You are logged in! </p>
                        <Link to="/"> Click here to continue </Link>
                    </div>) :
                    (<div className="container no-scrollbar flex-col absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 items-center justify-center gap-5">
                        <PillToggle hasAccount={hasAccount} onToggle={(val) => {
                            if (!throttling && val !== hasAccount) {
                                setThrottling(true);
                                setHasAccount(val);
                                setTimeout(() => setThrottling(false), ANIMATION_DELAYS.THROTTLE);
                            }
                          }}
                        />
                        <div className="card-3d-wrap w-[50vw] max-w-[28rem] aspect-square">
                            <div className={`card-3d-wrapper ${hasAccount ? "flipped" : ""}`}>
                                <div className="card-front bg-bg-accent text-text-dark rounded-2xl flex-col justify-center p-8">
                                    <SignUp 
                                        register = {registerSignUp}
                                        handleSubmit = {handleSubmitSignUp}
                                        errors = {errorsSignUp}
                                        setHasAccount = {setHasAccount}
                                        setServerErr = {setServerErr}
                                    />
                                </div>
                                <div className="card-back bg-bg-accent text-text-dark rounded-2xl flex-col justify-center p-8">
                                    <SignIn 
                                        register = {registerSignIn}
                                        handleSubmit = {handleSubmitSignIn}
                                        errors = {errorsSignIn}
                                        setServerErr = {setServerErr}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>)
                }
            </section>
        </PageWrapper>
    )
}

export default Login