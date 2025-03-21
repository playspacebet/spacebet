// Poker.svelte
<script>
  import { onMount } from 'svelte';

  // Game state
  let deck = [];
  let playerHand = [];
  let computerHand = [];
  let communityCards = [];
  let gameStatus = "waiting"; // waiting, preFlop, flop, turn, river, showdown
  let playerCredits = 1000;
  let computerCredits = 1000;
  let pot = 0;
  let currentBet = 0;
  let computerBet = 0;
  let minBet = 10;
  let message = "Welcome to Galactic Poker! Place your ante to begin.";
  let isDealing = false;
  let playerHandRank = "";
  let computerHandRank = "";
  let winner = null;

  // Card values and suits with space theme
  const values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
  const suits = ["♠", "♥", "♦", "♣"];
  const suitEmojis = {
    "♠": "🪐", // planet
    "♥": "🚀", // rocket
    "♦": "⭐", // star
    "♣": "👽"  // alien
  };

  // Hand ranking descriptions
  const handDescriptions = {
    "High Card": "Just a high card. The weakest hand.",
    "Pair": "Two cards of the same value.",
    "Two Pair": "Two different pairs of cards.",
    "Three of a Kind": "Three cards of the same value.",
    "Straight": "Five cards in sequential order.",
    "Flush": "Five cards of the same suit.",
    "Full House": "Three of a kind plus a pair.",
    "Four of a Kind": "Four cards of the same value.",
    "Straight Flush": "Five sequential cards of the same suit.",
    "Royal Flush": "A, K, Q, J, 10 of the same suit. The ultimate hand!"
  };

  onMount(() => {
    initGame();
  });

  function initGame() {
    createDeck();
    shuffleDeck();
    resetHands();
    gameStatus = "waiting";
    pot = 0;
    currentBet = 0;
    computerBet = 0;
    winner = null;
    message = "Welcome to Galactic Poker! Place your ante to begin.";
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
    if (value === "A") return 14;
    if (value === "K") return 13;
    if (value === "Q") return 12;
    if (value === "J") return 11;
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

  // Reset hands and community cards
  function resetHands() {
    playerHand = [];
    computerHand = [];
    communityCards = [];
    playerHandRank = "";
    computerHandRank = "";
  }

  // Place ante and start the game
  function placeAnte(amount) {
    if (gameStatus !== "waiting" || playerCredits < amount) return;

    currentBet = amount;
    playerCredits -= amount;

    // Computer matches the ante
    computerBet = amount;
    computerCredits -= amount;

    pot = amount * 2;
    startGame();
  }

  // Start a new game
  async function startGame() {
    isDealing = true;
    resetHands();

    // Deal player cards
    playerHand.push(dealCard());
    await new Promise(resolve => setTimeout(resolve, 300));
    playerHand.push(dealCard());
    await new Promise(resolve => setTimeout(resolve, 300));

    // Deal computer cards (face down)
    computerHand.push(dealCard(false));
    await new Promise(resolve => setTimeout(resolve, 300));
    computerHand.push(dealCard(false));

    evaluateHands();

    gameStatus = "preFlop";
    message = "Pre-flop round. Choose your action.";
    isDealing = false;
  }

  // Evaluate both hands
  function evaluateHands() {
    if (playerHand.length < 2) return;

    const playerCards = [...playerHand, ...communityCards];
    const playerResult = getHandRank(playerCards);
    playerHandRank = playerResult.name;

    // Also evaluate computer's hand (but don't show yet)
    if (gameStatus !== "waiting") {
      const computerCards = [...computerHand, ...communityCards];
      const computerResult = getHandRank(computerCards);
      computerHandRank = computerResult.name;
    }
  }

  // Player checks (no additional bet)
  function check() {
    if (gameStatus === "waiting" || isDealing) return;

    message = "You check. Computer's turn...";
    computerAction();
  }

  // Player bets
  function bet(amount) {
    if (gameStatus === "waiting" || isDealing || playerCredits < amount) return;

    playerCredits -= amount;
    currentBet = amount;
    pot += amount;

    message = `You bet ${amount} credits. Computer's turn...`;
    computerAction();
  }

  // Player folds
  function fold() {
    if (gameStatus === "waiting" || isDealing) return;

    message = "You fold. The computer wins the pot.";
    computerCredits += pot;
    pot = 0;
    gameStatus = "waiting";

    setTimeout(() => {
      initGame();
    }, 3000);
  }

  // Computer's action
  async function computerAction() {
    if (isDealing) return;
    isDealing = true;

    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simple AI for computer actions
    const actionRoll = Math.random();

    if (gameStatus === "river") {
      // On the river, computer is more likely to call
      if (actionRoll < 0.7 || computerHandRank !== "High Card") {
        computerCall();
      } else {
        computerFold();
      }
    } else {
      // Computer decides based on its hand and randomness
      if (actionRoll < 0.2) {
        // Computer folds occasionally
        computerFold();
      } else if (actionRoll < 0.6) {
        // Computer calls
        computerCall();
      } else {
        // Computer raises
        const raiseAmount = Math.min(
          [10, 20, 50][Math.floor(Math.random() * 3)],
          computerCredits
        );
        computerRaise(raiseAmount);
      }
    }

    isDealing = false;
  }

  // Computer calls
  function computerCall() {
    if (currentBet > 0) {
      const callAmount = Math.min(currentBet, computerCredits);
      computerCredits -= callAmount;
      computerBet = callAmount;
      pot += callAmount;
      message = `Computer calls ${callAmount} credits.`;
    } else {
      message = "Computer checks.";
    }

    // Move to next street
    dealNextStreet();
  }

  // Computer raises
  function computerRaise(amount) {
    computerCredits -= amount;
    computerBet = amount;
    pot += amount;
    message = `Computer raises ${amount} credits. Do you call?`;

    // Player must now call or fold
    currentBet = 0;
  }

  // Computer folds
  function computerFold() {
    message = "Computer folds. You win the pot!";
    playerCredits += pot;
    pot = 0;
    gameStatus = "waiting";

    setTimeout(() => {
      initGame();
    }, 3000);
  }

  // Player calls computer's bet
  function call() {
    if (computerBet <= 0 || playerCredits < computerBet) return;

    playerCredits -= computerBet;
    pot += computerBet;
    message = `You call ${computerBet} credits.`;
    currentBet = 0;
    computerBet = 0;

    // Move to next street
    dealNextStreet();
  }

  // Deal the next round of community cards
  async function dealNextStreet() {
    isDealing = true;

    await new Promise(resolve => setTimeout(resolve, 800));

    switch (gameStatus) {
      case "preFlop":
        // Deal the flop (3 community cards)
        communityCards.push(dealCard());
        await new Promise(resolve => setTimeout(resolve, 300));
        communityCards.push(dealCard());
        await new Promise(resolve => setTimeout(resolve, 300));
        communityCards.push(dealCard());

        gameStatus = "flop";
        message = "The flop is dealt. Choose your action.";
        break;

      case "flop":
        // Deal the turn (4th community card)
        communityCards.push(dealCard());

        gameStatus = "turn";
        message = "The turn is dealt. Choose your action.";
        break;

      case "turn":
        // Deal the river (5th community card)
        communityCards.push(dealCard());

        gameStatus = "river";
        message = "The river is dealt. Final betting round.";
        break;

      case "river":
        // Move to showdown
        determineWinner();
        break;
    }

    // Evaluate hands after each street
    evaluateHands();

    isDealing = false;
  }

  // Determine the winner at showdown
  function determineWinner() {
    // Flip computer's cards face up
    computerHand.forEach(card => card.faceUp = true);

    const playerResult = getHandRank([...playerHand, ...communityCards]);
    const computerResult = getHandRank([...computerHand, ...communityCards]);

    playerHandRank = playerResult.name;
    computerHandRank = computerResult.name;

    const playerRank = getHandRankValue(playerResult.name);
    const computerRank = getHandRankValue(computerResult.name);

    if (playerRank > computerRank) {
      winner = "player";
      message = `You win with ${playerHandRank}! Collecting ${pot} credits.`;
      playerCredits += pot;
    } else if (playerRank < computerRank) {
      winner = "computer";
      message = `Computer wins with ${computerHandRank}. You lose.`;
      computerCredits += pot;
    } else {
      // Same hand rank, compare high cards
      if (playerResult.highCard > computerResult.highCard) {
        winner = "player";
        message = `You win with ${playerHandRank} (high card ${values[playerResult.highCard - 2]})! Collecting ${pot} credits.`;
        playerCredits += pot;
      } else if (playerResult.highCard < computerResult.highCard) {
        winner = "computer";
        message = `Computer wins with ${computerHandRank} (high card ${values[computerResult.highCard - 2]}). You lose.`;
        computerCredits += pot;
      } else {
        // It's a tie
        winner = "tie";
        message = "It's a tie! Splitting the pot.";
        const halfPot = Math.floor(pot / 2);
        playerCredits += halfPot;
        computerCredits += pot - halfPot;
      }
    }

    pot = 0;
    gameStatus = "showdown";

    // Start a new game after 5 seconds
    setTimeout(() => {
      initGame();
    }, 5000);
  }

  // Calculate hand rank
  function getHandRank(cards) {
    // Need at least 5 cards for a poker hand
    if (cards.length < 5) {
      return { name: "Incomplete Hand", highCard: getHighestCard(cards) };
    }

    // Count frequencies of each value
    const valueCounts = {};
    const suitCounts = {};

    for (const card of cards) {
      valueCounts[card.numericValue] = (valueCounts[card.numericValue] || 0) + 1;
      suitCounts[card.suit] = (suitCounts[card.suit] || 0) + 1;
    }

    const values = Object.keys(valueCounts).map(Number).sort((a, b) => b - a);
    const highCard = values[0];

    // Check for a flush (all same suit)
    const isFlush = Object.values(suitCounts).some(count => count >= 5);

    // Check for a straight (5 consecutive values)
    let isStraight = false;
    let straightHighCard = 0;

    // Handle Ace low straight (A-2-3-4-5)
    if (values.includes(14) && values.includes(2) && values.includes(3) &&
        values.includes(4) && values.includes(5)) {
      isStraight = true;
      straightHighCard = 5; // 5 is high card in A-2-3-4-5 straight
    } else {
      // Check normal straights
      const sortedValues = [...new Set(values)].sort((a, b) => a - b);
      for (let i = 0; i <= sortedValues.length - 5; i++) {
        const slice = sortedValues.slice(i, i + 5);
        if (slice[4] - slice[0] === 4) {
          isStraight = true;
          straightHighCard = slice[4];
          break;
        }
      }
    }

    // Count pairs, trips, quads
    const pairs = values.filter(v => valueCounts[v] === 2);
    const trips = values.filter(v => valueCounts[v] === 3);
    const quads = values.filter(v => valueCounts[v] === 4);

    // Check from highest to lowest hand

    // Royal Flush: A-K-Q-J-10 of same suit
    if (isStraight && isFlush && values.includes(14) && straightHighCard === 14) {
      return { name: "Royal Flush", highCard: 14 };
    }

    // Straight Flush: 5 consecutive cards of same suit
    if (isStraight && isFlush) {
      return { name: "Straight Flush", highCard: straightHighCard };
    }

    // Four of a Kind: 4 cards of same value
    if (quads.length > 0) {
      return { name: "Four of a Kind", highCard: quads[0] };
    }

    // Full House: 3 cards of one value and 2 of another
    if (trips.length > 0 && pairs.length > 0) {
      return { name: "Full House", highCard: trips[0] };
    }

    // Flush: 5 cards of same suit
    if (isFlush) {
      return { name: "Flush", highCard: highCard };
    }

    // Straight: 5 consecutive cards
    if (isStraight) {
      return { name: "Straight", highCard: straightHighCard };
    }

    // Three of a Kind: 3 cards of same value
    if (trips.length > 0) {
      return { name: "Three of a Kind", highCard: trips[0] };
    }

    // Two Pair: 2 different pairs
    if (pairs.length >= 2) {
      return { name: "Two Pair", highCard: pairs[0] };
    }

    // Pair: 2 cards of same value
    if (pairs.length === 1) {
      return { name: "Pair", highCard: pairs[0] };
    }

    // High Card: highest value card
    return { name: "High Card", highCard: highCard };
  }

  // Get the highest card value from a hand
  function getHighestCard(cards) {
    return Math.max(...cards.map(card => card.numericValue));
  }

  // Get numeric value for hand ranking
  function getHandRankValue(handName) {
    const ranks = [
      "High Card",
      "Pair",
      "Two Pair",
      "Three of a Kind",
      "Straight",
      "Flush",
      "Full House",
      "Four of a Kind",
      "Straight Flush",
      "Royal Flush"
    ];

    return ranks.indexOf(handName);
  }
</script>

<div class="space-poker">
  <div class="stars"></div>
  <div class="twinkling"></div>
  <div class="planets"></div>

  <header>
    <h1>GALACTIC POKER</h1>
    <p class="subtitle">Five Card Challenge in Deep Space</p>
  </header>

  <div class="game-container">
    <div class="status-bar">
      <div class="credits player-credits">
        <span class="label">YOUR CREDITS:</span>
        <span class="value">{playerCredits}</span>
      </div>
      <div class="pot">
        <span class="label">POT:</span>
        <span class="value">{pot}</span>
      </div>
      <div class="credits computer-credits">
        <span class="label">ALIEN CREDITS:</span>
        <span class="value">{computerCredits}</span>
      </div>
    </div>

    <div class="message-area">
      <div class="message">{message}</div>
      {#if playerHandRank}
        <div class="hand-rank">Your hand: <span class="rank">{playerHandRank}</span></div>
      {/if}
    </div>

    <div class="computer-area">
      <h2>Alien Opponent</h2>
      <div class="cards">
        {#each computerHand as card, i}
          <div class="card {card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'} {!card.faceUp ? 'back' : ''}"
               style="transform: translateX({i * 30}px) rotate({-5 + i * 2}deg);">
            {#if card.faceUp}
              <div class="card-inner">
                <div class="card-top">
                  <span class="value">{card.value}</span>
                  <span class="suit">{suitEmojis[card.suit]}</span>
                </div>
                <div class="card-center">
                  <span class="big-suit">{suitEmojis[card.suit]}</span>
                </div>
                <div class="card-bottom">
                  <span class="value">{card.value}</span>
                  <span class="suit">{suitEmojis[card.suit]}</span>
                </div>
              </div>
            {:else}
              <div class="card-back">
                <div class="space-design"></div>
              </div>
            {/if}
          </div>
        {/each}

        {#if gameStatus === "showdown" && computerHandRank}
          <div class="computer-hand-rank">
            <span class="rank">{computerHandRank}</span>
          </div>
        {/if}
      </div>
    </div>

    <div class="community-area">
      <h2>Nebula Cards</h2>
      <div class="cards">
        {#each communityCards as card, i}
          <div class="card {card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'}"
               style="transform: translateX({i * 50 - 100}px) rotate({-2 + i}deg);">
            <div class="card-inner">
              <div class="card-top">
                <span class="value">{card.value}</span>
                <span class="suit">{suitEmojis[card.suit]}</span>
              </div>
              <div class="card-center">
                <span class="big-suit">{suitEmojis[card.suit]}</span>
              </div>
              <div class="card-bottom">
                <span class="value">{card.value}</span>
                <span class="suit">{suitEmojis[card.suit]}</span>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <div class="player-area">
      <h2>Space Explorer</h2>
      <div class="cards">
        {#each playerHand as card, i}
          <div class="card {card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'}"
               style="transform: translateX({i * 30}px) rotate({-5 + i * 2}deg);">
            <div class="card-inner">
              <div class="card-top">
                <span class="value">{card.value}</span>
                <span class="suit">{suitEmojis[card.suit]}</span>
              </div>
              <div class="card-center">
                <span class="big-suit">{suitEmojis[card.suit]}</span>
              </div>
              <div class="card-bottom">
                <span class="value">{card.value}</span>
                <span class="suit">{suitEmojis[card.suit]}</span>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <div class="controls">
      {#if gameStatus === "waiting"}
        <div class="bet-controls">
          <button class="bet-btn" on:click={() => placeAnte(10)} disabled={playerCredits < 10}>Ante 10</button>
          <button class="bet-btn" on:click={() => placeAnte(20)} disabled={playerCredits < 20}>Ante 20</button>
          <button class="bet-btn" on:click={() => placeAnte(50)} disabled={playerCredits < 50}>Ante 50</button>
        </div>
      {:else if gameStatus !== "showdown"}
        {#if computerBet > 0}
          <div class="action-controls">
            <button class="action-btn call" on:click={call} disabled={isDealing || playerCredits < computerBet}>
              Call {computerBet}
            </button>
            <button class="action-btn fold" on:click={fold} disabled={isDealing}>
              Fold
            </button>
          </div>
        {:else}
          <div class="action-controls">
            <button class="action-btn check" on:click={check} disabled={isDealing}>
              Check
            </button>
            <button class="action-btn bet" on:click={() => bet(10)} disabled={isDealing || playerCredits < 10}>
              Bet 10
            </button>
            <button class="action-btn bet" on:click={() => bet(20)} disabled={isDealing || playerCredits < 20}>
              Bet 20
            </button>
            <button class="action-btn bet" on:click={() => bet(50)} disabled={isDealing || playerCredits < 50}>
              Bet 50
            </button>
            <button class="action-btn fold" on:click={fold} disabled={isDealing}>
              Fold
            </button>
          </div>
        {/if}
      {:else}
        <div class="result-message">
          {#if winner === "player"}
            <div class="winner player-win">You Win!</div>
          {:else if winner === "computer"}
            <div class="winner computer-win">Computer Wins!</div>
          {:else}
            <div class="winner tie">It's a Tie!</div>
          {/if}
        </div>
      {/if}
    </div>

    <div class="help-section">
      <button class="help-toggle">Hand Rankings</button>
      <div class="hand-rankings">
        <h3>Poker Hand Rankings</h3>
        <ul>
          <li><strong>Royal Flush:</strong> A, K, Q, J, 10 of the same suit</li>
          <li><strong>Straight Flush:</strong> Five sequential cards of the same suit</li>
          <li><strong>Four of a Kind:</strong> Four cards of the same value</li>
          <li><strong>Full House:</strong> Three of a kind plus a pair</li>
          <li><strong>Flush:</strong> Five cards of the same suit</li>
          <li><strong>Straight:</strong> Five sequential cards</li>
          <li><strong>Three of a Kind:</strong> Three cards of the same value</li>
          <li><strong>Two Pair:</strong> Two pairs of different values</li>
          <li><strong>Pair:</strong> Two cards of the same value</li>
          <li><strong>High Card:</strong> Highest value card when no other hand is made</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<style>
  /* Space theme and animations */
  .space-poker {
    position: relative;
    min-height: 100vh;
    overflow: hidden;
    color: white;
    font-family: 'Orbitron', 'Arial', sans-serif;
  }

  .stars, .twinkling, .planets {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .stars {
    background: #000 url('https://i.imgur.com/YKY28eT.png') repeat top center;
    z-index: -3;
  }

  .twinkling {
    background: transparent url('https://i.imgur.com/XYMF4ca.png') repeat top center;
    z-index: -2;
    animation: move-twinks 200s linear infinite;
  }

  .planets {
    background: transparent url('https://i.imgur.com/2aAT2g3.png') repeat top center;
    z-index: -1;
    animation: move-planets 400s linear infinite;
  }

  @keyframes move-twinks {
    from {background-position: 0 0;}
    to {background-position: -10000px 5000px;}
  }

  @keyframes move-planets {
    from {background-position: 0 0;}
    to {background-position: -1000px 500px;}
  }

  /* Layout and styling */
  header {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
    border-bottom: 2px solid rgba(138, 43, 226, 0.5);
  }

  h1 {
    font-size: 2.5rem;
    letter-spacing: 3px;
    color: #8a2be2;
    text-shadow: 0 0 10px rgba(138, 43, 226, 0.7), 0 0 20px rgba(138, 43, 226, 0.5);
    margin: 0;
  }

  .subtitle {
    color: #b19cd9;
    font-style: italic;
    margin-top: 5px;
  }

  .game-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 15px;
    background-color: rgba(15, 23, 42, 0.8);
    box-shadow: 0 0 20px rgba(138, 43, 226, 0.3);
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

  .pot {
    background-color: rgba(138, 43, 226, 0.3);
    padding: 10px 15px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(138, 43, 226, 0.5);
  }

  .label {
    color: #b19cd9;
    margin-right: 5px;
  }

  .value {
    font-weight: bold;
    color: #8a2be2;
  }

  .message-area {
    text-align: center;
    margin-bottom: 20px;
    padding: 15px;
    border-radius: 8px;
    background-color: rgba(30, 41, 59, 0.5);
  }

  .message {
    font-size: 1.2rem;
    color: #e2e8f0;
    margin-bottom: 10px;
  }

  .hand-rank {
    font-size: 1rem;
    color: #b19cd9;
  }

  .rank {
    color: #8a2be2;
    font-weight: bold;
  }

  .computer-area, .community-area, .player-area {
    margin-bottom: 30px;
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(30, 41, 59, 0.5);
  }

  .community-area {
    text-align: center;
  }

  h2 {
    color: #b19cd9;
    font-size: 1.3rem;
    margin-bottom: 15px;
  }

  .cards {
    position: relative;
    height: 150px;
    margin-bottom: 10px;
  }

  .community-area .cards {
    height: 150px;
  }

  .card {
    position: absolute;
    width: 100px;
    height: 140px;
    perspective: 600px