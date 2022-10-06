import java.util.ArrayDeque;
import java.util.concurrent.ThreadLocalRandom;

import java.awt.Graphics;
import java.awt.Canvas;
import java.awt.Color;
import javax.swing.JFrame;

import java.awt.event.KeyListener;
import java.awt.event.KeyEvent;

// Main class, initializes screen/window and runs game
public class Snake {
    public static void main(String[] args){
        JFrame frame = new JFrame("Snake");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        Window canvas = new Window();

        frame.add(canvas);
        frame.pack();
        frame.setVisible(true);
    }
}
// Generic helper Point2/Vector2 type class with builtin comparison functions  
class Point2 {
    public int x, y;

    public Point2(int x_, int y_){ x = x_; y = y_; }

    public Point2(Point2 p) { x = p.x; y = p.y; }

    public boolean isAt(int x_, int y_){
        return ( x == x_ ) & ( y == y_ );
    }
    public boolean isAt(Point2 p) {
        return ( x == p.x ) & ( y == p.y );
    }
}

// Main window class, executes game logic, takes input etc.
class Window extends Canvas implements KeyListener {

    // Initializing color palettes
    private static final Color DEFAULTsnakeHeadColor = new Color(200,0,0);
    private static final Color DEFAULTsnakeBodyColor = new Color(125,0,0);
    private static final Color DEFAULTfoodColor = new Color(0, 200, 0);

    private static final Color ALTsnakeHeadColor = new Color(255,255,255);
    private static final Color ALTsnakeBodyColor = new Color(230,230,230);
    private static final Color ALTfoodColor = new Color(200,0,0);

    private static final Color bgColor = Color.BLACK, borderColor = Color.WHITE;

    // Updates/paints per second of the game (unfortunately fixed 1:1)
    private static final int FPS = 5;

    // screen drawing general info
    public static final int scrWidth = 20, scrHeight = 20;
    public static final int pxWidth = 20;
    public static final int scrPxWidth = scrWidth*pxWidth, scrPxHeight = scrHeight*pxWidth;
    public static final int marginX = 20, marginY = 20;

    private static final int borderStroke = 2;
    private static final int borderWidth = 2*borderStroke + scrPxWidth;
    private static final int borderHeight = 2*borderStroke + scrPxHeight;

    // text spacing info
    private static final int scrTop = marginY + borderStroke;
    private static final int scrLeft = marginX + borderStroke;

    // direction consts
    private final Point2 RIGHT = new Point2(1,0);
    private final Point2 LEFT = new Point2(-1,0);
    private final Point2 UP = new Point2(0,-1);
    private final Point2 DOWN = new Point2(0,1);

    // Snake info
    private Color snakeHeadColor, snakeBodyColor, foodColor;
    private boolean isAlive, hasEaten;
    private ArrayDeque<Point2> snakeBody;
    private Point2 snakeHead, food, snakeDirection, snakeLastTravelledDirection;

    // Object Constructor
    public Window(){
        this.setSize( scrPxWidth + 2*scrLeft, scrPxHeight + 2*scrTop );
        this.setBackground(bgColor);

        addKeyListener(this);
        setFocusable(true);
        setFocusTraversalKeysEnabled(false);
        
        snakeHeadColor = DEFAULTsnakeHeadColor;
        snakeBodyColor = DEFAULTsnakeBodyColor;
        foodColor = DEFAULTfoodColor;

        initializeSnake();
    }

    // Initialize snake params (for start/restart)
    private void initializeSnake() {
        isAlive = true;
        hasEaten = false;

        snakeHead = new Point2( (int) scrWidth / 2 - 2, (int) scrHeight / 2);

        snakeBody = new ArrayDeque<>();
        for (int i=1; i<4; i++){
            addBodySegment(snakeHead.x - i, snakeHead.y);
        }

        snakeDirection = new Point2(1,0);
        snakeLastTravelledDirection = snakeDirection;

        food = new Point2(snakeHead.x + 3, snakeHead.y);
    }

    // Gets user score from snake size (for display)
    private int getScore(){
        return snakeBody.size() - 3;
    }

    // Helper, adds a body-segment (Point2) to our ArrayDeque
    private void addBodySegment(int x, int y) {
        snakeBody.add( new Point2(x, y) );
    }

    // (Sara, this is polymorphism)
    // Two versions of placeFood with different parameters -> different behaviors

    // Place food at given loc (no checks)
    private void placeFood( int x, int y ) {    
        food.x = x; food.y = y;
    }

    // Spawns food at a random unoccupied location using recursion
    private void placeFood(){ 
        int newFoodX = ThreadLocalRandom.current().nextInt(0, scrWidth);    // get random x/y candidate
        int newFoodY = ThreadLocalRandom.current().nextInt(0, scrHeight);   // for spawn loc

        if ( snakeHead.isAt(newFoodX, newFoodY) ) { placeFood(); }  // Check collision with head

        // check collision with body
        else for ( Point2 bodySegment : snakeBody ) if ( bodySegment.isAt(newFoodX, newFoodY) ){
            placeFood(); break;
        }

        // run overloaded function to place food in successful candidate loc
        placeFood(newFoodX, newFoodY);
    }

    // Updates game logic
    private void update(){ 
        if (!isAlive){  // no updates for dead snakes :(
            return;
        }

        hasEaten = false;   // Reset snake 'satiation' amount

        int newHeadX = (snakeHead.x + snakeDirection.x);    // get next head pos
        int newHeadY = (snakeHead.y + snakeDirection.y);

        // check wall collisions (H/V)
        if ((newHeadX < 0 | newHeadX == scrWidth) | (newHeadY < 0 | newHeadY == scrHeight)) {
            isAlive = false;
            return;
        }

        // Check head/body collisions with Point2.isAt(Point2 p)
        Point2 newHead = new Point2(newHeadX, newHeadY);
        for (Point2 b : snakeBody) {
            if (newHead.isAt(b)) {
                isAlive = false;
                return;
            }
        }

        if ( food.isAt(newHead) ) {         // Check for head/food intersect and reward snake/respawn food
            hasEaten = true; placeFood();
        }

        snakeBody.push( new Point2(snakeHead) );        // Add duplicate of old head to snake body
        if ( !hasEaten ) { snakeBody.removeLast(); }    // Remove last segment if snake hasn't eaten

        snakeHead = newHead;                            // Update head pos to next pos
        snakeLastTravelledDirection = snakeDirection;   // Update last travelled direction (input-bug prevention)

    }

    // Main loop function, handles painting logic and updates the board
    public void paint(Graphics g) { 

        // Update game logic and clear screen
        update();
        g.clearRect(0,0,scrPxWidth,marginY);

        // Write score
        g.setColor(borderColor);
        g.drawString("Score: " + Integer.toString(getScore()), marginX + 5, marginY - 4);

        // Draw border
        g.fillRect(marginX, marginY, borderWidth, borderHeight);
        g.setColor(bgColor);
        g.fillRect(scrLeft, scrTop, scrPxWidth, scrPxHeight);

        // Draw food
        g.setColor(foodColor);
        drawAtPx(g, food.x, food.y);

        // Draw snake
        g.setColor(snakeHeadColor);             // head
        drawAtPx(g, snakeHead.x, snakeHead.y);

        g.setColor(snakeBodyColor);             // body
        for ( Point2 bodySegment : snakeBody ){
            drawAtPx(g, bodySegment.x, bodySegment.y);
        }
    
        try { Thread.sleep((int) 1000/FPS); }
        catch (InterruptedException e) {}
        repaint();
    }

    // Helper to draw a macropixel (a "screen pixel") to the screen
    public void drawAtPx(Graphics g, int x, int y){ 
        int scrX = scrLeft + pxWidth * x;
        int scrY = scrTop + pxWidth * y;

        g.fillRect(scrX, scrY, pxWidth, pxWidth);
    }

    // Shell functions to appease abstract base class KeyListener
    public void keyReleased(KeyEvent e){}
    public void keyTyped(KeyEvent e){}

    // Handles keypress events with a switch/case
    public void keyPressed(KeyEvent e) { 
        int key = e.getKeyCode();

        switch (key) {
            case KeyEvent.VK_RIGHT: case KeyEvent.VK_D:         // Right Arrow / D to turn to right
                if (!snakeLastTravelledDirection.isAt(LEFT)) {
                    snakeDirection = RIGHT;
                }; break;

            case KeyEvent.VK_LEFT: case KeyEvent.VK_A:          // Left Arrow / A to turn to left
                if (!snakeLastTravelledDirection.isAt(RIGHT)) {
                    snakeDirection = LEFT;
                }; break;

            case KeyEvent.VK_UP: case KeyEvent.VK_W:            // Up Arrow / W to turn upwards
                if (!snakeLastTravelledDirection.isAt(DOWN)) {
                    snakeDirection = UP;
                }; break;

            case KeyEvent.VK_DOWN: case KeyEvent.VK_S:          // Down Arrow / S to turn downwards
                if (!snakeLastTravelledDirection.isAt(UP)) {
                    snakeDirection = DOWN;
                }; break;

            case KeyEvent.VK_C:             // C to change Color Scheme (red/green - white/red)
                if (snakeHeadColor == DEFAULTsnakeHeadColor) {  // switch to ALT scheme (white/red)
                    snakeHeadColor = ALTsnakeHeadColor;
                    snakeBodyColor = ALTsnakeBodyColor;
                    foodColor = ALTfoodColor;
                }
                else {                                          // switch to DEFAULT scheme (red/green)
                    snakeHeadColor = DEFAULTsnakeHeadColor;
                    snakeBodyColor = DEFAULTsnakeBodyColor;
                    foodColor = DEFAULTfoodColor;
                }
                break;

            case KeyEvent.VK_R:             // R to restart (checks if snake is dead)
                if (!isAlive) {
                    initializeSnake();
                }; break;

            case KeyEvent.VK_X:             // X to kill snake
                isAlive = false;
                break;

            case KeyEvent.VK_Q:             // Q to exit
                System.exit(0);

        }
    }

}
