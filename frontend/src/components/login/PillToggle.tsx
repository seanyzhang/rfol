import { useEffect, useRef } from 'react'

type Props = {
  hasAccount: boolean;
  onToggle: (val: boolean) => void;
};
  
const PillToggle = ({ hasAccount, onToggle }: Props) => {
  const pill1 = useRef<HTMLButtonElement>(null);
  const pill2 = useRef<HTMLButtonElement>(null);
  const highlight = useRef<HTMLDivElement>(null);

  const shiftHighlight = (val: boolean) => {
    const pillActive = val ? pill2.current : pill1.current;
    const pillInactive = val ? pill1.current : pill2.current;
    const highlighter = highlight.current;

    if (pillActive && pillInactive && highlighter) {
      const { offsetLeft, offsetWidth } = pillActive;
      highlighter.style.transform = `translateX(${offsetLeft}px)`;
      highlighter.style.width = `${offsetWidth}px`;
      pillActive.style.color = "var(--color-text-dark)";
      pillInactive.style.color = "var(--color-text)";
    }
  };

  useEffect(() => {
    shiftHighlight(hasAccount);
  }, [hasAccount]);

  return (
    <div className="signup-signin relative flex justify-evenly">
      <button
        ref={pill1}
        onClick={() => onToggle(false)}
        className="signup-signin-button no-select text-2xl z-10 transition-colors duration-300"
      >
        Sign Up
      </button>
      <button
        ref={pill2}
        onClick={() => onToggle(true)}
        className="signup-signin-button no-select text-2xl z-10 transition-colors duration-300"
      >
        Sign In
      </button>
      <span
        ref={highlight}
        className="absolute top-0 left-0 h-full p-4.5 bg-bg-accent rounded-full transition-all duration-500 ease-in-out"
        style={{ width: "50%" }}
      ></span>
    </div>
  );
}

export default PillToggle