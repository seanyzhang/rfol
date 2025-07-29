import { type JSX } from 'react'

interface SlideData {
    id: string,
    className: string,
    html: () => JSX.Element
}

interface NavBarProps {
    slides: SlideData[],
    currentSlide: number,
    goTo: (index: number) => void
}

const NavBar = ({ slides, currentSlide, goTo } : NavBarProps) => {
    return (
        <nav className="navbar fixed p-4 left-1/2 -translate-x-1/2 z-10 overflow-hidden">
            <ul className="w-4/10 flex justify-evenly">
                {slides.map((slide, idx) => (
                    <li key={slide.id}>
                        <button className={`${currentSlide === idx ? 'active' : ''} px-6 py-4 hover:cursor-pointer`} onClick={() => goTo(idx)}>
                            {slide.id}
                        </button>
                    </li>
                ))}
            </ul>
        </nav>
    )
}

export default NavBar