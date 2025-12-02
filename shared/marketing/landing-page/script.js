document.addEventListener('DOMContentLoaded', () => {
    const bgImage = document.querySelector('.bg-image');
    
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 15;
        const y = (e.clientY / window.innerHeight - 0.5) * 15;
        
        if (bgImage) {
            bgImage.style.transform = `scale(1.1) translate(${x}px, ${y}px)`;
        }
    });
});
