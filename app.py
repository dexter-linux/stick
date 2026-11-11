import streamlit as st
import streamlit.components.v1 as components

# Configure page layout
st.set_page_config(page_title="Tower Math Defense PWA", page_icon="🏰", layout="centered")

st.title("🏰 Tower Math Defense PWA")
st.markdown("Defeat enemies in ascending arithmetic order! Play using **Desktop Arrow Keys** or **Mobile Touch Buttons** below.")

# Self-contained game HTML/CSS/JS string
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Tower Math Defense PWA</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: #0f172a;
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding: 10px;
        }

        #game-container {
            text-align: center;
            background: #1e293b;
            padding: 16px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            max-width: 440px;
            width: 100%;
            margin: 0 auto;
        }

        header h1 {
            font-size: 1.25rem;
            margin-bottom: 4px;
            color: #38bdf8;
        }

        #score-board {
            font-size: 1rem;
            font-weight: bold;
            margin-bottom: 12px;
            color: #cbd5e1;
        }

        canvas {
            background: #090d16;
            border: 3px solid #334155;
            border-radius: 8px;
            display: block;
            margin: 0 auto 12px auto;
            max-width: 100%;
            height: auto;
        }

        #touch-controls {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            margin-bottom: 12px;
        }

        .control-row {
            display: flex;
            gap: 12px;
        }

        .ctrl-btn {
            background: #38bdf8;
            color: #0f172a;
            border: none;
            font-size: 1.4rem;
            width: 60px;
            height: 48px;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: background 0.2s;
        }

        .ctrl-btn:active {
            background: #0284c7;
            transform: scale(0.95);
        }

        #game-message {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-bottom: 10px;
        }

        #restart-btn {
            background: #ef4444;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 0.9rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s;
        }

        #restart-btn:hover {
            background: #dc2626;
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
            <canvas id="gameCanvas" width="400" height="450"></canvas>
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

        <div id="game-message">Use Arrow Keys or On-Screen Controls. Defeat lower values first!</div>
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
            document.getElementById("game-message").innerText = "Use Arrow Keys or Touch Controls. Defeat lower values first!";
            draw();
        }

        function movePlayer(dr, dc) {
            if (gameState !== "PLAYING") return;

            let newR = playerPos.r + dr;
            let newC = playerPos.c + dc;

            if (newR < 0 || newR >= ROWS || newC < 0 || newC >= COLS) return;

            let target = grid[newR][newC];

            if (target.type === 'empty') {
                grid[playerPos.r][playerPos.c] = { type: 'empty', val: 0 };
                playerPos = { r: newR, c: newC };
                grid[newR][newC] = { type: 'player', val: playerPower };
            } 
            else if (target.type === 'enemy') {
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

                    if (cell.type === 'player') {
                        ctx.fillStyle = '#0284c7';
                    } else if (cell.type === 'enemy') {
                        ctx.fillStyle = cell.val <= playerPower ? '#16a34a' : '#dc2626';
                    } else {
                        ctx.fillStyle = '#1e293b';
                    }

                    ctx.fillRect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8);
                    ctx.strokeStyle = '#475569';
                    ctx.strokeRect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8);

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

        window.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowUp': case 'w': movePlayer(-1, 0); break;
                case 'ArrowDown': case 's': movePlayer(1, 0); break;
                case 'ArrowLeft': case 'a': movePlayer(0, -1); break;
                case 'ArrowRight': case 'd': movePlayer(0, 1); break;
            }
        });

        document.getElementById('btn-up').addEventListener('click', () => movePlayer(-1, 0));
        document.getElementById('btn-down').addEventListener('click', () => movePlayer(1, 0));
        document.getElementById('btn-left').addEventListener('click', () => movePlayer(0, -1));
        document.getElementById('btn-right').addEventListener('click', () => movePlayer(0, 1));

        draw();
    </script>
</body>
</html>
"""

# Render the game inside Streamlit component
components.html(game_html, height=780, scrolling=False)
