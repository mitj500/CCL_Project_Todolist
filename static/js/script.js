// Get the drawing area canvas element
const drawingArea = document.getElementById('drawingArea');
const ctx = drawingArea.getContext('2d');

// Set initial variables for drawing
let isDrawing = false;
let previousX = 0;
let previousY = 0;

// Function to start drawing
function startDrawing(event) {
  isDrawing = true;
  previousX = event.clientX - drawingArea.offsetLeft;
  previousY = event.clientY - drawingArea.offsetTop;
}

// Function to draw while mouse is moving
function draw(event) {
  if (isDrawing) {
    const currentX = event.clientX - drawingArea.offsetLeft;
    const currentY = event.clientY - drawingArea.offsetTop;

    ctx.beginPath();
    ctx.moveTo(previousX, previousY);
    ctx.lineTo(currentX, currentY);
    ctx.strokeStyle = '#000'; // Black color
    ctx.lineWidth = 2;
    ctx.stroke();

    previousX = currentX;
    previousY = currentY;
  }
}

// Function to stop drawing
function stopDrawing() {
  isDrawing = false;
}

// Function to reset the drawing
function resetDrawing() {
  ctx.clearRect(0, 0, drawingArea.width, drawingArea.height);
}

// Event listeners for drawing functionality
drawingArea.addEventListener('mousedown', startDrawing);
drawingArea.addEventListener('mousemove', draw);
drawingArea.addEventListener('mouseup', stopDrawing);
drawingArea.addEventListener('mouseleave', stopDrawing);

// Event listener for reset button
const resetButton = document.getElementById('resetButton');
resetButton.addEventListener('click', resetDrawing);

