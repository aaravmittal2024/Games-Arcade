from tkinter import *
from tkinter import messagebox, Tk
import random

class MSCell(Label):
    '''represents an MScell'''
    fg_colormap = ['white','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']

    def __init__(self,master,coord):
        '''MSCell(master,coord) -> MSCell
        creates a new blank MSCell with (row,column) coord'''
        Label.__init__(self,master,height=1,width=2,text='',\
                       bg='white',font=('Arial',24))

        # Initializing the attributes
        self.number = 0
        self.coord = coord
        self.bomb = False
        self.exposed = False
        self.flag = False
        #self.fg_color = self.fg_colormap[self.number]
        self["relief"] = RAISED
        
        # Binding the buttons
        self.bind('<Button-1>',self.expose_cell) 
        self.bind('<Button-2>',self.toggle_flag_bomb) 
        self.bind('<Button-3>',self.toggle_flag_bomb)
        
    # Accessor methods
    def get_coord(self):
        '''MSCell.get_coord() -> tuple
        returns the (row,column) coordinate of the cell'''
        return self.coord

    def get_number(self):
        '''MSCell.get_number() -> int
        returns the number of bombs adjacent
        to the cell'''
        return self.number

    def is_exposed(self):
        '''MSCell.is_exposed() -> boolean
        returns True if the cell is exposed
        and False otherwise'''
        return self.exposed

    def has_Bomb(self):
        '''MSCell.has_Bomb() -> boolean
        returns True if the cell is a bomb
        and False otherwise'''
        return self.bomb

    def is_flagged(self):
        '''MSCell.is_flagged() -> boolean
        returns True if the cell is flagged
        and False otherwise'''
        return self.flag

    # Setter method
    def set_number(self,number):
        '''MSCell.set_number(number) -> None
        Sets the number in the sale'''
        self.number = number        

    # Handler methods
    def toggle_flag_bomb(self,event):
        '''MSCell.toggle_flag_bomb(event) -> None
        Flags or unflags a bomb
        When a cell is flagged:
        text display changes to *
        When a cell is unflagged:
        text display changes to ""'''
        if self.is_flagged():
             self.flag = False
             self.master.flagCount+=1
             self.master.bombCountLabel['text'] = str(self.master.flagCount)
             self.master.bombCountLabel.grid()
             self.update_display()
             
        else:
            self.flag = True
            self.master.flagCount-=1
            self.master.bombCountLabel['text'] = str(self.master.flagCount)
            self.master.bombCountLabel.grid()
            self.update_display()

    def expose_cell(self,event):
        '''MSCell.expose_cell(event) -> None
        exposes the cell'''
        if self.has_Bomb():           
            self.master.gameOverLose() #Write gameOverLose method in MSGrid
        else:
            self.exposed = True
            self.update_display()
            self.master.auto_expose(self) # Write auto_expose in MSGrid
            self.master.gameWinCheck()

    def open_cell(self):
        '''MSCell.open_cell() -> None
        auto-opens the cell'''
        if self.has_Bomb() is False:
            self.exposed = True
            self.update_display()


    def update_display(self):
        '''MSCell.update_display() -> None
        Updates the display of the cell'''
        if self.is_exposed():
            if self.number == 0:
                self['text'] = ''
            else:
                self['text'] = str(self.number)
                self['fg'] = self.fg_colormap[self.number]
            self['relief'] = SUNKEN
            self['bg'] = "lightgrey"
        elif not self.is_exposed() and self.is_flagged():
            self['text'] = "*"
        else:
            self['text'] = ''

    def expose_the_bomb(self):
        '''MSCell.expose_the_bomb() -> None
        Expose the bomb when the game is over'''
        if self.has_Bomb():
            self['text'] = "B"
            self['bg'] = "red"

class MSGrid(Frame):
    '''object for a Mindsweeper grid'''

    def __init__(self,master,width,height,numBombs):
        '''MSGrid(master)
        creates a new blank Mindsweeper grid'''
        # initialize a new Frame
        Frame.__init__(self,master,bg='black')
        self.grid()
        self.cellsExp = {} # Dictionary of MSCells (including dummy cells)
        self.cells = {} # Dictionary of MSCells without dummy cells
        self.width = width
        self.height = height
        self.numBombs = numBombs
        self.flagCount = numBombs
        self.coordList = []

        # Create bomb-counter label
        self.bombCountLabel = Label(self,text=str(self.flagCount),height=2,width=3,bg='white',font=('Arial',30))
        self.bombCountLabel.grid(row=self.height+1,columnspan=self.width)
        
        
        # Create the cells
        for r in range(-1,height+1):
            for c in range(-1,width+1):
                coord = (r,c)
                self.cellsExp[coord] = MSCell(self,coord)
                
        # Grid the approppriate cells
        for r in range(height):
            for c in range(width):
                coord = (r,c)
                self.cells[coord] = self.cellsExp[coord]
                self.cells[coord].grid(row=r,column=c)
                
        # Set up surround cell dictionary
        self.surroundCellDict = {}
        for r in range(height):
            for c in range(width):
                self.surroundCellDict[self.cellsExp[(r,c)]] = [self.cellsExp[(r-1,c-1)],self.cellsExp[(r-1,c)],self.cellsExp[(r-1,c+1)],\
                                                               self.cellsExp[(r,c-1)],self.cellsExp[(r,c+1)],\
                                                               self.cellsExp[(r+1,c-1)],self.cellsExp[(r+1,c)],self.cellsExp[(r+1,c+1)]]
    

        # Randomly selects cells to place bombs in
        self.bombCellList=random.sample(list(self.cells.values()),self.numBombs)

        # Places bombs within the randomly selected cells
        for cell in self.bombCellList:
            cell.bomb = True

        # Counts the surrounding cells having bombs
        for cell in list(self.cells.values()):
            for adjCell in self.surroundCellDict[cell]:
                if adjCell.has_Bomb():
                    cell.number+=1


    def auto_expose(self,clickedCell):
        '''MSGrid.auto_expose(clickCellCoord) -> None
        Auto exposes cell that need to be exposed'''        
        for cell in self.surroundCellDict[clickedCell]:
            if cell.has_Bomb() is False:
                cell.open_cell()

    def gameOverLose(self):
        '''MSGrid.gameOver() -> None
        Displays a window with a statement
        that announces when the game is over and the player has lost'''
        for cell in self.bombCellList:
            cell.expose_the_bomb()
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
        


    def gameOverWin(self):
        '''MSGrid.gameOver() -> None
        Displays a window with a statement
        that announces when the game is over and the player has won'''
        messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)
        

    def gameWinCheck(self):
        '''MSGrid.gameWinCheck() -> None
        Checks to see if the player
        has won by counting the number of exposed
        cells and checking if it is equal to the total
        number of cells without bombs in the gameboard'''
        exposedCellCount=0
        for cell in list(self.cells.values()):
            if cell.is_exposed():
                exposedCellCount+=1

        if exposedCellCount == (self.width * self.height) - self.numBombs:
            self.gameOverWin()
                
            
    


# main loop for the game
def minesweeper(width,height,numBombs):
    '''minesweeper(width,height,numBombs)
    plays Minesweeper'''
    root = Tk()
    root.title('MineSweeper')
    msg = MSGrid(root,width,height,numBombs)
    root.mainloop()
minesweeper(12,10,15)