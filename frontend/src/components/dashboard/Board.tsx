import { useEffect, useRef, useState, type JSX } from 'react'
import { useGSAP } from '@gsap/react'
import gsap from 'gsap'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'
import Overview from './Overview';
import IncomeSlide from './IncomeSlide';
import TransactionSlide from './TransactionSlide';
import PlanningSlide from './PlanningSlide';
import GoalSlide from './GoalSlide';
import NavBar from '../NavBar';
import { logger } from '../../utils/logger';

gsap.registerPlugin(ScrollToPlugin);

const Board = () => {
    const container = useRef<HTMLDivElement>(null);
    const slideRefs = useRef<(HTMLElement | null)[]>([]);
    const [ currentSlide, setCurrentSlide ] = useState(0);

    const currentSlideRef = useRef(currentSlide);
    const tweenRef = useRef<gsap.core.Tween | null>(null);

    const slides = [
        { id: 'dashboard', className: "slide 0", html: Overview},
        { id: 'income', className: 'slide 1', html: IncomeSlide},
        { id: 'transaction', className: 'slide 2', html: TransactionSlide},
        { id: 'planning', className: 'slide 3', html: PlanningSlide},
        { id: 'goal', className: 'slide 4', html: GoalSlide}
    ];

    const goToSlide = (idx: number) => {
        if (tweenRef.current) {
            tweenRef.current.kill();
        }

        if ( gsap.isTweening(window) ) return;

        const currSlide= slideRefs.current[currentSlideRef.current];
        const tgt = slideRefs.current[idx];
        if ( tgt ) {
            const tl = gsap.timeline({
                onComplete: () => {
                    setCurrentSlide(idx);
                    tweenRef.current = null;
                    console.log("animation done.")
                }
            });
            tl.to(currSlide, {
                opacity: 0,
                duration: 0.5,
                ease: "power2.inOut"
            }, 0);
            tl.to(window, {
                scrollTo: {
                    y: tgt.offsetTop,
                    autoKill: false
                },
                duration: 1,
                ease: "power2.inOut",
            }, 0)
            tl.fromTo(tgt, {
                opacity: 0
            }, {
                opacity: 1,
                duration: 0.5,
                ease: "power2.inOut",
            }, 0);
        }
    }

    useEffect(() => {
        goToSlide(0)
    }, []);

    useEffect(() => {
        currentSlideRef.current = currentSlide;
        logger.log(currentSlideRef.current)
    }, [currentSlide])

    useGSAP(() => {
        const handleScroll = (e: WheelEvent) => {
            e.preventDefault()
            const dir = e.deltaY;
            const current = currentSlideRef.current;

            if ( dir > 0 && current < slideRefs.current.length - 1 ) {
                goToSlide( current + 1 )
            } else if ( dir < 0 && current > 0 ) {
                goToSlide( current - 1 )
            }
        }

        const handleUpDown = (e: KeyboardEvent) => {
            const dir = e.key
            if (dir !== "ArrowUp" && dir !=="ArrowDown") return;
            e.preventDefault()
            const current = currentSlideRef.current;

            if ( dir == "ArrowDown" && current < slideRefs.current.length - 1 ) {
                goToSlide( current + 1 )
            } else if ( current > 0 ) {
                goToSlide( current - 1 )
            }
        }

        const ignoreUpDown = (e: KeyboardEvent) => {
            if (e.key === "ArrowDown" || e.key === "ArrowUp") {
                e.preventDefault()
            }
        }

        window.addEventListener("wheel", handleScroll, { passive: false });
        window.addEventListener("keydown", ignoreUpDown, { passive: false })
        window.addEventListener("keyup", handleUpDown, { passive: false });
        window.addEventListener("mousedown", e => {if (e.button == 1) e.preventDefault()});
    
        console.log('Setting up animations...');

        // cleanup 
        return () => {
            window.removeEventListener("wheel", handleScroll)
            window.removeEventListener("mousedown", e => {if (e.button == 1) e.preventDefault()})
            if (tweenRef.current) {
                tweenRef.current.kill();
            }
            console.log('Cleaning up...');
        }
    });

    return (
        <>
            <NavBar slides= {slides} currentSlide= {currentSlide} goTo={goToSlide} />
            <div className="bg-[#f2f2f2] slide-container no-scrollbar" ref={container}>
                {slides.map((slide, idx) => (
                    <section key={slide.id} className={slide.className} ref={(el) => {slideRefs.current[idx] = el}}>
                        <slide.html />
                    </section>
                ))}
            </div>
        </>
    )
}

export default Board