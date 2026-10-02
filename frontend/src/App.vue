<template>
  <div class="app">
    <!-- Hero секция -->
    <header class="hero">
      <div class="hero-content">
        <h1 class="hero-title">🎖️ WORLD OF TANKS</h1>
        <p class="hero-subtitle">Система учёта статистики боёв</p>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">{{ tanks.length }}</div>
            <div class="stat-label">Танков</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ players.length }}</div>
            <div class="stat-label">Игроков</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ totalBattles }}</div>
            <div class="stat-label">Всего боёв</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ averageWinrate }}%</div>
            <div class="stat-label">Средний винрейт</div>
          </div>
        </div>
      </div>
    </header>

    <!-- Секция Танки -->
    <section class="section">
      <div class="section-header">
        <h2>🛡️ Ангар техники</h2>
        <button class="btn" @click="loadTanks" :disabled="loadingTanks">
          {{ loadingTanks ? 'Загрузка...' : 'Загрузить танки' }}
        </button>
      </div>
      
      <div v-if="tanks.length > 0" class="cards-grid">
        <div v-for="tank in tanks" :key="tank.id" class="tank-card">
          <div class="tank-tier">LVL {{ tank.tier }}</div>
          <h3 class="tank-name">{{ tank.name }}</h3>
          <div class="tank-info">
            <span class="badge" :class="tank.tank_type.toLowerCase()">{{ getTypeName(tank.tank_type) }}</span>
            <span class="nation">{{ getNationFlag(tank.nation) }} {{ tank.nation }}</span>
          </div>
        </div>
      </div>
      <div v-else-if="!loadingTanks" class="empty-state">
        Нажмите кнопку, чтобы загрузить танки из базы данных
      </div>
    </section>

    <!-- Секция Игроки -->
    <section class="section section-dark">
      <div class="section-header">
        <h2>👥 Командиры</h2>
        <button class="btn" @click="loadPlayers" :disabled="loadingPlayers">
          {{ loadingPlayers ? 'Загрузка...' : 'Загрузить игроков' }}
        </button>
      </div>
      
      <div v-if="players.length > 0" class="players-grid">
        <div v-for="player in players" :key="player.id" class="player-card">
          <div class="player-avatar">
            {{ player.nickname.charAt(0).toUpperCase() }}
          </div>
          <div class="player-info">
            <h3 class="player-name">{{ player.nickname }}</h3>
            <div class="player-stats">
              <div class="player-stat">
                <span class="stat-num">{{ player.battles }}</span>
                <span class="stat-text">боёв</span>
              </div>
              <div class="player-stat">
                <span class="stat-num">{{ player.wins }}</span>
                <span class="stat-text">побед</span>
              </div>
            </div>
            <div class="winrate-bar">
              <div class="winrate-fill" :style="{ width: getWinrate(player) + '%' }">
                <span class="winrate-text">{{ getWinrate(player) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="!loadingPlayers" class="empty-state">
        Нажмите кнопку, чтобы загрузить игроков из базы данных
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>Лабораторная работа №1 • CI/CD с Jenkins • 2026</p>
      <p class="footer-tech">Django REST Framework + Vue.js + SQLite</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      tanks: [],
      players: [],
      loadingTanks: false,
      loadingPlayers: false
    }
  },
  computed: {
    totalBattles() {
      return this.players.reduce((sum, p) => sum + p.battles, 0)
    },
    averageWinrate() {
      if (this.players.length === 0) return 0
      const total = this.players.reduce((sum, p) => {
        return sum + (p.battles > 0 ? (p.wins / p.battles) * 100 : 0)
      }, 0)
      return (total / this.players.length).toFixed(1)
    }
  },
  methods: {
    async loadTanks() {
      this.loadingTanks = true
      try {
        const response = await fetch('http://localhost:8000/api/tanks/')
        this.tanks = await response.json()
      } catch (error) {
        console.error('Ошибка загрузки танков:', error)
        alert('Не удалось загрузить танки. Убедитесь, что Django запущен на порту 8000')
      } finally {
        this.loadingTanks = false
      }
    },
    async loadPlayers() {
      this.loadingPlayers = true
      try {
        const response = await fetch('http://localhost:8000/api/players/')
        this.players = await response.json()
      } catch (error) {
        console.error('Ошибка загрузки игроков:', error)
        alert('Не удалось загрузить игроков. Убедитесь, что Django запущен на порту 8000')
      } finally {
        this.loadingPlayers = false
      }
    },
    getWinrate(player) {
      if (player.battles === 0) return 0
      return ((player.wins / player.battles) * 100).toFixed(1)
    },
    getTypeName(type) {
      const types = {
        'HT': 'Тяжёлый',
        'MT': 'Средний',
        'LT': 'Лёгкий',
        'TD': 'ПТ-САУ',
        'SPG': 'Арта'
      }
      return types[type] || type
    },
    getNationFlag(nation) {
      const flags = {
        'USSR': '☭',
        'Germany': '🇩🇪',
        'USA': '🇺🇸',
        'UK': '🇬🇧',
        'France': '🇫🇷',
        'Japan': '🇯🇵',
        'China': '🇨🇳'
      }
      return flags[nation] || '🏳️'
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: #0f1419;
  color: #e0e0e0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app {
  min-height: 100vh;
}

/* Hero секция */
.hero {
  background: linear-gradient(135deg, #1a2332 0%, #2d3e2d 50%, #1a2332 100%);
  padding: 80px 20px;
  text-align: center;
  border-bottom: 3px solid #d4a017;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(212, 160, 23, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 50%, rgba(139, 69, 19, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  color: #d4a017;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
  letter-spacing: 4px;
  margin-bottom: 10px;
  font-weight: 900;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #a0a0a0;
  margin-bottom: 40px;
  letter-spacing: 2px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.stat-card {
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid #d4a017;
  border-radius: 8px;
  padding: 25px 15px;
  backdrop-filter: blur(10px);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(212, 160, 23, 0.3);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #d4a017;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #a0a0a0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Секции */
.section {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-dark {
  background: #14191f;
  max-width: 100%;
  padding-left: calc((100% - 1200px) / 2 + 20px);
  padding-right: calc((100% - 1200px) / 2 + 20px);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.section-header h2 {
  font-size: 2rem;
  color: #d4a017;
  border-left: 4px solid #d4a017;
  padding-left: 15px;
}

/* Кнопки */
.btn {
  background: linear-gradient(135deg, #d4a017 0%, #8b6914 100%);
  color: #0f1419;
  border: none;
  padding: 12px 28px;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(212, 160, 23, 0.3);
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 160, 23, 0.5);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Карточки танков */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.tank-card {
  background: linear-gradient(145deg, #1e2832 0%, #14191f 100%);
  border: 1px solid #2d3e2d;
  border-radius: 8px;
  padding: 25px;
  position: relative;
  transition: all 0.3s;
  overflow: hidden;
}

.tank-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 3px;
  background: linear-gradient(90deg, #d4a017, transparent);
}

.tank-card:hover {
  transform: translateY(-5px);
  border-color: #d4a017;
  box-shadow: 0 10px 30px rgba(212, 160, 23, 0.2);
}

.tank-tier {
  display: inline-block;
  background: #d4a017;
  color: #0f1419;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: bold;
  margin-bottom: 12px;
}

.tank-name {
  font-size: 1.4rem;
  color: #ffffff;
  margin-bottom: 15px;
}

.tank-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.badge {
  padding: 4px 10px;
  border-radius: 3px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.badge.ht { background: #8b0000; color: white; }
.badge.mt { background: #2e7d32; color: white; }
.badge.lt { background: #1565c0; color: white; }
.badge.td { background: #6a1b9a; color: white; }
.badge.spg { background: #e65100; color: white; }

.nation {
  color: #a0a0a0;
  font-size: 0.9rem;
}

/* Карточки игроков */
.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.player-card {
  background: linear-gradient(145deg, #1e2832 0%, #14191f 100%);
  border: 1px solid #2d3e2d;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  gap: 20px;
  align-items: center;
  transition: all 0.3s;
}

.player-card:hover {
  border-color: #d4a017;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(212, 160, 23, 0.2);
}

.player-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4a017, #8b6914);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
  color: #0f1419;
  flex-shrink: 0;
}

.player-info {
  flex: 1;
  min-width: 0;
}

.player-name {
  font-size: 1.2rem;
  color: #ffffff;
  margin-bottom: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 10px;
}

.player-stat {
  display: flex;
  flex-direction: column;
}

.stat-num {
  font-size: 1.3rem;
  font-weight: bold;
  color: #d4a017;
}

.stat-text {
  font-size: 0.8rem;
  color: #a0a0a0;
  text-transform: uppercase;
}

.winrate-bar {
  background: #0f1419;
  border-radius: 10px;
  height: 24px;
  overflow: hidden;
  position: relative;
}

.winrate-fill {
  background: linear-gradient(90deg, #2e7d32 0%, #d4a017 50%, #8b0000 100%);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
  transition: width 0.8s ease-out;
  min-width: 50px;
}

.winrate-text {
  font-size: 0.85rem;
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

/* Пустое состояние */
.empty-state {
  text-align: center;
  padding: 40px;
  color: #606060;
  font-style: italic;
  border: 1px dashed #2d3e2d;
  border-radius: 8px;
}

/* Footer */
.footer {
  background: #0a0d10;
  padding: 30px 20px;
  text-align: center;
  border-top: 2px solid #d4a017;
  margin-top: 40px;
}

.footer p {
  color: #a0a0a0;
  margin-bottom: 5px;
}

.footer-tech {
  font-size: 0.85rem;
  color: #606060;
  letter-spacing: 1px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
    letter-spacing: 2px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .player-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>