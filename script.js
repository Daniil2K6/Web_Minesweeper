(function() {
    function createParticles() {
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 8 + 's';
            particle.style.background = i % 3 === 0 ? '#bf7aff' : (i % 3 === 1 ? '#ff7de9' : '#aa6eff');
            particle.style.width = (Math.random() * 6 + 2) + 'px';
            particle.style.height = particle.style.width;
            document.body.appendChild(particle);
        }
    }
    createParticles();

    const lightning = document.getElementById('lightning');
    function flashLightning() {
        lightning.style.setProperty('--x', (Math.random() * 100) + '%');
        lightning.style.setProperty('--y', (Math.random() * 100) + '%');
        lightning.classList.add('flash');
        setTimeout(() => {
            lightning.classList.remove('flash');
        }, 300);
    }

    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth) * 100;
        const y = (e.clientY / window.innerHeight) * 100;
        lightning.style.setProperty('--x', x + '%');
        lightning.style.setProperty('--y', y + '%');
    });
    
    const ROWS = 9;
    const COLS = 9;
    const TOTAL_MINES = 10;

    let board = [];
    let revealed = [];
    let flags = [];
    let gameActive = true;
    let minesGenerated = false;
    
    // Таймер
    let gameStartTime = null;
    let timerInterval = null;
    let elapsedTime = 0;

    const API_BASE = 'http://localhost:8000/api';
    
    let currentRole = 'guest';
    let currentUser = null;
    let leaderboardData = [];

    // Функция форматирования времени (0.001 секунды)
    function formatTime(milliseconds) {
        const seconds = milliseconds / 1000;
        return seconds.toFixed(3) + 'с';
    }

    // Функция для запуска таймера
    function startTimer() {
        gameStartTime = Date.now();
        timerInterval = setInterval(() => {
            elapsedTime = Date.now() - gameStartTime;
            const timeDisplay = formatTime(elapsedTime);
            document.getElementById('gameTimer').textContent = timeDisplay;
        }, 10); // обновляем каждые 10 миллисекунд для плавности
    }

    // Функция для остановки таймера
    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        return elapsedTime / 1000; // возвращаем время в секундах
    }

    // API функции
    const apiClient = {
        async getCSRFToken() {
            try {
                const response = await fetch(`${API_BASE}/csrf-token`, {
                    method: 'GET',
                    credentials: 'include'
                });
                const data = await response.json();
                return data.csrfToken;
            } catch (error) {
                console.error('Ошибка получения CSRF токена:', error);
                return null;
            }
        },

        async getCurrentUser() {
            try {
                const response = await fetch(`${API_BASE}/current-user`, {
                    method: 'GET',
                    credentials: 'include'
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка получения текущего пользователя:', error);
                return { is_authenticated: false };
            }
        },

        async register(username, password) {
            try {
                const csrfToken = await this.getCSRFToken();
                const response = await fetch(`${API_BASE}/register`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: { 
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ username, password })
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка регистрации:', error);
                throw error;
            }
        },

        async login(username, password) {
            try {
                const csrfToken = await this.getCSRFToken();
                const response = await fetch(`${API_BASE}/login`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: { 
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ username, password })
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка входа:', error);
                throw error;
            }
        },

        async logout() {
            try {
                const csrfToken = await this.getCSRFToken();
                await fetch(`${API_BASE}/logout`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: { 'X-CSRFToken': csrfToken }
                });
            } catch (error) {
                console.error('Ошибка выхода:', error);
            }
        },

        async getLeaderboard() {
            try {
                const response = await fetch(`${API_BASE}/leaderboard`, {
                    method: 'GET',
                    credentials: 'include'
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка получения лидерборда:', error);
                return leaderboardData;
            }
        },

        async saveScore(time) {
            try {
                const csrfToken = await this.getCSRFToken();
                const response = await fetch(`${API_BASE}/save-score`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: { 
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ time })
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка сохранения результата:', error);
                throw error;
            }
        },

        async getUserStats() {
            try {
                const response = await fetch(`${API_BASE}/user-stats`, {
                    method: 'GET',
                    credentials: 'include'
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка получения статистики:', error);
                throw error;
            }
        },

        async resetLeaderboard() {
            try {
                const response = await fetch(`${API_BASE}/admin/reset-leaderboard`, {
                    method: 'POST',
                    credentials: 'include'
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка сброса лидерборда:', error);
                throw error;
            }
        },

        async deletePlayer(username) {
            try {
                const response = await fetch(`${API_BASE}/admin/delete-player/${username}`, {
                    method: 'DELETE',
                    credentials: 'include'
                });
                return await response.json();
            } catch (error) {
                console.error('Ошибка удаления игрока:', error);
                throw error;
            }
        }
    };

    const boardElement = document.getElementById('board');
    const mineCounterElement = document.getElementById('mineCounter');
    const resetBtn = document.getElementById('resetGameBtn');
    const gameStatusEl = document.getElementById('gameStatus');
    const rightSection = document.getElementById('rightSection');
    const roleBadge = document.getElementById('roleBadge');

    function formatMines(count) {
        return count.toString().padStart(3, '0');
    }

    function updateMineCounter() {
        let flaggedCount = 0;
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                if (flags[r][c]) flaggedCount++;
            }
        }
        const remaining = TOTAL_MINES - flaggedCount;
        mineCounterElement.textContent = formatMines(remaining >= 0 ? remaining : 0);
    }

    function initMatrices() {
        board = Array(ROWS).fill().map(() => Array(COLS).fill(0));
        revealed = Array(ROWS).fill().map(() => Array(COLS).fill(false));
        flags = Array(ROWS).fill().map(() => Array(COLS).fill(false));
        minesGenerated = false;
        gameActive = true;
    }

    function generateMines(firstRow, firstCol) {
        let minesPlaced = 0;
        
        while (minesPlaced < TOTAL_MINES) {
            const r = Math.floor(Math.random() * ROWS);
            const c = Math.floor(Math.random() * COLS);
            if ((r === firstRow && c === firstCol) || board[r][c] === -1) continue;
            board[r][c] = -1;
            minesPlaced++;
        }

        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                if (board[r][c] === -1) continue;
                let count = 0;
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        if (dr === 0 && dc === 0) continue;
                        const nr = r + dr;
                        const nc = c + dc;
                        if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && board[nr][nc] === -1) count++;
                    }
                }
                board[r][c] = count;
            }
        }
    }

    function revealCell(row, col) {
        if (!gameActive) return;
        if (row < 0 || row >= ROWS || col < 0 || col >= COLS) return;
        if (revealed[row][col] || flags[row][col]) return;

        revealed[row][col] = true;

        if (board[row][col] === -1) {
            gameActive = false;
            gameStatusEl.textContent = '💥 БАХ! ПРИЗРАЧНАЯ МИНА ВЗОРВАЛАСЬ! 💥';
            flashLightning();
            
            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) {
                    if (board[r][c] === -1) revealed[r][c] = true;
                }
            }
            renderBoard();
            return;
        }

        if (board[row][col] === 0) {
            for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                    if (dr === 0 && dc === 0) continue;
                    const nr = row + dr;
                    const nc = col + dc;
                    if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && !revealed[nr][nc] && !flags[nr][nc]) {
                        revealCell(nr, nc);
                    }
                }
            }
        }

        checkWin();
    }

    function checkWin() {
        let allSafeRevealed = true;
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                if (board[r][c] !== -1 && !revealed[r][c]) {
                    allSafeRevealed = false;
                    break;
                }
            }
        }

        if (allSafeRevealed && gameActive) {
            gameActive = false;
            const finalTime = stopTimer();
            
            gameStatusEl.textContent = '🎉 ПОБЕДА! ФИОЛЕТОВАЯ МОЛНИЯ! 🎉';
            console.log('Победа! Время:', finalTime, 'Статус:', { role: currentRole, user: currentUser });
            flashLightning();
            
            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) {
                    if (board[r][c] === -1) flags[r][c] = true;
                }
            }
            renderBoard();
            
            if (currentRole === 'user' && currentUser) {
                console.log('Сохраняем результат на сервер:', finalTime);
                apiClient.saveScore(finalTime)
                    .then(result => {
                        console.log('Результат сохранён:', result);
                        gameStatusEl.textContent = '✅ Результат сохранён!';
                    })
                    .catch(error => {
                        console.error('Ошибка сохранения результата:', error);
                        gameStatusEl.textContent = '⚠️ Не удалось сохранить результат';
                    });
            } else {
                console.log('Пользователь не залогинен, результат не сохраняется');
                gameStatusEl.textContent = '👻 Результат не сохранён (авторизуйтесь чтобы сохранить)';
            }
        }
    }

    function toggleFlag(row, col) {
        if (!gameActive) return;
        if (revealed[row][col]) return;
        flags[row][col] = !flags[row][col];
        updateMineCounter();
        renderBoard();
    }

    function leftClickHandler(row, col) {
        if (!gameActive) return;
        if (revealed[row][col] || flags[row][col]) return;

        if (!minesGenerated) {
            generateMines(row, col);
            minesGenerated = true;
            startTimer();
        }

        revealCell(row, col);
        updateMineCounter();
        renderBoard();
    }

    function renderBoard() {
        boardElement.innerHTML = '';
        
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                
                if (revealed[r][c]) {
                    cell.classList.add('revealed');
                    if (board[r][c] === -1) {
                        cell.textContent = '💣';
                        if (Math.random() < 0.3) cell.classList.add('ghost-mine');
                    } else {
                        const val = board[r][c];
                        cell.textContent = val === 0 ? '' : val;
                        cell.setAttribute('data-value', val);
                    }
                } else {
                    if (flags[r][c]) {
                        cell.classList.add('flagged');
                    }
                    if (Math.random() < 0.1 && !flags[r][c]) {
                        cell.classList.add('ghost-mine');
                    }
                }
                
                cell.dataset.row = r;
                cell.dataset.col = c;
                
                cell.addEventListener('click', (e) => {
                    e.preventDefault();
                    const rr = parseInt(e.currentTarget.dataset.row);
                    const cc = parseInt(e.currentTarget.dataset.col);
                    leftClickHandler(rr, cc);
                });
                
                cell.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    const rr = parseInt(e.currentTarget.dataset.row);
                    const cc = parseInt(e.currentTarget.dataset.col);
                    toggleFlag(rr, cc);
                });
                
                boardElement.appendChild(cell);
            }
        }
    }

    function resetGame() {
        stopTimer();
        document.getElementById('gameTimer').textContent = '0.000с';
        initMatrices();
        renderBoard();
        updateMineCounter();
        gameActive = true;
        minesGenerated = false;
        gameStatusEl.textContent = '⚡ НОВАЯ ИГРА ⚡';
    }
    
    function updateRoleUI() {
        roleBadge.className = 'role-badge ' + currentRole;
        
        if (currentRole === 'guest') {
            roleBadge.innerHTML = '👤 ГОСТЬ';
        } else if (currentRole === 'user') {
            roleBadge.innerHTML = `⭐ ${currentUser || 'ЮЗЕР'}`;
        } else if (currentRole === 'admin') {
            roleBadge.innerHTML = `🛡️ АДМИН ${currentUser || ''}`;
        }
    }

    function renderLeaderboard() {
        let rows = '';
        const topPlayers = leaderboardData.slice(0, 100);
        topPlayers.forEach((player, index) => {
            const timeStr = formatTime(player.time * 1000);
            const date = new Date(player.created_at).toLocaleDateString('ru-RU', {
                month: 'short',
                day: 'numeric'
            });
            rows += `
                <tr>
                    <td>${index + 1}. ${player.username}</td>
                    <td>${timeStr}</td>
                    <td style="font-size:0.85em; color:#a890c0;">${date}</td>
                </tr>
            `;
        });
        return rows;
    }

    function renderAdminUserList() {
        let list = '';
        leaderboardData.forEach((player, index) => {
            list += `
                <div class="admin-user-row">
                    <span>${player.username}</span>
                    <span style="color:#9effb0;">👻 онлайн</span>
                    <button class="remove-user-btn" data-username="${player.username}">✕</button>
                </div>
            `;
        });
        return list;
    }

    function removeUserFromLeaderboard(username) {
        leaderboardData = leaderboardData.filter(player => player.username !== username);
        if (currentRole === 'admin') {
            renderRightPanel();
        }
        gameStatusEl.textContent = `👻 Игрок ${username} удалён из лидерборда`;
        flashLightning();
    }

    function renderRightPanel() {
        let html = '';
        
        if (currentRole === 'guest') {
            html = `
                <div class="register-box">
                    <div class="register-title">🔐 ВХОД / РЕГИСТРАЦИЯ</div>
                    <div id="loginForm">
                        <div style="margin-bottom:10px; font-size:0.9em; color:#b0a0d0;">ВХОД</div>
                        <input type="text" class="register-input" id="loginUsername" placeholder="имя пользователя">
                        <input type="password" class="register-input" id="loginPassword" placeholder="пароль">
                        <div id="loginError" class="error-message" style="display: none;"></div>
                        <button class="register-button" id="loginBtn">🌐 ВОЙТИ</button>
                        <button class="register-button" style="background:#3a3a5a; margin-top:8px;" id="switchToRegister">📝 Создать аккаунт</button>
                    </div>
                    
                    <div id="registerForm" style="display:none;">
                        <div style="margin-bottom:10px; font-size:0.9em; color:#b0a0d0;">НОВЫЙ АККАУНТ</div>
                        <input type="text" class="register-input" id="usernameInput" placeholder="имя пользователя" value="Игрок_${Math.floor(Math.random() * 1000)}">
                        <input type="password" class="register-input" id="passwordInput" placeholder="пароль">
                        <div id="registerError" class="error-message" style="display: none;"></div>
                        <button class="register-button" id="registerBtn">🌟 ЗАРЕГИСТРИРОВАТЬСЯ</button>
                        <button class="register-button" style="background:#3a3a5a; margin-top:8px;" id="switchToLogin">🌐 Есть аккаунт?</button>
                    </div>
                </div>
                </div>
                <div class="leaderboard">
                    <h3>🏆 ТОП ИГРОКОВ</h3>
                    <table class="leaderboard-table">
                        <thead><tr><th>МЕСТО И ИГРОК</th><th>ВРЕМЯ</th><th>ДАТА</th></tr></thead>
                        <tbody>
                            ${renderLeaderboard()}
                        </tbody>
                    </table>
                    <div class="backend-hint" id="guestLeaderboardHint">⚡ загрузить с бэкенда</div>
                </div>
            `;
        } else if (currentRole === 'user') {
            html = `
                <div class="register-box">
                    <div class="register-title">⭐ ПРИВЕТ, ${currentUser}</div>
                    <div style="background:#2b1e3d; border-radius:40px; padding:15px; margin-bottom:16px; border:1px solid #9b79cf;">
                        Ты в игре, удачи! Результаты сохраняются автоматически.
                    </div>
                    <button class="register-button" style="background:#352c4a;" id="logoutBtn">🚪 ВЫЙТИ</button>
                </div>
                <div class="leaderboard">
                    <h3>🏆 ТВОЙ ТОП</h3>
                    <table class="leaderboard-table">
                        <thead><tr><th>МЕСТО И ИГРОК</th><th>ВРЕМЯ</th><th>ДАТА</th></tr></thead>
                        <tbody>
                            ${renderLeaderboard()}
                        </tbody>
                    </table>
                    <div class="backend-hint" id="userLeaderboardHint">⚡ моя статистика</div>
                </div>
            `;
        } else if (currentRole === 'admin') {
            html = `
                <div class="register-box">
                    <div class="register-title">🛡️ АДМИНКА</div>
                    <div style="background:#2b1d3e; border-radius:40px; padding:15px; margin-bottom:16px; border:2px solid #ff44aa;">
                        ${currentUser}, ты управляешь всем
                    </div>
                    <button class="register-button" id="resetLeaderboardBtn" style="background:#6b3f6b;">⚡ СБРОСИТЬ ЛИДЕРБОРД</button>
                    <button class="register-button" style="margin-top:10px; background:#4f3a6b;" id="adminLogoutBtn">🚪 ВЫЙТИ ИЗ АДМИНКИ</button>
                </div>
                <div class="leaderboard" style="border-color:#ff88ff;">
                    <h3>👥 УПРАВЛЕНИЕ ИГРОКАМИ</h3>
                    <div id="usersList">
                        ${renderAdminUserList()}
                    </div>
                    <div class="backend-hint" id="adminHint">⚡ нажми ✕ чтобы удалить игрока</div>
                </div>
            `;
        }
        
        rightSection.innerHTML = html;
        
        if (currentRole === 'guest') {
            // Обработчик переключения на форму регистрации
            document.getElementById('switchToRegister')?.addEventListener('click', () => {
                document.getElementById('loginForm').style.display = 'none';
                document.getElementById('registerForm').style.display = 'block';
            });
            
            // Обработчик переключения на форму логина
            document.getElementById('switchToLogin')?.addEventListener('click', () => {
                document.getElementById('registerForm').style.display = 'none';
                document.getElementById('loginForm').style.display = 'block';
            });
            
            // Обработчик логина
            document.getElementById('loginBtn')?.addEventListener('click', async () => {
                const username = document.getElementById('loginUsername')?.value.trim() || '';
                const password = document.getElementById('loginPassword')?.value.trim() || '';
                const errorEl = document.getElementById('loginError');
                
                console.log('Попытка входа:', { username });
                
                if (!username || !password) {
                    errorEl.style.display = 'block';
                    errorEl.textContent = 'Введите имя пользователя и пароль';
                    gameStatusEl.textContent = '❌ Заполните все поля';
                    return;
                }
                
                errorEl.style.display = 'none';
                gameStatusEl.textContent = '📡 Входим...';
                
                try {
                    const result = await apiClient.login(username, password);
                    console.log('Ответ от логина:', result);
                    
                    if (result.error) {
                        errorEl.style.display = 'block';
                        errorEl.textContent = result.error;
                        gameStatusEl.textContent = '❌ ' + result.error;
                        currentRole = 'guest';
                        currentUser = null;
                        updateRoleUI();
                        renderRightPanel();
                    } else if (result.username) {
                        currentRole = result.role || 'user';
                        currentUser = result.username;
                        gameStatusEl.textContent = `🌟 Добро пожаловать, ${currentUser}!`;
                        console.log('Вход успешен:', { role: currentRole, user: currentUser });
                        flashLightning();
                        updateRoleUI();
                        renderRightPanel();
                    } else {
                        console.log('Неожиданный ответ:', result);
                        errorEl.style.display = 'block';
                        errorEl.textContent = 'Ошибка при входе';
                    }
                } catch (error) {
                    console.error('Ошибка при входе:', error);
                    errorEl.style.display = 'block';
                    errorEl.textContent = 'Ошибка подключения';
                    gameStatusEl.textContent = '❌ Ошибка подключения к серверу';
                }
            });
            
            document.getElementById('registerBtn')?.addEventListener('click', async () => {
                const nick = document.getElementById('usernameInput')?.value.trim() || 'Игрок';
                const password = document.getElementById('passwordInput')?.value.trim() || '';
                const errorEl = document.getElementById('registerError');
                
                console.log('Попытка регистрации:', { username: nick });
                
                if (!nick || !password) {
                    errorEl.style.display = 'block';
                    errorEl.textContent = 'Введите имя пользователя и пароль';
                    gameStatusEl.textContent = '❌ Заполните все поля';
                    return;
                }
                
                errorEl.style.display = 'none';
                gameStatusEl.textContent = '📡 Регистрируем...';
                
                try {
                    const result = await apiClient.register(nick, password);
                    console.log('Ответ от регистрации:', result);
                    
                    if (result.error) {
                        errorEl.style.display = 'block';
                        errorEl.textContent = result.error;
                        gameStatusEl.textContent = '❌ ' + result.error;
                        currentRole = 'guest';
                        currentUser = null;
                        updateRoleUI();
                        renderRightPanel();
                    } else if (result.username) {
                        currentRole = 'user';
                        currentUser = result.username;
                        gameStatusEl.textContent = `🌟 Добро пожаловать, ${currentUser}!`;
                        console.log('Регистрация успешна:', { user: currentUser });
                        flashLightning();
                        updateRoleUI();
                        renderRightPanel();
                    } else {
                        console.log('Неожиданный ответ от регистрации:', result);
                        errorEl.style.display = 'block';
                        errorEl.textContent = 'Ошибка при регистрации';
                    }
                } catch (error) {
                    console.error('Ошибка при регистрации:', error);
                    errorEl.style.display = 'block';
                    errorEl.textContent = 'Ошибка подключения';
                    gameStatusEl.textContent = '❌ Ошибка подключения к серверу';
                    currentRole = 'guest';
                    currentUser = null;
                    updateRoleUI();
                    renderRightPanel();
                }
            });
            
            document.getElementById('guestLeaderboardHint')?.addEventListener('click', async () => {
                gameStatusEl.textContent = '📡 Загружаем лидерборд...';
                try {
                    const data = await apiClient.getLeaderboard();
                    if (Array.isArray(data) && data.length > 0) {
                        leaderboardData = data;
                        renderRightPanel();
                        gameStatusEl.textContent = '✅ Лидеборд загружен!';
                    } else {
                        gameStatusEl.textContent = '⚠️ Лидеборд пуст';
                    }
                } catch (error) {
                    gameStatusEl.textContent = '❌ Ошибка загрузки лидерборда';
                }
            });
        }
        
        if (currentRole === 'user') {
            document.getElementById('logoutBtn')?.addEventListener('click', async () => {
                try {
                    await apiClient.logout();
                } catch (error) {}
                
                currentRole = 'guest';
                currentUser = null;
                updateRoleUI();
                renderRightPanel();
                gameStatusEl.textContent = '👋 Ты вышел. Возвращайся!';
            });
            
            document.getElementById('userLeaderboardHint')?.addEventListener('click', async () => {
                gameStatusEl.textContent = '📡 Загружаем твою статистику...';
                try {
                    const stats = await apiClient.getUserStats();
                    gameStatusEl.textContent = `📊 Побед: ${stats.stats.wins}/${stats.stats.total_games}`;
                } catch (error) {
                    gameStatusEl.textContent = '❌ Ошибка загрузки статистики';
                }
            });
        }
        
        if (currentRole === 'admin') {
            document.getElementById('resetLeaderboardBtn')?.addEventListener('click', async () => {
                gameStatusEl.textContent = '🌩️ Сбрасываем лидерборд...';
                try {
                    await apiClient.resetLeaderboard();
                    const data = await apiClient.getLeaderboard();
                    leaderboardData = data;
                    renderRightPanel();
                    gameStatusEl.textContent = '🌩️ ЛИДЕРБОРД СБРОШЕН!';
                    flashLightning();
                    flashLightning();
                } catch (error) {
                    gameStatusEl.textContent = '❌ Ошибка сброса лидерборда';
                }
            });
            
            document.getElementById('adminLogoutBtn')?.addEventListener('click', async () => {
                try {
                    await fetch(`${API_BASE}/admin/logout`, {
                        method: 'POST',
                        credentials: 'include'
                    });
                } catch (error) {}
                
                currentRole = 'guest';
                currentUser = null;
                updateRoleUI();
                renderRightPanel();
                gameStatusEl.textContent = '👋 Админ вышел. Возвращайся!';
                flashLightning();
            });
            
            document.querySelectorAll('.remove-user-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    const username = btn.dataset.username;
                    try {
                        await apiClient.deletePlayer(username);
                        removeUserFromLeaderboard(username);
                        gameStatusEl.textContent = `👻 Игрок ${username} удалён`;
                    } catch (error) {
                        gameStatusEl.textContent = '❌ Ошибка удаления игрока';
                    }
                });
            });
        }
    }
    
    async function initializeApp() {
        // Проверяем, аутентифицирован ли пользователь
        try {
            const userData = await apiClient.getCurrentUser();
            if (userData.is_authenticated) {
                currentRole = userData.role || 'user';
                currentUser = userData.username;
                gameStatusEl.textContent = `🌟 С возвращением, ${currentUser}!`;
                updateRoleUI();
            }
        } catch (error) {
            console.log('Ошибка при проверке аутентификации:', error);
        }
        
        // Загружаем лидерборд
        try {
            const data = await apiClient.getLeaderboard();
            if (Array.isArray(data) && data.length > 0) {
                leaderboardData = data;
            } else {
                leaderboardData = [];
            }
        } catch (error) {
            console.log('Используем локальный лидерборд');
            leaderboardData = [];
        }
        
        initMatrices();
        renderBoard();
        updateMineCounter();
        renderRightPanel();
        updateRoleUI();
    }
    
    resetBtn.addEventListener('click', resetGame);
    
    // Инициализируем приложение при загрузке
    initializeApp();
})();