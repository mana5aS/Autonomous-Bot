import numpy as np

def updateDirection(i, j, direction) :
	if (direction%4) == 0:
		j += 1		
	elif (direction%4) == 1:
		i += 1
	elif (direction%4) == 2:
		j -= 1
	elif (direction%4) == 3:
		i -= 1	
	return ([i, j])


def checkCell(i,j):
	if maze[i][j] == wall or maze[i][j] >= 0 :#maze[i][j] == 1 or maze[i][j] == 0:      #i in [0,i_max+1] or j in [0,j_max+] (can write this instead of wall)
		if (direction%4) == 0:
			j -= 1		
		elif (direction%4) == 1:
			i -= 1
		elif (direction%4) == 2:
			j += 1
		elif (direction%4) == 3:
			i += 1	
		return (["invalid",i,j])	
	else:
		return(["valid",i,j])

count = 0
minDistance = 50
cell ="valid"
traversedDistance = 0
gridLength = 80
i_max = 5
j_max = 5
row, col = (i_max+2,j_max+2)                                    #refer to mazecode and see the 
unoccupied = -1	                                                  #and see the output file maze.txt
maze = [[unoccupied for i in range(col)] for j in range(row)]   #to understance this part
wall = "*"
for i in range(i_max+2):
	maze[0][i] = wall
	maze[i_max+1][i] = wall
	maze[i][0] = wall
	maze[i][i_max+1] = wall 

direction = 0 #  0-forward(+j) 1-right(+i) 2-back(-j) 3-left(-i) 
i = 1
j = 1
flag =True

if __name__ == '__main__':

	#lookStraight()
   
	while flag:

		distance = 500 #getDistance()
		
		if distance <= minDistance or cell == "invalid" :						
			#stop()			
			if cell == "valid":
				maze[i][j] = 0                        #Obstruction
				np.savetxt('maze.txt', maze, fmt='%s')
				traversedDistance = -20      #reset			

			Left_i, Left_j = updateDirection(i,j,direction-1)
			statusOfLeftCell,_,_ =  checkCell(Left_i,Left_j)
			Right_i, Right_j = updateDirection(i,j,direction+1)
			statusOfRightCell,_,_ = checkCell(Right_i,Right_j)

			if statusOfRightCell == "valid" and statusOfLeftCell == "valid" :
				print("Bruhh")
				maxDistRight = getRightDistance()
				lookStraight()
				maxDistLeft = getLeftDistance()
				lookStraight()
				if maxDistLeft <= maxDistRight :
					pivotRight()
					direction += 1			
					if cell == "invalid" :
						i,j = updateDirection(i,j,direction)
				else :
					pivotLeft()
					direction =- 1	
					if cell == "invalid" :
						i,j = updateDirection(i,j,direction)				
			elif statusOfRightCell == "valid" :
				#pivotRight()
				direction += 1
				if cell == "invalid" :
					i,j = updateDirection(i,j,direction)				
			elif statusOfLeftCell == "valid" :
				#pivotLeft()
				direction -= 1
				if cell == "invalid" :
					i,j = updateDirection(i,j,direction)				
			else :
				print("no known path available",i,j,sep="\t")
				flag = False
			cell = "valid"                                #reset

		else :
			#goForward()
			traversedDistance += 1			
			if traversedDistance > gridLength :				
				traversedDistance = 0
				count += 1
				maze[i][j] = count #1                        #path
				np.savetxt('maze.txt', maze, fmt='%s')				
				#print("old",i,j,count)
				i,j = updateDirection(i,j,direction)
				#print("\tupdate",i,j,count)
				cell,i,j = checkCell(i,j)
				#print("\t\taftercheck",cell,i,j,count)				
				
