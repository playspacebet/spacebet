// Blackjack.svelte
<script>
  import { onMount } from 'svelte';

  // Game state
  let deck = [];
  let playerHand = [];
  let dealerHand = [];
  let gameStatus = "waiting"; // waiting, playing, playerBust, dealerBust, playerWin, dealerWin, push
  let playerScore = 0;
  let dealerScore = 0;
  let playerCredits = 1000;
  let currentBet = 0;
  let message = "Welcome to Space Blackjack! Place your bet to begin.";
  let isDealing = false;
  let canDoubleDown = false;

  // Card values and suits
  const values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
  const suits = ["♠", "♥", "♦", "♣"];

  // Space themed card back image
  const cardBack = "https://cdn.pixabay.com/photo/2016/07/19/04/40/moon-1527501_640.jpg";

  // Initialize the game
  onMount(() => {
    initGame();
  });

  function initGame() {
    createDeck();
    shuffleDeck();
    resetHands();
    gameStatus = "waiting";
    canDoubleDown = false;
    message = "Welcome to Space Blackjack! Place your bet to begin.";
  }

  // Create a new deck of cards
  function createDeck() {
    deck = [];
    for (let suit of suits) {
      for (let value of values) {
        deck.push({
          value: value,
          suit: suit,
          numericValue: getCardValue(value),
          faceUp: true
        });
      }
    }
  }

  // Shuffle the deck
  function shuffleDeck() {
    for (let i = deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }
  }

  // Get card numeric value
  function getCardValue(value) {
    if (["J", "Q", "K"].includes(value)) return 10;
    if (value === "A") return 11;
    return parseInt(value);
  }

  // Deal a card from the deck
  function dealCard(faceUp = true) {
    if (deck.length === 0) {
      createDeck();
      shuffleDeck();
    }
    const card = deck.pop();
    card.faceUp = faceUp;
    return card;
  }

  // Reset hands
  function resetHands() {
    playerHand = [];
    dealerHand = [];
    playerScore = 0;
    dealerScore = 0;
  }

  // Calculate hand score
  function calculateScore(hand) {
    let score = 0;
    let aceCount = 0;

    for (let card of hand) {
      if (!card.faceUp) continue;
      score += card.numericValue;
      if (card.value === "A") aceCount++;
    }

    // Adjust for aces
    while (score > 21 && aceCount > 0) {
      score -= 10;
      aceCount--;
    }

    return score;
  }

  // Place bet and start the game
  function placeBet(amount) {
    if (gameStatus !== "waiting" || playerCredits < amount) return;

    currentBet = amount;
    playerCredits -= amount;
    startGame();
  }

  // Start a new game
  async function startGame() {
    isDealing = true;
    resetHands();

    // Deal initial cards
    playerHand.push(dealCard());
    await new Promise(resolve => setTimeout(resolve, 300));

    dealerHand.push(dealCard(false));
    await new Promise(resolve => setTimeout(resolve, 300));

    playerHand.push(dealCard());
    await new Promise(resolve => setTimeout(resolve, 300));

    dealerHand.push(dealCard());

    // Update scores
    playerScore = calculateScore(playerHand);
    dealerScore = calculateScore(dealerHand);

    // Check for blackjack
    if (playerScore === 21) {
      if (dealerScore === 21) {
        endGame("push");
      } else {
        endGame("playerBlackjack");
      }
    } else if (dealerScore === 21) {
      endGame("dealerBlackjack");
    } else {
      gameStatus = "playing";
      canDoubleDown = true;
      message = "Your move, space traveler.";
    }

    isDealing = false;
  }

  // Player hits (takes another card)
  async function hit() {
    if (gameStatus !== "playing" || isDealing) return;

    isDealing = true;
    canDoubleDown = false;

    playerHand.push(dealCard());
    playerScore = calculateScore(playerHand);

    await new Promise(resolve => setTimeout(resolve, 300));

    if (playerScore > 21) {
      endGame("playerBust");
    }

    isDealing = false;
  }

  // Player stands (ends turn)
  async function stand() {
    if (gameStatus !== "playing" || isDealing) return;

    isDealing = true;

    // Flip dealer's hidden card
    dealerHand[0].faceUp = true;
    dealerScore = calculateScore(dealerHand);

    await new Promise(resolve => setTimeout(resolve, 500));

    // Dealer draws until score is at least 17
    while (dealerScore < 17) {
      dealerHand.push(dealCard());
      dealerScore = calculateScore(dealerHand);
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Determine winner
    if (dealerScore > 21) {
      endGame("dealerBust");
    } else if (dealerScore > playerScore) {
      endGame("dealerWin");
    } else if (dealerScore < playerScore) {
      endGame("playerWin");
    } else {
      endGame("push");
    }

    isDealing = false;
  }

  // Double down
  async function doubleDown() {
    if (!canDoubleDown || gameStatus !== "playing" || isDealing || playerCredits < currentBet) return;

    isDealing = true;
    playerCredits -= currentBet;
    currentBet *= 2;

    // Player gets exactly one more card
    playerHand.push(dealCard());
    playerScore = calculateScore(playerHand);

    await new Promise(resolve => setTimeout(resolve, 500));

    if (playerScore > 21) {
      endGame("playerBust");
    } else {
      // Player's turn ends, dealer's turn begins
      await stand();
    }

    isDealing = false;
  }

  // End the game and determine outcome
  function endGame(result) {
    gameStatus = result;

    switch (result) {
      case "playerBlackjack":
        message = "COSMIC BLACKJACK! You win 3:2!";
        playerCredits += currentBet * 2.5;
        break;
      case "dealerBlackjack":
        message = "Dealer has blackjack. You lose your bet.";
        break;
      case "playerBust":
        message = "You went bust! Your ship crashed into a meteor.";
        break;
      case "dealerBust":
        message = "Dealer went bust! The aliens surrendered!";
        playerCredits += currentBet * 2;
        break;
      case "playerWin":
        message = "You win! Stars align in your favor!";
        playerCredits += currentBet * 2;
        break;
      case "dealerWin":
        message = "Dealer wins. Space is a harsh place.";
        break;
      case "push":
        message = "It's a tie! Gravitational balance restored.";
        playerCredits += currentBet;
        break;
    }

    currentBet = 0;
    setTimeout(() => {
      gameStatus = "waiting";
      message = "Place your bet for another cosmic journey.";
    }, 3000);
  }
</script>

<div class="space-blackjack">
  <div class="stars"></div>
  <div class="twinkling"></div>

  <header>
    <h1>COSMIC BLACKJACK</h1>
    <p class="subtitle">Take your chances in the vastness of space</p>
  </header>

  <div class="game-container">
    <div class="status-bar">
      <div class="credits">
        <span class="label">CREDITS:</span>
        <span class="value">{playerCredits}</span>
      </div>
      <div class="message">
        <span>{message}</span>
      </div>
      <div class="current-bet">
        <span class="label">BET:</span>
        <span class="value">{currentBet}</span>
      </div>
    </div>

    <div class="dealer-area">
      <h2>Alien Dealer <span class="score">{dealerHand[0]?.faceUp ? dealerScore : '??'}</span></h2>
      <div class="cards">
        {#each dealerHand as card, i}
          <div class="card {card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'} {!card.faceUp ? 'back' : ''}"
               style="transform: translateX({i * 30}px) rotate({-5 + i * 2}deg);">
            {#if card.faceUp}
              <div class="card-inner">
                <div class="card-top">
                  <span class="value">{card.value}</span>
                  <span class="suit">{card.suit}</span>
                </div>
                <div class="card-center">
                  <span class="big-suit">{card.suit}</span>
                </div>
                <div class="card-bottom">
                  <span class="value">{card.value}</span>
                  <span class="suit">{card.suit}</span>
                </div>
              </div>
            {:else}
              <div class="card-back">
                <div class="space-design"></div>
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>

    <div class="player-area">
      <h2>Space Explorer <span class="score">{playerScore}</span></h2>
      <div class="cards">
        {#each playerHand as card, i}
          <div class="card {card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'}"
               style="transform: translateX({i * 30}px) rotate({-5 + i * 2}deg);">
            <div class="card-inner">
              <div class="card-top">
                <span class="value">{card.value}</span>
                <span class="suit">{card.suit}</span>
              </div>
              <div class="card-center">
                <span class="big-suit">{card.suit}</span>
              </div>
              <div class="card-bottom">
                <span class="value">{card.value}</span>
                <span class="suit">{card.suit}</span>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <div class="controls">
      {#if gameStatus === "waiting"}
        <div class="bet-controls">
          <button class="bet-btn" on:click={() => placeBet(10)}>Bet 10</button>
          <button class="bet-btn" on:click={() => placeBet(25)}>Bet 25</button>
          <button class="bet-btn" on:click={() => placeBet(50)}>Bet 50</button>
          <button class="bet-btn" on:click={() => placeBet(100)}>Bet 100</button>
        </div>
      {:else if gameStatus === "playing"}
        <div class="action-controls">
          <button class="action-btn hit" on:click={hit} disabled={isDealing}>Hit</button>
          <button class="action-btn stand" on:click={stand} disabled={isDealing}>Stand</button>
          <button class="action-btn double" on:click={doubleDown} disabled={!canDoubleDown || isDealing || playerCredits < currentBet}>Double Down</button>
        </div>
      {:else}
        <button class="new-game-btn" on:click={initGame}>New Game</button>
      {/if}
    </div>
  </div>
</div>

<style>
  /* Space theme and animations */
  .space-blackjack {
    position: relative;
    min-height: 100vh;
    overflow: hidden;
    color: white;
    font-family: 'Orbitron', 'Arial', sans-serif;
  }

  .stars, .twinkling {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .stars {
    background: #000 url('https://i.imgur.com/YKY28eT.png') repeat top center;
    z-index: -2;
  }

  .twinkling {
    background: transparent url('https://i.imgur.com/XYMF4ca.png') repeat top center;
    z-index: -1;
    animation: move-twinks 200s linear infinite;
  }

  @keyframes move-twinks {
    from {background-position: 0 0;}
    to {background-position: -10000px 5000px;}
  }

  /* Layout and styling */
  header {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
    border-bottom: 2px solid rgba(77, 155, 230, 0.5);
  }

  h1 {
    font-size: 2.5rem;
    letter-spacing: 3px;
    color: #4d9be6;
    text-shadow: 0 0 10px rgba(77, 155, 230, 0.7), 0 0 20px rgba(77, 155, 230, 0.5);
    margin: 0;
  }

  .subtitle {
    color: #a3c9ed;
    font-style: italic;
    margin-top: 5px;
  }

  .game-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 15px;
    background-color: rgba(15, 23, 42, 0.8);
    box-shadow: 0 0 20px rgba(77, 155, 230, 0.3);
    backdrop-filter: blur(5px);
  }

  .status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 8px;
    background-color: rgba(30, 41, 59, 0.7);
  }

  .label {
    color: #a3c9ed;
    margin-right: 5px;
  }

  .value {
    font-weight: bold;
    color: #4d9be6;
  }

  .message {
    text-align: center;
    font-size: 1.1rem;
    color: #e2e8f0;
    flex-grow: 1;
    padding: 0 15px;
  }

  .dealer-area, .player-area {
    margin-bottom: 30px;
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(30, 41, 59, 0.5);
  }

  h2 {
    color: #a3c9ed;
    font-size: 1.3rem;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .score {
    color: #4d9be6;
    font-size: 1.5rem;
    background-color: rgba(15, 23, 42, 0.7);
    padding: 5px 10px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(77, 155, 230, 0.3);
  }

  .cards {
    position: relative;
    height: 150px;
    margin-bottom: 10px;
  }

  .card {
    position: absolute;
    width: 100px;
    height: 140px;
    perspective: 600px;
    transition: transform 0.3s ease;
  }

  .card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 10px;
    background-color: #f8fafc;
    display: flex;
    flex-direction: column;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 10px rgba(77, 155, 230, 0.3);
    overflow: hidden;
  }

  .card.back .card-back {
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 10px;
    background-color: #1e293b;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 10px rgba(77, 155, 230, 0.3);
  }

  .card-back .space-design {
    width: 90%;
    height: 90%;
    border-radius: 8px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    position: relative;
    overflow: hidden;
  }

  .card-back .space-design::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at center, transparent 0%, #0f172a 90%);
    background-size: 5px 5px;
    opacity: 0.5;
  }

  .card.red {
    color: #ef4444;
  }

  .card.black {
    color: #1e293b;
  }

  .card-top, .card-bottom {
    display: flex;
    padding: 5px;
    font-size: 1rem;
    font-weight: bold;
  }

  .card-bottom {
    flex-direction: row-reverse;
    justify-content: space-between;
    margin-top: auto;
  }

  .card-center {
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .big-suit {
    font-size: 3rem;
  }

  .controls {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    gap: 10px;
  }

  button {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    font-family: 'Orbitron', 'Arial', sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s ease;
    margin: 0 5px;
  }

  .bet-btn {
    background-color: #334155;
    color: #a3c9ed;
    box-shadow: 0 0 10px rgba(51, 65, 85, 0.5);
  }

  .bet-btn:hover {
    background-color: #475569;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(51, 65, 85, 0.7);
  }

  .action-btn {
    min-width: 100px;
    font-size: 1rem;
    letter-spacing: 1px;
  }

  .hit {
    background-color: #4d9be6;
    color: #f8fafc;
    box-shadow: 0 0 10px rgba(77, 155, 230, 0.5);
  }

  .hit:hover {
    background-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(77, 155, 230, 0.7);
  }

  .stand {
    background-color: #ef4444;
    color: #f8fafc;
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
  }

  .stand:hover {
    background-color: #dc2626;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(239, 68, 68, 0.7);
  }

  .double {
    background-color: #10b981;
    color: #f8fafc;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
  }

  .double:hover {
    background-color: #059669;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(16, 185, 129, 0.7);
  }

  .new-game-btn {
    background-color: #8b5cf6;
    color: #f8fafc;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
    padding: 12px 25px;
    font-size: 1.1rem;
  }

  .new-game-btn:hover {
    background-color: #7c3aed;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(139, 92, 246, 0.7);
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  @media (max-width: 768px) {
    .game-container {
      padding: 10px;
    }

    .card {
      width: 80px;
      height: 112px;
    }

    .big-suit {
      font-size: 2rem;
    }

    .controls {
      flex-wrap: wrap;
    }

    button {
      margin: 5px;
      padding: 8px 12px;
      font-size: 0.9rem;
    }
  }
</style>