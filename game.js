const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const TILE_SIZE = 80;
const COLS = 5;
const ROWS = 5;

// Level 20 layout setup: grid mapping types ('player', 'enemy', 'empty') and numeric values
let initialGrid = [
    [{type: 'enemy', val: 125}, {type: 'enemy', val: 207}, {type: 'enemy', val: 499}, {type: 'enemy', val: 310}, {type: 'enemy', val: 180}],
    [{type: 'enemy', val: 85},  {type: 'empty', val: 0},   {type: 'enemy', val: 150}, {type: 'empty', val: 0},   {type: 'enemy', val: 95}],
    [{type: 'enemy', val: 45},  {type: 'enemy', val: 60},  {type: 'empty', val: 0},   {type: 'enemy', val: 110}, {type: 'enemy', val: 70}],
    [{type: 'empty', val: 0},   {type: 'enemy', val: 30},  {type: 'enemy', val: 40},  {type: 'enemy', val: 55},  {type: 'empty', val: 0}],
    [{type: 'enemy', val: 20},  {type: 'enemy', val: 25},  {type: 'player', val: 15},{type: 'enemy', val: 35},  {type: 'enemy', val: 49}]
];

let grid = JSON.parse(JSON.stringify(initialGrid));
let playerPos = { r: 4, c: 2 };
let playerPower = 15;
let gameState = "PLAYING"; // PLAYING, WON, LOST

function resetGame() {
    grid = JSON.parse(JSON.stringify(initialGrid));
    playerPos = { r: 4, c: 2 };
    playerPower = 15;
    gameState = "PLAYING";
    document.getElementById("game-message").innerText = "Use Arrow Keys or Touch Controls. Defeat lower values first!";
    draw();
}

function movePlayer(dr, dc) {
    if (gameState !== "PLAYING") return;

    let newR = playerPos.r + dr;
    let newC = playerPos.c + dc;

    // Check bounds
    if (newR < 0 || newR >= ROWS || newC < 0 || newC >= COLS) return;

    let target = grid[newR][newC];

    if (target.type === 'empty') {
        // Move freely into empty slots
        grid[playerPos.r][playerPos.c] = { type: 'empty', val: 0 };
        playerPos = { r: newR, c: newC };
        grid[newR][newC] = { type: 'player', val: playerPower };
    } 
    else if (target.type === 'enemy') {
        // Arithmetic Progression Combat Rule
        if (playerPower > target.val) {
            playerPower += target.val;
            grid[playerPos.r][playerPos.c] = { type: 'empty', val: 0 };
            playerPos = { r: newR, c: newC };
            grid[newR][newC] = { type: 'player', val: playerPower };
            checkWinCondition();
        } else {
            gameState = "LOST";
            document.getElementById("game-message").innerText = "❌ Defeat! Your power is too low to beat " + target.val + ".";
        }
    }
    draw();
}

function checkWinCondition() {
    let enemiesLeft = 0;
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            if (grid[r][c].type === 'enemy') enemiesLeft++;
        }
    }
    if (enemiesLeft === 0) {
        gameState = "WON";
        document.getElementById("game-message").innerText = "🎉 Victory! Level Cleared Successfully!";
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById("player-power").innerText = playerPower;

    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            let cell = grid[r][c];
            let x = c * TILE_SIZE;
            let y = r * TILE_SIZE;

            // Tile background coloring
            if (cell.type === 'player') {
                ctx.fillStyle = '#0284c7';
            } else if (cell.type === 'enemy') {
                ctx.fillStyle = cell.val <= playerPower ? '#16a34a' : '#dc2626'; // Green if beatable, red if deadly
            } else {
                ctx.fillStyle = '#1e293b';
            }

            ctx.fillRect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8);
            ctx.strokeStyle = '#475569';
            ctx.strokeRect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8);

            // Render numbers and labels
            if (cell.type === 'player') {
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 16px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText("HERO", x + TILE_SIZE/2, y + TILE_SIZE/2 - 8);
                ctx.fillText(playerPower, x + TILE_SIZE/2, y + TILE_SIZE/2 + 14);
            } else if (cell.type === 'enemy') {
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 18px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(cell.val, x + TILE_SIZE/2, y + TILE_SIZE/2 + 6);
            }
        }
    }
}

// Event Listeners for Desktop Arrow Keys
window.addEventListener('keydown', (e) => {
    switch (e.key) {
        case 'ArrowUp': case 'w': movePlayer(-1, 0); break;
        case 'ArrowDown': case 's': movePlayer(1, 0); break;
        case 'ArrowLeft': case 'a': movePlayer(0, -1); break;
        case 'ArrowRight': case 'd': movePlayer(0, 1); break;
    }
});

// Event Listeners for Mobile On-Screen Buttons
document.getElementById('btn-up').addEventListener('click', () => movePlayer(-1, 0));
document.getElementById('btn-down').addEventListener('click', () => movePlayer(1, 0));
document.getElementById('btn-left').addEventListener('click', () => movePlayer(0, -1));
document.getElementById('btn-right').addEventListener('click', () => movePlayer(0, 1));

// Initial Render
draw();
