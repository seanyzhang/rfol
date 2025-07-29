import React, { useState } from 'react'
import DashPillbar from './DashPillbar';
import "./dashboard.css"

interface UserData {
    institution: string,
    currentBalance: number,
    type: string
}

const userAccounts: UserData[] = [
    {institution: "Bank of America", currentBalance: 3000, type: "Assets"},
    {institution: "Chase", currentBalance: 3000, type: "Assets"},
    {institution: "Bank of America", currentBalance: 3000, type: "Liabilities"},
    {institution: "Robinhood", currentBalance: 3000, type: "Assets"}
]

const assetAccounts =  userAccounts.filter(item => item.type === "Assets");
const liabilityAccounts = userAccounts.filter(item => item.type === "Liabilities");

const Overview = () => {
    const [accountType, setAccountType] = useState("Assets") 

    return (
        <>  
            <div className="page pt-[3vh] pr-[3vw] pb-[4vh] pl-[3vw] grid grid-rows-8 grid-cols-4 gap-4">
                <div className="sec accounts flex-col h-full rounded-2xl
                row-start-1 col-start-1 row-end-7 col-end-2">
                    <div className="accountsTitle flex mb-3">
                        <p className="text-2xl">Accounts: {accountType}</p>
                    </div>
                    <div className="pillBar">
                        <DashPillbar setAccountType={setAccountType} />
                    </div>
                    <div className="select">
                        {(() => {
                            let accounts: UserData[];
                            let displayType;
                            
                            switch(accountType) {
                                case "Assets":
                                    accounts = assetAccounts;
                                    displayType = "Assets";
                                    break;
                                case "Liabilities":
                                    accounts = liabilityAccounts;
                                    displayType = "Liabilities";
                                    break;
                                case "Both":
                                    accounts = userAccounts;
                                    displayType = "Both";
                                    break;
                                default:
                                    accounts = [];
                                    displayType = "unknown";
                            }
                            
                            return accounts.map((item, idx) => (
                                <section key={idx} className={`${accountType} account ${item.institution} grid grid-cols-[2fr_2fr_1fr] gap-4`}>
                                    <p className="flex col-span-1"> {item.institution} </p>
                                    <p className="flex col-span-1"> GRAPH </p>
                                    <p className="flex col-span-1"> {item.currentBalance} </p>
                                </section>
                            ));
                        })()}
                    </div>
                </div>
                <div className="sec nextPaycheck flex-col justify-center items-center h-full rounded-2xl
                row-start-7 col-start-1 row-end-10 col-end-2">
                    <div className="nextPaycheckTitle">
                        <p className="text-2xl">Income</p>
                    </div>
                    
                </div>
                <div className="sec summary networth justify-center items-center h-full grid grid-cols-[3fr_2fr] grid-rows-[2rem_auto] gap-4 rounded-2xl
                row-start-1 col-start-2 row-end-6 col-end-4">
                    <div className="summaryTitle row-start-1 row-end-1 col-start-1 col-end-1">
                        <p className="text-2xl">Account summary</p>
                    </div>
                    <div className="summaryGraph row-start-2 row-end-2 col-start-1 col-end-1 flex justify-center">
                        <div className="graph">
                            <p> Graph </p>
                        </div>
                    </div>
                    <div className="summaryDetails row-start-1 row-end-3 col-start-2 col-end-2 flex justify-center">
                        <div className="details">
                            <p> Balance: </p>
                            <p> Lorem ipsum dolor sit amet consectetur adipisicing elit. Ratione soluta laborum ipsam at eveniet unde perspiciatis eos amet quos magni. Provident exercitationem architecto deleniti aperiam veniam earum quibusdam, autem temporibus. </p>
                        </div>
                    </div>
                </div>
                <div className="sec budgetTracker flex-col justify-center items-center h-full rounded-2xl
                row-start-6 col-start-2 row-end-10 col-end-3">
                    <div className="budgetTitle">
                        <p className="text-2xl">Monthly Budget</p>
                    </div>
                </div>
                <div className="sec recentTransactions flex-col justify-center items-center h-full rounded-2xl
                row-start-6 col-start-3 row-end-10 col-end-4">
                    <div className="transactionTitle">
                        <p className="text-2xl">Recent Transactions</p>
                    </div> 
                </div>
                <div className="sec goalsVisual flex-col justify-center items-center h-full rounded-2xl
                row-start-1 col-start-4 row-end-5 col-end-5">
                    <div className="goalsTitle">
                        <p className="text-2xl">Goals Progress</p>
                    </div>
                </div>
                <div className="sec recommendations flex-col justify-center items-center h-full rounded-2xl
                row-start-5 col-start-4 row-end-10 col-end-5">
                    <div className="recommendationTitle">
                        <p className="text-2xl">Recommendations</p>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Overview