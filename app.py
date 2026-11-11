import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit Page Layout
st.set_page_config(page_title="Tower Math Defense PWA", page_icon="🏰", layout="centered")

st.title("🏰 Tower Math Defense PWA")
st.markdown("Defeat enemies in ascending arithmetic order by moving into adjacent tiles! Use **Desktop Arrow Keys** or **Mobile Touch Buttons** below.")

# Self-contained game HTML, CSS, and Canvas Game Engine
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Tower Math Defense</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        body {
            background: #090d16;
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 10px;
        }

        #game-container {
            text-align: center;
            background: linear-gradient(145deg, #1e293b, #0f172a);
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), 0 0 15px rgba(56, 189, 248, 0.1);
            max-width: 440px;
            width: 100%;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        header h1 {
            font-size: 1.4rem;
            margin-bottom: 6px;
            color: #38bdf8;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        #score-board {
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 16px;
            color: #e2e8f0;
            background: rgba(15, 23, 42, 0.6);
            padding: 8px 12px;
            border-radius: 10px;
            display: inline-block;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }

        #score-board span {
            color: #38bdf8;
        }

        canvas {
            background: #050b14;
            border: 2px solid #334155;
            border-radius: 12px;
            display: block;
            margin: 0 auto 16px auto;
            box-shadow: inset 0 4px 8px rgba(0,0,0,0.5);
        }

        #touch-controls {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
        }

        .control-row {
            display: flex;
            gap: 12px;
        }

        .ctrl-btn {
            background: linear-gradient(135deg, #38bdf8, #0284c7);
            color: #0f172a;
            border: none;
            font-size: 1.5rem;
            width: 68px;
            height: 52px;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 6px 12px rgba(2, 132, 199, 0.3);
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        .ctrl-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(56, 189, 248, 0.4);
        }

        .ctrl-btn:active {
            transform: translateY(1px);
            box-shadow: 0 2px 4px rgba(2, 132, 199, 0.2);
        }

        #game-message {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 14px;
            min-height: 24px;
            line-height: 1.3;
        }

        #restart-btn {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            border: none;
            padding: 10px 22px;
            font-size: 0.95rem;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);
            transition: all 0.2s;
        }

        #restart-btn:hover {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div id="game-container">
        <header>
            <h1>Tower Math Defense</h1>
            <div id="score-board">Power: <span id="player-power">15</span> | Level: <span id="level-num">20</span></div>
        </header>

        <main>
            <canvas id="gameCanvas" width="400" height="400"></canvas>
        </main>

        <!-- On-Screen Touch Controls -->
        <div id="touch-controls">
            <div class="control-row">
                <button class="ctrl-btn" id="btn-up">⬆️</button>
            </div>
            <div class="control-row">
                <button class="ctrl-btn" id="btn-left">⬅️</button>
                <button class="ctrl-btn" id="btn-down">⬇️</button>
                <button class="ctrl-btn" id="btn-right">➡️</button>
            </div>
        </div>

        <div id="game-message">Move into adjacent tiles. Defeat lower values first!</div>
        <button id="restart-btn" onclick="resetGame()">Restart Level</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const TILE_SIZE = 80;
        const COLS = 5;
        const ROWS = 5;

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
        let gameState = "PLAYING";

        function resetGame() {
            grid = JSON.parse(JSON.stringify(initialGrid));
            playerPos = { r: 4, c: 2 };
            playerPower = 15;
            gameState = "PLAYING";
            document.getElementById("game-message").innerText = "Move into adjacent tiles. Defeat lower values first!";
            draw();
        }

        function movePlayer(dr, dc) {
            if (gameState !== "PLAYING") return;

            let newR = playerPos.r + dr;
            let newC = playerPos.c + dc;

            // Enforce grid boundaries
            if (newR < 0 || newR >= ROWS || newC < 0 || newC >= COLS) return;

            // Enforce adjacency rule (must step to immediate neighboring tile)
            let rowDiff = Math.abs(newR - playerPos.r);
            let colDiff = Math.abs(newC - playerPos.c);
            if (rowDiff + colDiff !== 1) return;

            let target = grid[newR][newC];

            if (target.type === 'empty') {
                document.getElementById("game-message").innerText = "⚠️ You cannot step into empty cleared slots!";
                return;
            } 
            else if (target.type === 'enemy') {
                if (playerPower > target.val) {
                    playerPower += target.val;
                    grid[playerPos.r][playerPos.c] = { type: 'empty', val: 0 };
                    playerPos = { r: newR, c: newC };
                    grid[newR][newC] = { type: 'player', val: playerPower };
                    document.getElementById("game-message").innerText = "⚔️ Defeated enemy " + target.val + "! Power increased.";
                    checkWinCondition();
                } else {
                    gameState = "LOST";
                    document.getElementById("game-message").innerText = "❌ Defeat! Your power (" + playerPower + ") is too low to beat " + target.val + ".";
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

        function drawRoundedRect(ctx, x, y, width, height, radius, fillColor, strokeColor) {
            ctx.beginPath();
            ctx.roundRect(x, y, width, height, radius);
            ctx.fillStyle = fillColor;
            ctx.fill();
            if (strokeColor) {
                ctx.strokeStyle = strokeColor;
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            document.getElementById("player-power").innerText = playerPower;

            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) {
                    let cell = grid[r][c];
                    let x = c * TILE_SIZE + 6;
                    let y = r * TILE_SIZE + 6;
                    let size = TILE_SIZE - 12;

                    if (cell.type === 'player') {
                        // Polished Hero Card Style
                        drawRoundedRect(ctx, x, y, size, size, 10, '#0284c7', '#38bdf8');
                        ctx.fillStyle = '#ffffff';
                        ctx.font = 'bold 13px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.fillText("🛡️ HERO", x + size/2, y + size/2 - 8);
                        ctx.font = 'bold 16px sans-serif';
                        ctx.fillStyle = '#f0f9ff';
                        ctx.fillText(playerPower, x + size/2, y + size/2 + 14);
                    } 
                    else if (cell.type === 'enemy') {
                        // Dynamic color-coding: green if beatable, red if deadly
                        let isBeatable = cell.val < playerPower;
                        let bgColor = isBeatable ? '#15803d' : '#b91c1c';
                        let borderColor = isBeatable ? '#4ade80' : '#f87171';
                        
                        drawRoundedRect(ctx, x, y, size, size, 10, bgColor, borderColor);
                        
                        ctx.fillStyle = '#ffffff';
                        ctx.font = 'bold 18px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.fillText(cell.val, x + size/2, y + size/2 + 6);
                    } 
                    else {
                        // Empty cleared slot
                        drawRoundedRect(ctx, x, y, size, size, 10, '#1e293b', '#334155');
                    }
                }
            }
        }

        // Keyboard Event Listeners
        window.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowUp': case 'w': movePlayer(-1, 0); break;
                case 'ArrowDown': case 's': movePlayer(1, 0); break;
                case 'ArrowLeft': case 'a': movePlayer(0, -1); break;
                case 'ArrowRight': case 'd': movePlayer(0, 1); break;
            }
        });

        // Touch Control Listeners
        document.getElementById('btn-up').addEventListener('click', () => movePlayer(-1, 0));
        document.getElementById('btn-down').addEventListener('click', () => movePlayer(1, 0));
        document.getElementById('btn-left').addEventListener('click', () => movePlayer(0, -1));
        document.getElementById('btn-right').addEventListener('click', () => movePlayer(0, 1));

        // Initial render
        draw();
    </script>
</body>
</html>
"""

# Render game inside Streamlit component
components.html(game_html, height=760, scrolling=False)
