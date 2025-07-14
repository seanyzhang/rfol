import PageWrapper from "../components/PageWrapper"

const Dashboard = ({ isExiting }: { isExiting: boolean }) => {
    return (
    <PageWrapper isExiting={isExiting}>
        <section className="main">
            <div>
                <p> Hello World </p>
            </div>
        </section>
    </PageWrapper>)
}

export default Dashboard