from flask import Flask, render_template_string
import random

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Word Chain Game</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }

        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }

        .menu-screen, .game-screen, .setup-screen {
            display: none;
        }

        .menu-screen.active, .game-screen.active, .setup-screen.active {
            display: block;
        }

        .btn {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #f093fb;
        }

        .btn-secondary:hover {
            background: #f5576c;
            transform: translateY(-2px);
        }

        .rules {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .rules h3 {
            color: #667eea;
            margin-bottom: 10px;
        }

        .rules ul {
            padding-left: 20px;
        }

        .rules li {
            margin: 8px 0;
            color: #555;
        }

        .game-info {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            font-weight: 600;
        }

        .word-history {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            max-height: 150px;
            overflow-y: auto;
        }

        .word-item {
            padding: 8px;
            margin: 5px 0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .word-item.user {
            background: #e3f2fd;
        }

        .word-item.computer {
            background: #fff3e0;
        }

        .word-item.player {
            background: #e8f5e9;
        }

        .input-group {
            margin: 20px 0;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        .input-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border 0.3s;
        }

        .input-group input:focus {
            outline: none;
            border-color: #667eea;
        }

        .message {
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            text-align: center;
            font-weight: 600;
            animation: fadeIn 0.3s;
        }

        .message.success {
            background: #d4edda;
            color: #155724;
        }

        .message.error {
            background: #f8d7da;
            color: #721c24;
        }

        .message.info {
            background: #d1ecf1;
            color: #0c5460;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .player-setup {
            margin: 20px 0;
        }

        .player-input {
            display: flex;
            gap: 10px;
            margin: 10px 0;
        }

        .player-input input {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
        }

        .current-turn {
            background: #fff3e0;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
            font-size: 1.2em;
            font-weight: 600;
            color: #e65100;
        }

        .game-over {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }

        .game-over h2 {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Word Chain</h1>
        <p class="subtitle">Chain words together!</p>

        <!-- Menu Screen -->
        <div class="menu-screen active" id="menuScreen">
            <div class="rules">
                <h3>📜 Game Rules</h3>
                <ul>
                    <li>Har word previous word ke last letter se start hona chahiye</li>
                    <li>Koi word repeat nahi hona chahiye</li>
                    <li>Minimum 2 letters ka word</li>
                    <li>Galat word dene par = Game Over!</li>
                </ul>
            </div>
            <button class="btn btn-primary" onclick="startSetup('computer')">🤖 Computer ke Sath Khelo</button>
            <button class="btn btn-secondary" onclick="startSetup('multiplayer')">👥 Multiplayer Mode</button>
        </div>

        <!-- Setup Screen -->
        <div class="setup-screen" id="setupScreen">
            <div class="input-group">
                <label>Kitne Players? (2-6):</label>
                <input type="number" id="numPlayers" min="2" max="6" value="2">
            </div>
            <div class="player-setup" id="playerSetup"></div>
            <button class="btn btn-primary" onclick="startGame()">Game Start Karo</button>
            <button class="btn btn-secondary" onclick="backToMenu()">Back</button>
        </div>

        <!-- Game Screen -->
        <div class="game-screen" id="gameScreen">
            <div class="game-info">
                <div class="info-row">
                    <span>Mode:</span>
                    <span id="gameMode">-</span>
                </div>
                <div class="info-row">
                    <span>Words Played:</span>
                    <span id="wordsCount">0</span>
                </div>
                <div class="info-row">
                    <span>Next Letter:</span>
                    <span id="nextLetter" style="font-size: 1.5em;">-</span>
                </div>
            </div>

            <div class="current-turn" id="currentTurn">Aapki baari!</div>

            <div id="messageBox"></div>

            <div class="input-group">
                <label>Apna word enter karo:</label>
                <input type="text" id="wordInput" placeholder="Word type karo..." autocomplete="off">
            </div>

            <button class="btn btn-primary" onclick="submitWord()">Submit Karo</button>

            <div class="word-history" id="wordHistory"></div>

            <button class="btn btn-secondary" onclick="endGame()">Game Band Karo</button>
        </div>
    </div>

    <script>
        const wordBank = {
            'a': ['ant', 'apple', 'arrow', 'amazing', 'adventure', 'anchor', 'album', 'actor'],
            'b': ['ball', 'banana', 'butterfly', 'beautiful', 'basket', 'bridge', 'bread', 'button'],
            'c': ['cat', 'car', 'castle', 'curious', 'chocolate', 'camera', 'cloud', 'crystal'],
            'd': ['dog', 'door', 'dragon', 'delicious', 'diamond', 'dance', 'desert', 'dream'],
            'e': ['elephant', 'egg', 'energy', 'excellent', 'engine', 'eagle', 'earth', 'eclipse'],
            'f': ['fish', 'flower', 'friend', 'fantastic', 'forest', 'falcon', 'flame', 'frost'],
            'g': ['garden', 'galaxy', 'guitar', 'golden', 'game', 'ghost', 'grape', 'grass'],
            'h': ['house', 'happy', 'helicopter', 'holiday', 'heart', 'honey', 'hammer', 'hill'],
            'i': ['ice', 'island', 'interesting', 'intelligent', 'iron', 'ink', 'igloo', 'idea'],
            'j': ['jump', 'jungle', 'journey', 'joy', 'jacket', 'jazz', 'jewel', 'juice'],
            'k': ['king', 'kite', 'kitchen', 'knowledge', 'kangaroo', 'key', 'knight', 'koala'],
            'l': ['lion', 'laptop', 'lemon', 'lovely', 'library', 'lamp', 'leaf', 'light'],
            'm': ['monkey', 'mountain', 'music', 'magical', 'moon', 'mirror', 'marble', 'medal'],
            'n': ['night', 'nature', 'number', 'notebook', 'nice', 'nest', 'needle', 'north'],
            'o': ['orange', 'ocean', 'opportunity', 'office', 'owl', 'orbit', 'opera', 'olive'],
            'p': ['penguin', 'planet', 'puzzle', 'perfect', 'peace', 'piano', 'paint', 'pearl'],
            'q': ['queen', 'question', 'quick', 'quality', 'quiet', 'quilt', 'quest', 'quiz'],
            'r': ['rabbit', 'river', 'rocket', 'rainbow', 'rose', 'ring', 'rain', 'ruby'],
            's': ['sun', 'star', 'school', 'summer', 'smile', 'song', 'silver', 'storm'],
            't': ['tiger', 'tree', 'treasure', 'temple', 'technology', 'thunder', 'tower', 'table'],
            'u': ['umbrella', 'universe', 'unique', 'unity', 'ultimate', 'urban', 'uncle', 'upper'],
            'v': ['volcano', 'valley', 'victory', 'violet', 'village', 'voice', 'vapor', 'viper'],
            'w': ['water', 'window', 'wonderful', 'wisdom', 'world', 'whale', 'winter', 'wood'],
            'x': ['xylophone', 'xerox', 'xenon', 'xray'],
            'y': ['yellow', 'yoga', 'yesterday', 'young', 'yard', 'yolk', 'yacht', 'yarn'],
            'z': ['zebra', 'zero', 'zoo', 'zone', 'zigzag', 'zinc', 'zombie', 'zenith']
        };

        let gameState = {
            mode: null,
            usedWords: new Set(),
            currentLetter: null,
            players: [],
            currentPlayerIndex: 0,
            wordsCount: 0,
            gameActive: false
        };

        function startSetup(mode) {
            gameState.mode = mode;
            document.getElementById('menuScreen').classList.remove('active');
            
            if (mode === 'computer') {
                gameState.players = ['Aap', 'Computer'];
                startGame();
            } else {
                document.getElementById('setupScreen').classList.add('active');
                updatePlayerInputs();
            }
        }

        function updatePlayerInputs() {
            const num = parseInt(document.getElementById('numPlayers').value) || 2;
            const container = document.getElementById('playerSetup');
            container.innerHTML = '';
            
            for (let i = 0; i < num; i++) {
                const div = document.createElement('div');
                div.className = 'player-input';
                div.innerHTML = `
                    <input type="text" placeholder="Player ${i + 1} ka Naam" id="player${i}" value="Player ${i + 1}">
                `;
                container.appendChild(div);
            }
        }

        document.getElementById('numPlayers')?.addEventListener('change', updatePlayerInputs);

        function startGame() {
            if (gameState.mode === 'multiplayer') {
                const num = parseInt(document.getElementById('numPlayers').value) || 2;
                gameState.players = [];
                for (let i = 0; i < num; i++) {
                    const name = document.getElementById(`player${i}`)?.value || `Player ${i + 1}`;
                    gameState.players.push(name);
                }
                document.getElementById('setupScreen').classList.remove('active');
            }

            gameState.usedWords.clear();
            gameState.currentLetter = null;
            gameState.currentPlayerIndex = 0;
            gameState.wordsCount = 0;
            gameState.gameActive = true;

            document.getElementById('gameScreen').classList.add('active');
            document.getElementById('gameMode').textContent = gameState.mode === 'computer' ? 'vs Computer' : 'Multiplayer';
            document.getElementById('wordHistory').innerHTML = '';
            updateTurnDisplay();
            document.getElementById('wordInput').focus();
        }

        function updateTurnDisplay() {
            const currentPlayer = gameState.players[gameState.currentPlayerIndex];
            document.getElementById('currentTurn').textContent = 
                gameState.currentLetter 
                    ? `${currentPlayer} ki baari - "${gameState.currentLetter.toUpperCase()}" se start karo`
                    : `${currentPlayer} ki baari - Koi bhi word se start karo!`;
        }

        function submitWord() {
            if (!gameState.gameActive) return;

            const input = document.getElementById('wordInput');
            const word = input.value.toLowerCase().trim();
            
            if (!word) {
                showMessage('Koi word enter karo!', 'error');
                return;
            }

            const validation = validateWord(word);
            if (!validation.valid) {
                showMessage(validation.message, 'error');
                if (gameState.mode === 'computer' && gameState.currentPlayerIndex === 0) {
                    gameOver('Computer', validation.message);
                } else {
                    gameOver(gameState.players[gameState.currentPlayerIndex], validation.message);
                }
                return;
            }

            addWordToHistory(word, gameState.players[gameState.currentPlayerIndex]);
            gameState.usedWords.add(word);
            gameState.currentLetter = word[word.length - 1];
            gameState.wordsCount++;
            document.getElementById('wordsCount').textContent = gameState.wordsCount;
            document.getElementById('nextLetter').textContent = gameState.currentLetter.toUpperCase();
            input.value = '';

            showMessage(`✓ Sahi word: ${word}`, 'success');

            gameState.currentPlayerIndex = (gameState.currentPlayerIndex + 1) % gameState.players.length;

            if (gameState.mode === 'computer' && gameState.currentPlayerIndex === 1) {
                setTimeout(computerTurn, 1500);
            } else {
                updateTurnDisplay();
                input.focus();
            }
        }

        function validateWord(word) {
            if (word.length < 2) {
                return { valid: false, message: 'Word kam se kam 2 letters ka hona chahiye!' };
            }
            if (gameState.usedWords.has(word)) {
                return { valid: false, message: 'Ye word pehle use ho chuka hai!' };
            }
            if (gameState.currentLetter && word[0] !== gameState.currentLetter) {
                return { valid: false, message: `Word "${gameState.currentLetter.toUpperCase()}" se start hona chahiye!` };
            }
            return { valid: true };
        }

        function computerTurn() {
            if (!gameState.gameActive) return;

            showMessage('Computer soch raha hai...', 'info');
            document.getElementById('currentTurn').textContent = 'Computer soch raha hai...';

            const letter = gameState.currentLetter;
            const available = wordBank[letter]?.filter(w => !gameState.usedWords.has(w)) || [];

            setTimeout(() => {
                if (available.length === 0) {
                    gameOver('Aap', 'Computer ko koi word nahi mila!');
                    return;
                }

                const word = available[Math.floor(Math.random() * available.length)];
                gameState.usedWords.add(word);
                gameState.currentLetter = word[word.length - 1];
                gameState.wordsCount++;
                
                addWordToHistory(word, 'Computer');
                document.getElementById('wordsCount').textContent = gameState.wordsCount;
                document.getElementById('nextLetter').textContent = gameState.currentLetter.toUpperCase();
                
                showMessage(`✓ Computer ne kaha: ${word}`, 'success');
                
                gameState.currentPlayerIndex = 0;
                updateTurnDisplay();
                document.getElementById('wordInput').focus();
            }, 1000);
        }

        function addWordToHistory(word, player) {
            const history = document.getElementById('wordHistory');
            const div = document.createElement('div');
            div.className = `word-item ${player === 'Computer' ? 'computer' : player === 'Aap' ? 'user' : 'player'}`;
            div.innerHTML = `
                <span><strong>${player}:</strong> ${word}</span>
                <span>${word[word.length - 1].toUpperCase()}</span>
            `;
            history.insertBefore(div, history.firstChild);
        }

        function showMessage(text, type) {
            const box = document.getElementById('messageBox');
            box.innerHTML = `<div class="message ${type}">${text}</div>`;
            setTimeout(() => {
                box.innerHTML = '';
            }, 3000);
        }

        function gameOver(winner, reason) {
            gameState.gameActive = false;
            const box = document.getElementById('messageBox');
            box.innerHTML = `
                <div class="game-over">
                    <h2>🏆 Game Khatam!</h2>
                    <p><strong>Winner: ${winner}</strong></p>
                    <p>${reason}</p>
                    <p>Total words: ${gameState.wordsCount}</p>
                </div>
            `;
            document.getElementById('wordInput').disabled = true;
        }

        function endGame() {
            backToMenu();
        }

        function backToMenu() {
            document.getElementById('gameScreen').classList.remove('active');
            document.getElementById('setupScreen').classList.remove('active');
            document.getElementById('menuScreen').classList.add('active');
            document.getElementById('wordInput').disabled = false;
            document.getElementById('messageBox').innerHTML = '';
            gameState.gameActive = false;
        }

        document.getElementById('wordInput')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') submitWord();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("=" * 60)
    print("🎮 WORD CHAIN GAME SERVER STARTING...")
    print("=" * 60)
    print("📱 Open your browser and go to:")
    print("   👉 http://localhost:5000")
    print("   👉 http://127.0.0.1:5000")
    print("=" * 60)
    print("⚠️  Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)