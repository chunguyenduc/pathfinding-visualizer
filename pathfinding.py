import tkinter as tk
from tkinter import ttk, messagebox
import time
from algorithm import *

#Kích thước cứng cho chương trình
#Sửa cũng được nhưng mà phải đúng tỷ lệ

HEIGHT = 600
WIDTH = 600
SIDE = 20 # Kích thước của 1 ô

#Vậy theo kích thước này thì chương trình có 30x30 ô

#Kiểm tra tại vị trí đó có phải wall
def isWall(a, row, col):
	return a[row][col] == 1

#Kiểm tra tại vị trí đó có phải điểm bắt đầu
def isStart(a, row, col):
	return a[row][col] == -2

#Kiểm tra tại vị trí đó có phải điểm kết thúc
def isGoal(a, row, col):
	return a[row][col] == 2

'''
Chương  trình có 3 class chính
	- Board: Dùng để vẽ tường, xóa tường, ...
	- ProcessBoard: kế thừa Board, có thêm các chức năng tìm đường đi, vẽ đường đi, xóa đường đi
	- OptionBoard: có các button chạy, xóa, chọn thuật toán, liên kết với ProcessBoard
'''

	
#Board chính
class Board(tk.Frame): #Kế thừa frame của tkinter
	def __init__(self, root, h = HEIGHT, w=WIDTH):
		
		super().__init__(root, width=h, height=w)

		
		self.canvas = tk.Canvas(self, width = WIDTH, height=HEIGHT, bg='white')
		
		heightMatrix = h//SIDE
		widthMatrix = w//SIDE

		self.a = [[0] * (heightMatrix) for i in range(widthMatrix)] #Ma trận của Board
		
		
		#0 là đi được, 1 là không đi được
		
		#Khởi tạo điểm bắt đầu và kết thúc
		self.startNode = Node(None, (heightMatrix//2, 0))
		self.endNode = Node(None, (heightMatrix//2, widthMatrix-1))
		
		#Set ma trận cho start, end
		startRow, startCol = self.startNode.position
		endRow, endCol = self.endNode.position
		
		
		self.a[startRow][startCol] = -2 #Điểm bắt đầu có giá trị -2
		self.a[endRow][endCol] = 2 #Điểm kết thúc có giá trị 2
		
		#List chứa những vị trí là wall
		self.wallList = []
		
		
		
	def drawBoard(self):
	
		self.pack(side='left')
		self.canvas.pack()
		#Vẽ các đường ngang dọc để tạo thành bàn cờ
		
		#Vẽ đường ngang
		x1 = 0
		x2 = WIDTH
		for k in range(0, HEIGHT, SIDE):
			y1 = k
			y2 = k
			self.canvas.create_line(x1, y1, x2, y2)
		#Vẽ đường dọc
		y1 = 0
		y2 = HEIGHT
		for k in range(0, WIDTH, SIDE):
			x1 = k
			x2 = k
			self.canvas.create_line(x1, y1, x2, y2)
			
		#Tô màu điểm bắt đầu và kết thúc	
		self.highlight(self.startNode.position[0], self.startNode.position[1], 'green')
		self.highlight(self.endNode.position[0], self.endNode.position[1], 'orange')
		
		
	#Tạo thao tác với người dùng	
	def setUI(self):
		
		# Click event handling
		self.canvas.bind("<Button-1>", self.callbackClick)


	#Xoa thao tac voi nguoi dung	
	def disableUI(self):
		
		self.canvas.unbind("<Button-1>")
		self.canvas.unbind("<B1-Motion>")

	#Update điểm bắt đầu và kết thúc khi được thao tác
	def updateStart(self, row, col):
		self.a[row][col] = -2
		self.startNode.position = (row, col)
		
	def updateGoal(self, row, col):
		self.a[row][col] = 2
		self.endNode.position = (row, col)
	
	
	#Tô màu 1 ô được click vào
	def highlight(self, row, col, color):
		
		#Thực chất là tạo hình chữ nhật màu khác ở vị trí đó
		x0 = col * SIDE
		y0 = row * SIDE

		x1 = (col + 1) * SIDE
		y1 = (row + 1) * SIDE
		
		#Nếu màu xám thì set value và thêm vị trí vào wallList
		if color == 'darkslategray':
			self.a[row][col] = 1
			self.wallList.append((row, col))
			
		#Nếu màu xanh lá thì updateStart
		elif color == 'green':
			self.updateStart(row, col)
			
		#Nếu màu cam lá thì updateGoal	
		elif color == 'orange':
			self.updateGoal(row, col)
			
		self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

		
	#Xóa màu 1 ô
	def hide(self, row, col):
		
		#Nếu là tường thì xóa vị trí trong wallList
		if self.a[row][col] == 1:
			self.wallList.remove((row, col))
			
				
		#Set value 
		self.a[row][col] = 0
		
		#Thực chất là tạo hình chữ nhật màu trắng ở vị trí đó
		x0 = col * SIDE
		y0 = row * SIDE

		x1 = (col + 1) * SIDE
		y1 = (row + 1) * SIDE

		self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
				
	#Hàm thực hiện vẽ tường, xóa tường, ... khi người dùng thao tác
	def callbackClick(self, event):
	

		self.canvas.focus_set()
		
		#Lấy giá trị dòng và cột được click
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		
		#Nếu click vào điểm bắt đầu hoặc kết thúc thì hold sẽ là kéo điểm
		if isStart(self.a, row, col):
			self.canvas.bind("<B1-Motion>", self.dragStart)
		
		elif isGoal(self.a, row, col):
			self.canvas.bind("<B1-Motion>", self.dragGoal)
		
		else:
		
			#Neu click vao wall thi hold sẽ là xóa tường
			if isWall(self.a, row, col):
				self.hide(row, col)
				self.canvas.bind("<B1-Motion>", self.deleteWall)
				
			#Neu click ô rỗng thi hold se la tạo tường	
			else:
				self.highlight(row, col, 'darkslategray')
				self.canvas.bind("<B1-Motion>", self.createWall)
				
		#NOTE: Cảm thấy hàm này hơi rườm rà, chắc là có thể làm mượt hơn
		
	#Kéo điểm bắt đầu	
	def dragStart(self, event):
	
		self.canvas.focus_set()
		
		#Điểm cũ
		oldRow = self.startNode.position[0]
		oldCol = self.startNode.position[1]
		
		#Điểm mới
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		#Nếu đủ điều kiện thì thực hiện kéo điểm bằng cách tô điểm mới và xóa điểm cũ
		if not isWall(self.a, row, col) and (oldRow, oldCol) != (row, col) and not isGoal(self.a, row, col):
			self.highlight(row, col, 'green')
			self.hide(oldRow, oldCol)
	
	#Kéo điểm kết thúc	
	def dragGoal(self, event):
	
		self.canvas.focus_set()
		
		#Điểm cũ
		oldRow = self.endNode.position[0]
		oldCol = self.endNode.position[1]
		
		#Điểm mới
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		#Nếu đủ điều kiện thì thực hiện kéo điểm bằng cách tô điểm mới và xóa điểm cũ
		if not isWall(self.a, row, col) and (oldRow, oldCol) != (row, col) and not isStart(self.a, row, col):
			self.highlight(row, col, 'orange')
			self.hide(oldRow, oldCol)
		
	#NOTE: Cảm thấy là 2 hàm trên có thể gộp
	

	#Tạo wall
	def createWall(self, event):

		self.canvas.focus_set()
		
		#Lấy giá trị dòng và cột được click
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		#Nếu đủ điều kiện thì tô màu ô đó
		if not isWall(self.a, row, col) and not isStart(self.a, row, col) and not isGoal(self.a, row, col):
			self.highlight(row, col, 'darkslategray')
			
	
	#Xóa wall
	def deleteWall(self, event):

		self.canvas.focus_set()
		
		#Lấy giá trị dòng và cột được click
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		#Nếu điểm là wall, xóa ô đó
		if isWall(self.a, row, col):
			self.hide(row, col)
	
	
	
#================================================================================================================================	
	
class ProcessBoard(Board):
	def __init__(self, root):
		
		
		
		super().__init__(root)
		
		#Thứ tự duyệt đường đi
		self.traversal = []
		
		
		#Đường đi
		self.path = []
		
		#Thuật toán sử dụng, default là A*
		self.algo = "A* Search"
		
		self.button = None
	
		self.doTraverse = None
		self.doPath = None
	
	#Hàm xử lý khi click Run
	def findPath(self):
		
		#Xóa đường đi cũ trước khi vẽ đường đi mới
		self.clearPath()
		
		#Biến tạm
		traversal, path = 0, 0
		
		
		#Choosing algorithm
		if self.algo == "A* Search":
		
			traversal, path = astar(self.a, self.startNode.position, self.endNode.position)
		
		elif self.algo == "Dijkstra Search":
			traversal, path = ucs(self.a, self.startNode.position, self.endNode.position)
			
		elif self.algo == "Breadth First Search" :
			traversal, path = bfs(self.a, self.startNode.position, self.endNode.position)
			
		else:
			traversal, path = dfs(self.a, self.startNode.position, self.endNode.position)
		
		#NOTE: Khúc trên rườm rà quá, có thể làm gọn
		
		#Không tìm được đường đi xuất thông báo
		if path == -1:
			messagebox.showerror(message='No path', title='Error')
		
		else:
			self.traversal = traversal
			
			self.path = path
			
			
			
			
			#Vẽ đường đi
			self.drawSearch()
			#self.drawCloseTraversal()
			
			
		
		
	#Hàm xóa tất cả khi click Clear All		
	def clearAll(self):

		#Xóa wall
		#Xóa phần tử đầu cho đến khi rỗng
		while self.wallList != []:
			self.hide(self.wallList[0][0], self.wallList[0][1])
			
		#Xóa đường đi
		self.clearPath()
		
	#Xóa đường đi	
	def clearPath(self):
	
		#Xóa phần tử đầu cho đến khi rỗng	
		while self.path != []:
			
			if self.path[0] != self.startNode.position and self.path[0] != self.endNode.position and not isWall(self.a, self.path[0][0], self.path[0][1]):
				self.hide(self.path[0][0], self.path[0][1])
			self.path.pop(0)
		
		while self.traversal != []:
			if self.traversal[0] != self.startNode.position and self.traversal[0] != self.endNode.position and not isWall(self.a, self.traversal[0][0], self.traversal[0][1]):
				self.hide(self.traversal[0][0], self.traversal[0][1])
			self.traversal.pop(0)
			
		
			
	#NOTE: Hàm trên quá dài đi


	def linkto(self, optionBoard):
		self.button = optionBoard.runButton

	#Hàm vẽ đường đi
	def drawSearch(self, i=0, j=1):
		#Trong quá trình vẽ thì không được thao tác 
		
		self.button.config(state = "disable")	#Liệt nút Run
		self.disableUI()						#Liệt thao tác Board chính
	
		#Khúc này khó quá quên rồi
		
		if i >= len(self.traversal)-1:
			#self.canvas.after_cancel(self.doTraverse)
			if j >= len(self.path)-1:
			
				#Khúc này là kết thúc vẽ
				self.button.config(state = "active") 	#Làm nút Run bấm được
				self.setUI()							#Làm Board chính thao tác được
				#self.canvas.after_cancel(self.doPath)
				return
			else:
				self.highlight(self.path[j][0], self.path[j][1], 'yellow')
				#self.doPath = 
				self.canvas.after(0, lambda: self.drawSearch(i, j+1))
			#return
		else:
			self.highlight(self.traversal[i][0], self.traversal[i][1], 'midnightblue')
			#self.doTraverse = 
			self.canvas.after(5, lambda: self.drawSearch(i+1))
		
		
	
		
	

	
		
						
			
	
	
#Board process
class OptionBoard(tk.Frame):
	def __init__(self, root, h=HEIGHT, w=WIDTH//3):
		'''
		#Main Board
		self.board = board
		'''
		
		#Frame bên cạnh Main Board
		super().__init__(root, width=h, height=w)
		self.pack(side='left', fill='both')
		
		
		self.process = None
		
		
		#Button Run
		self.runButton = None
		
	
		#Button Clear All
		self.clearButton = None
		
		
		
		#Button Clear Path
		self.clearPathButton = None
		
		
		#Combobox chọn thuật toán
		self.algoBox = ttk.Combobox(self, 
                            values=[
                                    "A* Search", 
                                    "Dijkstra Search",
                                    "Breadth First Search",
                                    "Depth First Search"])
		
		self.algoBox.current(0)
		self.algoBox.bind("<<ComboboxSelected>>", self.chooseAlgo)
		
		
		
	#
	def drawOptionBoard(self):
		self.pack(side='left')
		self.runButton.pack()
		self.clearButton.pack()
		self.clearPathButton.pack()
		self.algoBox.pack()
		
	
	#Hàm set thuật toán khi được click chọn thuật toán
	def chooseAlgo(self, event):
			self.process.algo = self.algoBox.get()
	
	
	def linkto(self, processBoard):
		self.process = processBoard
		self.runButton = tk.Button(self, text='Run', width = 10, command = self.process.findPath)
		self.clearButton = tk.Button(self, text='Clear All', width = 10, command = self.process.clearAll)
		self.clearPathButton = tk.Button(self, text='Clear Path', width = 10, command=self.process.clearPath) 
		
		

def main():


	root = tk.Tk()
	root.title("Pathfinding Visualizer")
	
	
	
	process_board = ProcessBoard(root)
	process_board.drawBoard()
	process_board.setUI()
	
	
	option_board = OptionBoard(root)
	
	
	option_board.linkto(process_board)
	option_board.drawOptionBoard()
	
	
	
	process_board.linkto(option_board)
	
	
	root.mainloop()

if __name__ == "__main__":
	main()
	










