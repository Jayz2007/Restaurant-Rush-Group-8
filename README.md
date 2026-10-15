# Restaurant Rush — Group 8

A small restaurant management game made with **Python and Pygame** for the Python Game Development Midterm Lab Exam.

## Objective
Serve customer orders before they become impatient. Select an order, prepare its meal using available ingredients, then serve it to earn points. A shift lasts 90 seconds. Customers can leave if they wait too long, lowering satisfaction.

## Requirements
- Python 3.10 or newer
- Pygame 2.5 or newer

## Setup and launch

### Windows
1. Install Python from https://www.python.org/downloads/
2. Open Command Prompt in this project folder.
3. Install Pygame:
   ```bash
   py -m pip install -r requirements.txt
   ```
4. Launch:
   ```bash
   py main.py
   ```

### macOS / Linux
```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

## Beginner step-by-step guide

1. Download `Restaurant_Rush_Group8.zip`.
2. Right-click the ZIP and choose **Extract All**.
3. Open Visual Studio Code.
4. Select **File → Open Folder** and choose the extracted `Restaurant_Rush_Group8` folder.
5. Open **Terminal → New Terminal** in VS Code.
6. Install the dependency:
   ```bash
   python -m pip install -r requirements.txt
   ```
   If `python` is not recognized on Windows, try:
   ```bash
   py -m pip install -r requirements.txt
   ```
7. Run the game:
   ```bash
   python main.py
   ```
   On Windows, if needed, use `py main.py`.
8. Click **Start Shift**, click an order card, choose **Prepare Meal**, then **Serve Customer**.
9. Test **Rank Wait Time**, **Quick Order**, and **Recipe Guide**.
10. If an error appears, copy the full error message from the terminal so you can troubleshoot it.

## Controls
- Click **Start Shift** to begin.
- Click an order card to select it.
- Click **Prepare Meal** to check and use the required ingredients.
- Click **Serve Customer** after preparation to earn points and tips.
- **Rank Wait Time** runs Bubble Sort to rank longest-waiting orders first.
- **Quick Order** uses Selection Sort to select the order with the shortest preparation time.
- **Recipe Guide** displays recipes, including the nested Combo Meal.
- Press **B** to rank waiting time and **S** to select the shortest-preparation order.
- Press **Esc** to quit (or return from the recipe guide).

## Required course concepts feature map

| Concept | Where it appears | How it affects gameplay |
|---|---|---|
| Bubble Sort | `bubble_sort_by_wait()` and `sort_by_wait()` | The Rank Wait Time button ranks active orders by longest waiting time. |
| Insertion Sort | `insertion_sort_by_wait()` and `spawn_order()` | New customer orders are inserted into the wait-time-ordered list. |
| Selection Sort | `selection_sort_by_prep()` and `choose_shortest_prep()` | Quick Order selects the active order with the shortest preparation time. |
| Tuple | `TABLE_POSITIONS` and each order's `table` field | Fixed table coordinates and table assignment are stored as tuples. |
| Set | `AVAILABLE_INGREDIENTS` | Ingredient membership is checked before meal preparation; sets keep unique names. |
| Dictionary | `RECIPES`, `MENU`, `INGREDIENT_STOCK`, and order dictionaries | Stores recipes, menu prices, prep times, stock, and live order data. |
| Recursion | `expand_recipe()` | Recursively expands nested recipes, such as Combo Meal into Burger, Fries, and Soda ingredients. Base case: a component is not another recipe, so it is counted as a base ingredient. |

## Testing checklist
- [ ] Launches without errors.
- [ ] Start Shift begins a 90-second round.
- [ ] Clicking an order selects it.
- [ ] Preparing an order reduces the appropriate ingredient stock.
- [ ] Serving a prepared order increases score and served count.
- [ ] An unprepared order cannot be served.
- [ ] Bubble Sort and Selection Sort buttons give visible feedback.
- [ ] Recipe Guide shows expanded ingredient lists.
- [ ] Shift ends when time runs out or satisfaction reaches zero.
- [ ] Play Again restarts the game.
- [ ] Sorting functions are tested with empty, one-item, and multiple-item lists.

## Team / individual contribution
The exam guide recommends a five-role team, but this project is being prepared by one student. The solo developer can cover all five responsibility areas:
1. **Coordinator/integrator:** organize files and test the complete game.
2. **Gameplay programmer:** orders, timer, score, customer satisfaction, and game ending.
3. **Algorithms/data programmer:** the three sorting algorithms, set, dictionaries, tuples, and recursion.
4. **Interface designer:** Pygame screens, panels, buttons, and visual feedback.
5. **QA/documentation/release:** test the game, maintain this README, and upload the runnable source to GitHub.

For the individual defense, be ready to explain the functions in the feature map and demonstrate each button in a live game.

## GitHub submission
Create a repository named `restaurant-rush-group8` and upload:
- `main.py`
- `requirements.txt`
- `README.md`

Make meaningful commits as you implement and test features. Do not upload only screenshots or a video; the source code must be included.
