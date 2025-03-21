<!-- Sidebar.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';

  export let sidebarOpen = true;
  export let isMobile = false;
  export let games = [];
  export let isAuthenticated = false;
  export let cryptoBalances = {};

  const dispatch = createEventDispatcher();

  function selectGame(game) {
    dispatch('selectGame', game);
  }

  const menuCategories = [
    {
      id: 'casino',
      name: 'Casino Games',
      items: [
        { id: 'slots', name: 'Slots', icon: '🎰' },
        { id: 'blackjack', name: 'Blackjack', icon: '🃏' },
        { id: 'dice', name: 'Dice', icon: '🎲' },
        { id: 'roulette', name: 'Roulette', icon: '🎡' },
        { id: 'poker', name: 'Poker', icon: '♠️' }
      ]
    },
    {
      id: 'specials',
      name: 'Specials',
      items: [
        { id: 'hot', name: 'Hot Games', icon: '🔥' },
        { id: 'new', name: 'New Releases', icon: '⭐' },
        { id: 'tournaments', name: 'Tournaments', icon: '🏆' }
      ]
    },
    {
      id: 'account',
      name: 'Account',
      items: [
        { id: 'profile', name: 'Profile', icon: '👤' },
        { id: 'wallet', name: 'Wallet', icon: '💰' },
        { id: 'bonuses', name: 'Bonuses', icon: '🎁' },
        { id: 'statistics', name: 'Statistics', icon: '📊' }
      ]
    }
  ];

  let activeCategory = 'casino';
  let activeItem = 'slots';

  function setActive(categoryId, itemId) {
    activeCategory = categoryId;
    activeItem = itemId;
  }
</script>

<aside class="sidebar" class:open={sidebarOpen || !isMobile}>
  {#if isAuthenticated}
    <div class="user-wallet">
      <h3>Your Balance</h3>
      <div class="balance-list">
        {#each Object.entries(cryptoBalances) as [currency, amount]}
          <div class="balance-item">
            <span class="currency">{currency}</span>
            <span class="amount">{amount.toFixed(currency === 'BTC' ? 8 : 4)}</span>
          </div>
        {/each}
      </div>
      <div class="wallet-actions">
        <button class="btn btn-sm btn-primary">Deposit</button>
        <button class="btn btn-sm btn-outline">Withdraw</button>
      </div>
    </div>
  {/if}

  <div class="sidebar-menu">
    {#each menuCategories as category}
      <div class="menu-category">{category.name}</div>
      <ul>
        {#each category.items as item}
          <li>
            <a
              href="#{item.id}"
              class:active={activeCategory === category.id && activeItem === item.id}
              on:click|preventDefault={() => setActive(category.id, item.id)}
            >
              <span class="menu-icon">{item.icon}</span>
              {item.name}
            </a>
          </li>
        {/each}
      </ul>
    {/each}
  </div>

  {#if games.length > 0}
    <div class="featured-games">
      <div class="menu-category">Featured Games</div>
      <div class="game-shortcuts">
        {#each games.filter(g => g.featured).slice(0, 3) as game}
          <button
            class="game-shortcut"
            on:click={() => selectGame(game)}
          >
            <div class="game-icon">{game.name.charAt(0)}</div>
            <span>{game.name}</span>
          </button>
        {/each}
      </div>
    </div>
  {/if}
</aside>

<style>
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: var(--sidebar-width);
    height: 100%;
    background: var(--bg-darker);
    border-right: 1px solid rgba(108, 0, 255, 0.3);
    padding-top: 6rem;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 90;
    overflow-y: auto;
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .user-wallet {
    padding: 1.5rem 1rem;
    border-bottom: 1px solid rgba(108, 0, 255, 0.2);
  }

  .user-wallet h3 {
    font-size: 1rem;
    margin-bottom: 1rem;
    color: var(--text-dim);
  }

  .balance-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .balance-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(108, 0, 255, 0.1);
    padding: 0.5rem;
    border-radius: 4px;
  }

  .currency {
    font-weight: 600;
  }

  .amount {
    color: var(--secondary-color);
  }

  .wallet-actions {
    display: flex;
    gap: 0.5rem;
  }

  .btn-sm {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }

  .sidebar-menu {
    list-style: none;
    padding: 1rem;
  }

  .menu-category {
    font-size: 0.9rem;
    color: var(--text-dim);
    margin: 1.5rem 0 0.5rem 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .sidebar-menu li a {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.8rem 1rem;
    color: var(--text-light);
    text-decoration: none;
    transition: all 0.2s;
    border-radius: 4px;
  }

  .sidebar-menu li a:hover {
    background: rgba(108, 0, 255, 0.1);
    color: var(--secondary-color);
  }

  .sidebar-menu li a.active {
    background: linear-gradient(90deg, rgba(108, 0, 255, 0.2), transparent);
    border-left: 3px solid var(--primary-color);
  }

  .menu-icon {
    width: 1.5rem;
    height: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .featured-games {
    padding: 0 1rem 2rem;
  }

  .game-shortcuts {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .game-shortcut {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.8rem;
    background: rgba(108, 0, 255, 0.1);
    border: 1px solid rgba(108, 0, 255, 0.2);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
    color: var(--text-light);
  }

  .game-shortcut:hover {
    background: rgba(108, 0, 255, 0.2);
    transform: translateY(-2px);
  }

  .game-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }

  .game-shortcut span {
    font-size: 0.8rem;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
  }

  @media (min-width: 769px) {
    .sidebar {
      transform: translateX(0);
    }
  }
</style>