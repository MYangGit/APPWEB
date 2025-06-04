export default {
    mounted(el, binding) {
        let isDragging = false;
        let offsetX = 0;
        let offsetY = 0;

        const handleMouseDown = (e) => {
            e.preventDefault();
            e.stopPropagation();
            isDragging = true;
            const rect = el.getBoundingClientRect();
            offsetX = e.pageX - rect.left;
            offsetY = e.pageY - rect.top;
            el.style.zIndex = 10;
        };

        const handleMouseMove = (e) => {
            if (!isDragging) return;
            e.preventDefault();
            e.stopPropagation();
            const containerRect = el.closest('.drag-container').getBoundingClientRect();
            let newX = e.pageX - offsetX - containerRect.left;
            let newY = e.pageY - offsetY - containerRect.top;
            newX = Math.max(0, Math.min(newX, containerRect.width - el.offsetWidth));
            newY = Math.max(0, Math.min(newY, containerRect.height - el.offsetHeight));
            el.style.transform = `translate(${newX}px, ${newY}px)`;
        };

        const handleMouseUp = (e) => {
            e.preventDefault();
            e.stopPropagation();
            isDragging = false;
            el.style.zIndex = 1;
            if (binding.value && typeof binding.value.onDragEnd === 'function') {
               const rect = el.getBoundingClientRect();
               binding.value.onDragEnd(rect.left, rect.top);
            }
        };

        el.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        return {
            onUnmounted: () => {
                el.removeEventListener('mousedown', handleMouseDown);
                document.removeEventListener('mousemove', handleMouseMove);
                document.removeEventListener('mouseup', handleMouseUp);
            }
        }
    }
};