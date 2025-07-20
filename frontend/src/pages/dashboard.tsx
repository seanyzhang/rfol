import PageWrapper from "../components/PageWrapper"
import { useEffect } from "react"
import { useUser } from "../UserContext";
import { useNavigate } from "react-router-dom";
import LoadingIcon from "../components/LoadingIcon";
  
const Dashboard = ({ isExiting }: { isExiting: boolean }) => {
    const {currentUser, loading} = useUser()
    const navigate = useNavigate()

    if (loading) {
        <PageWrapper isExiting={isExiting}>
            <section className="main">
                <div className="w-full h-full flex justify-center items-center">
                    <LoadingIcon></LoadingIcon>
                </div>
            </section>
        </PageWrapper>
    }

    useEffect(() => {
        if (!currentUser) {
            navigate("/login")
        }
    }, [currentUser])

    return (
        <PageWrapper isExiting={isExiting}>
            <section className="main">
                <div className="w-full h-full flex justify-center items-center">
                    {currentUser ? (
                        <p>Hello {currentUser.first_name}</p>
                    ) : (
                        <p>Redirecting back to login...</p>
                    )}
                </div>
            </section>
        </PageWrapper>
    )
}

export default Dashboard