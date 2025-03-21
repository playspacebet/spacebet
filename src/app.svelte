// App.svelte - Main component
<script>
  import { onMount } from 'svelte';
  import Sidebar from './components/Sidebar.svelte';
  import Hero from './components/Hero.svelte';
  import FeatureSection from './components/FeatureSection.svelte';
  import GameGallery from './components/GameGallery.svelte';
  import CtaSection from './components/CtaSection.svelte';
  import Footer from './components/Footer.svelte';

  let sidebarOpen = true;
  let isMobile = false;
  let isAuthenticated = false;
  let activeGame = null;
  let cryptoBalances = {
    BTC: 0.0045,
    ETH: 0.125,
    SOL: 2.34,
    USDT: 150.00
  };

  function toggleSidebar() {
    sidebarOpen = !sidebarOpen;
  }

  function checkScreenSize() {
    isMobile = window.innerWidth < 768;
    if (isMobile) {
      sidebarOpen = false;
    } else {
      sidebarOpen = true;
    }
  }

  function handleLogin() {
    // In a real implementation, this would validate credentials
    isAuthenticated = true;
  }

  function handleLogout() {
    isAuthenticated = false;
    activeGame = null;
  }

  function selectGame(game) {
    activeGame = game;
  }

  function handleDeposit(amount, currency) {
    // Simulate a successful deposit
    cryptoBalances[currency] += parseFloat(amount);
    return { success: true, message: `Successfully deposited ${amount} ${currency}` };
  }

  function handleWithdraw(amount, currency) {
    // Check if user has enough balance
    if (cryptoBalances[currency] >= parseFloat(amount)) {
      cryptoBalances[currency] -= parseFloat(amount);
      return { success: true, message: `Successfully withdrew ${amount} ${currency}` };
    } else {
      return { success: false, message: `Insufficient ${currency} balance` };
    }
  }

  onMount(() => {
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    createStars();

    return () => {
      window.removeEventListener('resize', checkScreenSize);
    };
  });

  function createStars() {
    const starsContainer = document.getElementById('stars');
    const starCount = 150;

    for (let i = 0; i < starCount; i++) {
      const star = document.createElement('div');
      star.classList.add('star');

      // Random position
      const x = Math.random() * 100;
      const y = Math.random() * 100;

      // Random size
      const size = Math.random() * 2 + 1;

      // Random animation delay
      const delay = Math.random() * 5;

      star.style.left = `${x}%`;
      star.style.top = `${y}%`;
      star.style.width = `${size}px`;
      star.style.height = `${size}px`;
      star.style.animationDelay = `${delay}s`;

      starsContainer.appendChild(star);
    }
  }

  // Game data
  const games = [
    {
      id: 'cosmic-slots',
      name: 'Cosmic Slots',
      type: 'slots',
      description: 'Take a spin through the cosmos with our space-themed slot machine.',
      minBet: 0.0001,
      maxBet: 0.1,
      currency: 'BTC',
      featured: true,
      image: '/images/games/cosmic-slots.jpg'
    },
    {
      id: 'lunar-roulette',
      name: 'Lunar Roulette',
      type: 'table',
      description: 'Place your bets on our lunar-themed roulette wheel.',
      minBet: 0.001,
      maxBet: 0.5,
      currency: 'BTC',
      featured: true,
      image: '/images/games/lunar-roulette.jpg'
    },
    {
      id: 'astro-blackjack',
      name: 'Astro Blackjack',
      type: 'table',
      description: 'Classic blackjack with a cosmic twist.',
      minBet: 0.0005,
      maxBet: 0.2,
      currency: 'BTC',
      featured: true,
      image: '/images/games/astro-blackjack.jpg'
    },
    {
      id: 'space-crash',
      name: 'Space Crash',
      type: 'crash',
      description: 'Watch the rocket soar and cash out before it crashes.',
      minBet: 0.0005,
      maxBet: 1.0,
      currency: 'BTC',
      featured: true,
      image: '/images/games/space-crash.jpg'
    },
    {
      id: 'galaxy-dice',
      name: 'Galaxy Dice',
      type: 'dice',
      description: 'Roll the dice across the galaxy and win big.',
      minBet: 0.0001,
      maxBet: 0.05,
      currency: 'BTC',
      featured: false,
      image: '/images/games/galaxy-dice.jpg'
    },
    {
      id: 'meteor-baccarat',
      name: 'Meteor Baccarat',
      type: 'table',
      description: 'Elegant card game with meteor-fast results.',
      minBet: 0.001,
      maxBet: 0.3,
      currency: 'BTC',
      featured: false,
      image: '/images/games/meteor-baccarat.jpg'
    }
  ];

  // Promotions
  const promotions = [
    {
      id: 'welcome-bonus',
      title: 'Welcome to Space: 100% Bonus',
      description: 'Get 100% bonus on your first deposit up to 1 BTC',
      endDate: '2025-05-01',
      image: '/images/promotions/welcome-bonus.jpg'
    },
    {
      id: 'weekly-cashback',
      title: 'Weekly Cosmic Cashback',
      description: 'Get 15% cashback on your losses every Monday',
      endDate: 'Ongoing',
      image: '/images/promotions/weekly-cashback.jpg'
    },
    {
      id: 'vip-program',
      title: 'Galactic VIP Program',
      description: 'Unlock exclusive rewards as you climb the VIP ranks',
      endDate: 'Ongoing',
      image: '/images/promotions/vip-program.jpg'
    }
  ];
  let loginModalOpen;
  let registerModalOpen;
</script>

<svelte:head>
  <title>SpaceBet - Take Your Bets to the Moon</title>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
</svelte:head>

<div class="app">
  <!-- Stars background -->
  <div class="stars" id="stars"></div>

  <!-- Sidebar toggle button (mobile) -->
  <button class="sidebar-toggle" class:active={sidebarOpen} on:click={toggleSidebar}>
    {#if sidebarOpen}✕{:else}☰{/if}
  </button>

  <!-- Sidebar -->
  <Sidebar
    {sidebarOpen}
    {isMobile}
    {games}
    {isAuthenticated}
    {cryptoBalances}
    on:selectGame={e => selectGame(e.detail)}
  />

  <!-- Main content -->
  <main class="main-content" class:sidebar-active={sidebarOpen && !isMobile}>
    <!-- Header -->
    <header>
      <a href="/static" class="logo">
        <div class="logo-icon">🚀</div>
        <span>Space</span>Bet
      </a>

      <nav>
        <ul>
          <li><a href="/static" class="active">Home</a></li>
          <li><a href="/games">Games</a></li>
          <li><a href="/promotions">Promotions</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/support">Support</a></li>
        </ul>
      </nav>

      <div class="auth-buttons">
        {#if !isAuthenticated}
          <button class="btn btn-outline" on:click={() => (loginModalOpen = true)}>Log In</button>
          <button class="btn btn-primary" on:click={() => (registerModalOpen = true)}>Sign Up</button>
        {:else}
          <div class="user-balance">
            <span>{cryptoBalances.BTC.toFixed(4)} BTC</span>
          </div>
          <button class="btn btn-outline" on:click={handleLogout}>Log Out</button>
        {/if}
      </div>
    </header>

    {#if activeGame}
      <!-- Game Component would go here -->
      <div class="game-container">
        <h2>{activeGame.name}</h2>
        <p>{activeGame.description}</p>
        <div class="game-frame">
          <!-- Game interface would be inserted here -->
          <p>Min Bet: {activeGame.minBet} {activeGame.currency}</p>
          <p>Max Bet: {activeGame.maxBet} {activeGame.currency}</p>
          <button class="btn btn-primary">Play Now</button>
        </div>
      </div>
    {:else}
      <!-- Landing page content -->
      <Hero
        slogan="Take Your Bets to the Moon"
        description="Experience the future of crypto gambling with SpaceBet. Play your favorite casino games with Bitcoin, Ethereum, and more. No KYC required."
        on:getStarted={() => (isAuthenticated ? null : registerModalOpen = true)}
      />

      <FeatureSection />

      <GameGallery
        featuredGames={games.filter(game => game.featured)}
        on:selectGame={e => selectGame(e.detail)}
      />

      <CtaSection
        title="Ready to Launch Your Cosmic Winning Streak?"
        description="Join thousands of players already winning big with SpaceBet. Sign up now and get a 100% bonus on your first deposit."
        on:createAccount={() => (isAuthenticated ? null : registerModalOpen = true)}
      />
    {/if}

    <Footer />
  </main>
</div>

<style>
  :global(:root) {
    --primary-color: #6c00ff;
    --secondary-color: #00d9ff;
    --accent-color: #ff7b00;
    --bg-dark: #0a0a1a;
    --bg-darker: #050510;
    --text-light: #ffffff;
    --text-dim: #a0a0c0;
    --card-bg: rgba(30, 30, 60, 0.7);
    --sidebar-width: 240px;
  }

  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Montserrat', 'Arial', sans-serif;
  }

  :global(body) {
    background-color: var(--bg-dark);
    color: var(--text-light);
    background-image:
      radial-gradient(circle at 20% 35%, rgba(108, 0, 255, 0.15) 0%, transparent 50%),
      radial-gradient(circle at 80% 10%, rgba(0, 217, 255, 0.1) 0%, transparent 50%);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Stars animation */
  .stars {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
  }

  :global(.star) {
    position: absolute;
    background-color: white;
    border-radius: 50%;
    opacity: 0.6;
    animation: twinkle 5s infinite;
  }

  @keyframes twinkle {
    0%, 100% { opacity: 0.2; }
    50% { opacity: 0.8; }
  }

  /* Header */
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    position: fixed;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 100;
    background: rgba(5, 5, 16, 0.8);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(108, 0, 255, 0.3);
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-light);
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .logo span {
    background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  .logo-icon {
    width: 2.2rem;
    height: 2.2rem;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    color: white;
  }

  nav ul {
    display: flex;
    gap: 2rem;
    list-style: none;
  }

  nav a {
    color: var(--text-light);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
    position: relative;
  }

  nav a:hover, nav a.active {
    color: var(--secondary-color);
  }

  nav a::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: -5px;
    left: 0;
    background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
    transition: width 0.3s;
  }

  nav a:hover::after, nav a.active::after {
    width: 100%;
  }

  .auth-buttons {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  .user-balance {
    background: rgba(108, 0, 255, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    border: 1px solid rgba(108, 0, 255, 0.4);
    font-weight: 600;
  }

  :global(.btn) {
    padding: 0.6rem 1.2rem;
    border-radius: 4px;
    font-weight: 600;
    transition: all 0.2s;
    cursor: pointer;
    text-decoration: none;
    border: none;
    outline: none;
  }

  :global(.btn-primary) {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    box-shadow: 0 4px 15px rgba(108, 0, 255, 0.3);
  }

  :global(.btn-primary:hover) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108, 0, 255, 0.4);
  }

  :global(.btn-outline) {
    background: transparent;
    color: var(--text-light);
    border: 1px solid var(--secondary-color);
  }

  :global(.btn-outline:hover) {
    background: rgba(0, 217, 255, 0.1);
  }

  /* Sidebar toggle button */
  .sidebar-toggle {
    position: fixed;
    top: 1.5rem;
    left: 1.5rem;
    z-index: 101;
    background: transparent;
    border: none;
    color: var(--text-light);
    font-size: 1.5rem;
    cursor: pointer;
    display: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    transition: background 0.2s;
  }

  .sidebar-toggle:hover {
    background: rgba(108, 0, 255, 0.1);
  }

  .sidebar-toggle.active {
    background: rgba(108, 0, 255, 0.2);
  }

  /* Main content */
  .main-content {
    padding: 7rem 2rem 2rem;
    margin-left: var(--sidebar-width);
    min-height: 100vh;
    transition: margin-left 0.3s ease;
  }

  .game-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 0;
  }

  .game-frame {
    background: var(--card-bg);
    border-radius: 10px;
    border: 1px solid rgba(108, 0, 255, 0.3);
    padding: 2rem;
    margin-top: 1.5rem;
    height: 500px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  /* Mobile responsiveness */
  @media (max-width: 992px) {
    .main-content {
      padding: 7rem 1rem 2rem;
    }
  }

  @media (max-width: 768px) {
    .sidebar-toggle {
      display: block;
    }

    .main-content {
      margin-left: 0;
    }

    .main-content.sidebar-active {
      margin-left: 0;
    }

    header {
      padding: 1rem;
    }

    nav ul {
      display: none;
    }
  }
</style>