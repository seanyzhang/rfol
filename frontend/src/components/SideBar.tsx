import { useEffect, useState } from "react";
import "./SideBar.css"
import { ANIMATION_DELAYS, ICON_MAP } from "../constants";

const items = ["Dropdown", "Dashboard", "Income", "Transactions", "Planning", "Goals"];

type Props = {
  navTo: (address: string) => void;
}

const SideBarItem = ({ label, onClick, children }: { label: string, onClick: () => void, children: React.ReactNode }) => (
    <li className="list-item relative group" onClick={onClick}>
        <div className="list-icon hover:cursor-pointer">
            { children }
        </div>
        <div className="list-text absolute ml-3 left-full m-auto color-accent invisible opacity-0 group-hover:visible group-hover:opacity-100">
            <p className="text-[1.5rem] p-0.5"> { label } </p>
        </div>
    </li>
)

const SideBar = ({navTo} : Props) => {
    const [focused, setFocused] = useState(false);
    
    return (
        <div className="sidebar fixed flex flex-col top-1/2 -translate-y-1/2 height-[100vh] gap-6">
            <ul className="">
                <SideBarItem label="" onClick={() => setFocused(prev => !prev)}>
                    {ICON_MAP["Dropdown"]}
                </SideBarItem>
            </ul>
            <ul className={`list flex flex-col gap-6 transition-all duration-500 ease-in-out ${
                focused ? "opacity-100 max-h-[500px]" : "opacity-0 max-h-0 overflow-hidden"
                }`}>
                {items.slice(1).map(label => (
                    <SideBarItem key={label} label={label} onClick={() => navTo(label.toLowerCase())}>
                    {ICON_MAP[label]}
                    </SideBarItem>
                ))}
            </ul>
        </div>
    )
}

export default SideBar