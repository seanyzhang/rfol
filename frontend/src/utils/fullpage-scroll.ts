import { SCROLL_CONFIG } from "../constants";
import { logger } from "./logger";

const fullPageScrolling = () => {

  logger.log("Initialized FullPage Scrolling")
  // query selectors
  const sections: NodeListOf<HTMLElement> = document.querySelectorAll("section")
  let activeSection: HTMLElement;

  // set active section

  const setActiveSection = (entry: IntersectionObserverEntry) => { activeSection = entry.target as HTMLElement; }

  const activeSectionHandler = (currentSectionID: string) => {
    sections.forEach(section => {
      if (section.dataset.id === currentSectionID) {
        section.classList.add('active');
      } else {
        section.classList.remove('active');
      }
    });
  };

  // helper functions

  const showPreviousSection = () => {
    if (!activeSection) { return; }
    const curr: number = Array.from(sections).indexOf(activeSection);
    if (curr > 0) {sections[curr-1].scrollIntoView()};
  }

  const showNextSection = () => {
    if (!activeSection) { return; }
    const curr: number = Array.from(sections).indexOf(activeSection);
    if (curr < sections.length - 1) {sections[curr+1].scrollIntoView()};
  }

  // sectionWatcher

  const sectionWatcherCallback = (
    entries: IntersectionObserverEntry[],
    observer: IntersectionObserver
  ) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      activeSectionHandler(entry.target.id);
      setActiveSection(entry)
    });
  };
  const sectionWatcherOptions = {
    threshold: SCROLL_CONFIG.INTERSECTION_THRESHOLD
  }

  const sectionWatcher = new IntersectionObserver(sectionWatcherCallback, sectionWatcherOptions)

  sections.forEach(section => {
    sectionWatcher.observe(section)
  })

  // event handler

  const keyEventHandler = (keyEvent: string) => {
    if (keyEvent === "ArrowUp") {
      showPreviousSection()
    }
    else {
      showNextSection();
    }
  }
  

  const wheelEventHandler = (deltaY: number) => {
    if (deltaY > 0) {
      showNextSection();
    } else if (deltaY < 0) {
      showPreviousSection();
    }
  }

  // event listeners

  const keydownHandler = (event: KeyboardEvent) => {
    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
      event.preventDefault();
      keyEventHandler(event.key);
    }
  }
  
  const wheelHandler = (event: WheelEvent) => {
    if (event.deltaY !== 0){
      event.preventDefault();
      wheelEventHandler(event.deltaY);
    }
  }

  window.addEventListener('wheel', wheelHandler, { passive: false })
  window.addEventListener('keydown', keydownHandler, { passive: false });

  const carousel = document.querySelector<HTMLDivElement>(".slider")
  if (carousel) {
    carousel.addEventListener('mouseenter', (event:MouseEvent) =>{
    window.removeEventListener('wheel', wheelHandler,)
  })

  carousel.addEventListener('mouseleave', (event:MouseEvent) =>{
    window.addEventListener('wheel', wheelHandler, {passive: false})
  })
  } else {
    console.warn("carousel not found")
  }
}

export default fullPageScrolling