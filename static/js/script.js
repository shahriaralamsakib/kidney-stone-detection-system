const path = document.querySelector('svg path');
const totalLength = path.getTotalLength();
path.style.setProperty('--total-length', totalLength);
