#include <vector>
#include <ncurses.h>
#include <unistd.h>
#include <string>
#include <stdio.h>

using namespace std;

#define COLOR_LIGHTRED 9
#define COLOR_APPLEGREEN 46
#define COLOR_APPLERED 196
#define BW_COLORS 5

bool gameOver = false;
bool alive;

const int width =20;
const int height =20;

int score, hs, timer;
int tickspeed = 200000;

vector<vector<int> > body;
int headX, headY;
int fruitX, fruitY;

enum eDirection {STOP=0, LEFT, RIGHT, UP, DOWN};
eDirection dir;

enum colorMode {DEFAULT=0, BW};
colorMode colormode;

enum colorpairs {SNAKE_HEAD=1, SNAKE_BODY, WALL, FRUIT, EMPTY};

void pcell(WINDOW *win, int x, int y, colorpairs COLORPAIR){
    int displayColor = ( colormode==DEFAULT ? COLORPAIR : BW_COLORS+(COLORPAIR==FRUIT) );

    wattron(win, COLOR_PAIR(displayColor));
    mvwprintw(win,y,x,"##");
    wattroff(win, COLOR_PAIR(displayColor));
}

int spawnFruit(){
    fruitX = rand()%width; fruitY = rand()%height;
    for ( vector<int> pos: body ){
        if ( fruitX == pos[0] && fruitY == pos[1]) return -1;
    }
    if ( fruitX == headX && fruitY == headY ) return -1;
    else return 0;
}

int my_kbhit(){
    int ch = getch();

    if ( ch != ERR ){
        ungetch(ch);
        return 1;
    } else{
        return 0;
    }

}

void Setup(){

    start_color();
    init_pair(1, COLOR_RED, COLOR_RED);                 // Snake head
    init_pair(2, COLOR_LIGHTRED, COLOR_LIGHTRED);       // Snake body

    init_pair(4, COLOR_APPLEGREEN, COLOR_APPLEGREEN);   // Food

    init_pair(5, 255, 255);                             // Retro Colorpair
    init_pair(6,COLOR_APPLERED,COLOR_APPLERED);         // Retro Fruit Colorpair
    
    srand(time(0));
    alive = true;
    score = 0;
    headX = width/2; headY = height/2;
    while ( spawnFruit() != 0 );
    dir=RIGHT;colormode=DEFAULT;
    body.clear();
    // add bodysegments
    body.push_back({width/2-1,height/2});
    body.push_back({width/2-2,height/2});
}


void Draw(WINDOW *GAME, WINDOW *CTRLS){
    werase(GAME); werase(CTRLS);
    box(GAME,0,0); box(CTRLS,0,0);

    pcell(GAME, 2*headX+1,headY+1,SNAKE_HEAD);
    pcell(GAME,2*fruitX+1,fruitY+1,FRUIT);

    const char *score_text = (" Score: "+to_string(score)).c_str();
    const char *hs_text = (" - HI: "+to_string(hs)+" ").c_str();

    mvwprintw(GAME,0,3,score_text);
    wprintw(GAME,hs_text);

    for (vector<int> pos: body){
        pcell(GAME,2*pos[0]+1,pos[1]+1,SNAKE_BODY);
    }
    mvwprintw(CTRLS,1,1,"CONTROLS:");
    mvwprintw(CTRLS,2,1,"WASD - MOVEMENT");
    mvwprintw(CTRLS,3,1,"X - GIVE UP");
    mvwprintw(CTRLS,4,1,"C - CHANGE COLOR MODE");
    mvwprintw(CTRLS,5,1,"R - RESTART GAME");
    
    wrefresh(GAME); wrefresh(CTRLS);
}

void Logic(){
    if ( dir != STOP ){

        int nheadX = headX+(dir<3)*(2*(dir==2)-1);
        int nheadY = headY+(dir>2)*(2*(dir==4)-1);

        if ( nheadX<0  || nheadX==width || nheadY<0 || nheadY==width ) alive=false;
        else for( vector<int> pos: body ) if ( nheadX == pos[0] && nheadY == pos[1] ) alive=false;

        if ( alive ){
            body.insert(body.begin(),{headX, headY});
            headX = nheadX; headY = nheadY; 

            if ( headX == fruitX && headY == fruitY ) {score++; while ( spawnFruit() != 0 );}
            else body.pop_back();
        }
    }
}

void Input(WINDOW *GAME, WINDOW *CTRLS){
    for (timer = 0; timer<tickspeed; timer+=tickspeed/50 ){
        if ( my_kbhit() ){
            int dirtmp = dir; bool atmp = alive;

            switch(getch()){
                case 'w':
                    if ( dir != DOWN ){dir=UP;}
                    break;
                case 'a':
                    if ( dir != RIGHT ){dir=LEFT;}
                    break;
                case 's':
                    if ( dir != UP ){dir=DOWN;}
                    break;
                case 'd':
                    if ( dir != LEFT ){dir=RIGHT;}
                    break;
                case 'x':
                    if ( alive ) {alive=false; break;}
                    else {gameOver = true;  score+=1; break;}
                case 'c':
                    colormode = ( colormode == DEFAULT ? BW : DEFAULT );
                    Draw(GAME, CTRLS);
                    break;
                case 'r': alive=true; break;
            }
            refresh();
            if ( dirtmp != dir ) break;//|| atmp!=alive ) break;
        }
        usleep(tickspeed/50);
    }
    for (timer; timer<tickspeed; timer+=tickspeed/50) usleep(tickspeed/50);
}

int main(){

    initscr();
    cbreak();
    noecho();
    nodelay(stdscr, TRUE);
    curs_set(0);

    WINDOW *gameWindow = newwin(height+2,2*width+2,1,1);
    WINDOW *controlsWindow = newwin(height+2,width+3,1,2*width+2);
    touchwin(gameWindow); touchwin(controlsWindow);
    scrollok(stdscr,false);

    FILE *hsfile = fopen("./hs.txt","r");
    if ( hsfile!=NULL ) {
        char c;
        while ( ( c=fgetc(hsfile) )&& isdigit(c) ){hs = hs*10+(c-'0');}
    }
    else {
        hsfile = fopen("./hs.txt", "w");
        fputc('0',hsfile); hs=0;
    }
    fclose(hsfile);
    
    while (!gameOver){

        touchwin(gameWindow);
        touchwin(controlsWindow);
        Setup();

        while ( alive ){
        Draw(gameWindow, controlsWindow);
        Input(gameWindow, controlsWindow);
        Logic();
        }

        if ( score > hs ) {
            FILE *hsfile = fopen("./hs.txt","w");
            fprintf(hsfile, "%d", score);
            fclose(hsfile);
        }

        while ( !alive && !gameOver ){
            Draw(gameWindow, controlsWindow);
            Input(gameWindow, controlsWindow);
        }
    }

    curs_set(1);
    endwin();

    return 0;
}