// Based on https://codepen.io/abjt14/pen/zYaBExZ

import React, { useEffect, useRef, useState } from 'react'
import "./DashPillbar.css"

type Props = {
    setAccountType: React.Dispatch<React.SetStateAction<string>>
}

const pillBarData: string[] = [
    "Assets",
    "Liabilities",
    "Both"
]

const DashPillbar = ({setAccountType} : Props) => {
    const pillRef = useRef<HTMLDivElement>(null)
    const menuLinks = useRef<(HTMLDivElement | null)[]>([])
    const itemsRef = useRef<HTMLDivElement>(null)
    const [selected, setSelected] = useState(0)

    const setPill = (idx: number) => {
        if (!pillRef.current || !menuLinks.current || !itemsRef.current) return;

        menuLinks.current.forEach((el, i) => {
            if (!el) return;

            if (i === idx) {
                const dimensions = el.getBoundingClientRect();
                const itemsRect = itemsRef.current!.getBoundingClientRect();

                pillRef.current!.style.width = dimensions.width + 'px';
                pillRef.current!.style.height = dimensions.height + 'px';
                pillRef.current!.style.left = (dimensions.left - itemsRect.left) + 'px';
        
                el.classList.add('active');
                setAccountType(el.id)
            } else {
                el.classList.remove('active');
            }
        });
    };

    useEffect(() => {
        const eventHandlers: ((e: Event) => void)[] = [];
        
        menuLinks.current.forEach((el, idx) => {
            if (!el) return;
            
            const handler = (e: Event) => {
                setSelected(idx);
                setPill(idx); 
            };
            
            eventHandlers[idx] = handler;
            el.addEventListener('click', handler);
        });

        // Initial setup
        setPill(0);
        
        return () => {
            menuLinks.current.forEach((element, index) => {
                if (element && eventHandlers[index]) {
                    element.removeEventListener('click', eventHandlers[index]);
                }
            });
        }
    }, []);

    useEffect(() => {
        setPill(selected);
    }, [selected]);

    useEffect(() => {
        const handleResize = () => setPill(selected)
        
        if (itemsRef.current) {
            const resizeObserver = new ResizeObserver(handleResize)
            resizeObserver.observe(itemsRef.current)
            
            return () => resizeObserver.disconnect()
        }
    }, [selected])

    return (
        <div id="menu" className="flex justify-center">
            <div className="content relative flex m-auto">
                <div id="pill" className="absolute top-1/2 -translate-y-1/2 left-0 bg-gray-600 rounded-md transition-[left,width] duration-500 ease-in-out" ref={pillRef}></div>
                <div id="items" className="flex justify-evenly bg-[#F2F2F2] rounded-lg ring-1 ring-fuchsia-200" ref={itemsRef}>
                    {pillBarData.map((pill, idx) => (
                        <div key={pill} id={pill} className={`item px-4 py-1 rounded-lg cursor-pointer z-10 transition-all duration-1000 ease-in-out`} ref={(el) => {menuLinks.current[idx] = el}}>
                            {pill}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default DashPillbar