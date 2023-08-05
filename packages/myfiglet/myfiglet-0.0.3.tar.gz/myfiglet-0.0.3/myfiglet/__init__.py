class printer:
    def A(n, s):
        if n==0:
            print(" "*3+s+" "*3,end="  ")
        if n==1:
            print(" "*2+s+" "+s+" "*2,end="  ")
        if n==2:
            print(" "+s*5+" ",end="  ")
        if n==3:
            print(" "+s+" "*3+s+" ",end="  ")
        if n==4:
            print(" "+s+" "*3+s+" ",end="  ")

    def B(n,s):
        if n==0 or n==2 or n==4:
            print(s*4+" ",end="  ")
        else:
            print(s+" "*3+s,end="  ")

    def C(n,s):
      if n==0 or n==4:
        print(" "+s*4,end="  ")
      else:
        print(s+" "*4,end="  ")

    def D(n,s):
      if n==0 or n==4:
        print(s*4+" ",end="  ")
      else:
        print(" "+s+" "*2+s,end="  ") 

    def E(n,s):
      if n==1 or n==3:
        print(s+" "*4,end="  ")
      else:
        print(s*5,end="  ") 

    def F(n,s):
      if n==1 or n==3 or n==4:
        print(s+" "*4,end="  ")
      else:
        print(s*5,end="  ")

    def G(n,s):
      if n==0 or n==4:
        print(' '+s*4,end="  ")
      if n==1:
        print(s+' '*4,end="  ")
      if n==2:
        print(s+' '+s*3,end='  ')
      if n==3:
        print(s+' '+s+' '+s,end="  ")  

    def H(n,s):
      if (n==0 or n==1 or n==3 or n==4):
        print(s+" "*3+s,end="  ")
      if n==2:
        print(s*5,end="  ")
    
    def I(n,s):
      if(n==0 or n==4):
        print(s*5,end="  ")
      else:
        print(" "*2+s+" "*2,end="  ")

    def J(n,s):
      if n==0:
        print(s*5,end="  ")
      if n==1 or n==2:
        print(" "*2+s+" "*2,end="  ")    
      if n==3 or n==4:
        print(s+" "+s+" "*2,end="  ")  

    def K(n,s):
      if n==0 or n==4:
        print(s+' '*2+s,end="  ")
      if n==1 or n==3:
        print(s+' '+s+' ',end="  ")
      if n==2:
        print(s*2+' '*2,end="  ") 


    def L(n,s):
      if(n==0 or n==1 or n==2 or n==3):
        print(s+4*" ",end="  ")
      if(n==4):
        print(s*5,end="  ")

    def M(n,s):
      if n==0 or n==3 or n==4:
        print(s+" "*3+s,end="  ")
      if n==1:
        print(s*2+" "+s*2,end="  ")
      if n==2:
        print(s+" "+s+" "+s,end="  ")

    def O(n,s):
      if n==0 or n==4:
        print(" "+s*3+" ",end="  ")
      else:
        print(s+" "*3+s,end="  ")

    def N(n,s):
      if n==0 or n==4:
        print(s+" "*3+s,end="  ")
      if n==1:
        print(s*2+" "*2+s,end="  ")
      if n==2:
        print(s+" "+s+" "+s,end="  ")
      if n==3:
        print(s+" "*2+s*2,end="  ")

    def P(n,s):
      if n==0 or n==2:
        print(s*5,end="  ")
      if n==1:
        print(s+' '*3+s,end="  ")
      if n==3 or n==4:
        print(s+' '*4,end="  ")

    def Q(n,s):
      if n==4:
        print(' '*4+s+' '*2,end="  ")
      if n==0:
        print(' '+s+' '+s+' '*3,end="  ")
      if n==1:
        print(s*2+' '*2+s+' '*2,end="  ")
      if n==2:
        print(s+' '+s+' '+s+' '*2,end="  ")
      if n==3:
        print(' '+s+' '+s+' '*3,end="  ")

    def S(n,s):
      if n==0 or n==2 or n==4:
        print(s+' '+s+' '+s,end="  ")
      if n==1:
        print(s+" "*4,end="  ")
      if n==3:
        print(" "*4+s,end="  ")

    def R(n,s):
      if n==0:
        print(s*5,end="  ")
      if n==1:
        print(s+" "*3+s,end="  ")
      if n==2:
        print(s*5,end="  ")
      if n==3:
        print(s+" "+s+" "*2,end="  ")
      if n==4:
        print(s+" "*2+s*2,end="  ")

    def T(n,s):
      if n==0:
        print(s*5,end="  ")
      else:
        print(" "*2+s+" "*2,end="  ")

    def U(n,s):
      if n==4:
        print(" "+s*3+" ",end="  ")
      else:
        print(s+" "*3+s,end="  ")

    def V(n,s):
      if n==0 or n==1 or n==2:
        print(s+" "*3+s,end="  ")
      if n==3:
        print(" "+s+" "+s+" ",end="  ")
      if n==4:
        print(" "*2+s+" "*2,end="  ")

    def W(n,s):
      if n==0 or n==1:
        print(s+' '*5+s,end='  ')
      if n==2:
        print(s+' '*2+s+' '*2+s,end="  ")
      if n==3:
        print(s+' '+s+' '+s+' '+s,end='  ')
      if n==4:
        print(' '+s+' '*3+s+' ',end="  ")

    def X(n,s):
      if n==0 or n==4:
        print(s+' '*3+s,end="  ")
      if n==1 or n==3:
        print(' '+s+' '+s+' ',end="  ")
      if n==2:
        print(' '*2+s+' '*2,end="  ")    

    def Y(n,s):
      if n==3 or n==4 or n==2:
        print(' '*2+s+' '*2,end="  ")
      if n==0:
        print(s+' '*3+s,end="  ")
      if n==1:
        print(' '+s+' '+s+' ',end="  ")

    def Z(n,s):
      if n==0 or n==4:
        print(s*5,end="  ")
      if n==2:
        print(' '*2+s+' '*2,end="  ")
      if n==1:
        print(' '*3+s+' ',end="  ")
      if n==3:
        print(' '+s+' '*3,end="  ")

    def space():
      print(" "*5,end="  ")

    def fullstop(n,s):
      if n==4:
        print(' '+s+' ',end="  ")
      else:
        print(" "*3,end="  ")

def help():
  print()
  print("*********************************************************")
  print("This program has been written by Harsh Gupta.")
  print("This program can be used to display the given input into figlet fonts :)\n")
  print("Syntax >>>myfiglet.display(<input string>,<symbol>)\n")
  print("For example.......")
  print(">>>myfiglet.dispaly('Python','%')\n")
  print("OUTPUT:")
  display("Python",'%')
  print("Second argument '<symbol>' in dispaly() is optional and is by default '*'")
  print("*********************************************************")



class control:
  def main(name,symbol):
    for i in range(0,5):
      for k in range(0,len(name)):
        if name[k]==' ':
          printer.space()
        if name[k]=='.':
          printer.fullstop(i,symbol)
        if name[k]=="a" or name[k]=="A":
          printer.A(i,symbol)
        if name[k]=="b" or name[k]=="B":
          printer.B(i,symbol)
        if name[k]=="c" or name[k]=="C":
          printer.C(i,symbol)
        if name[k]=="d" or name[k]=="D":
          printer.D(i,symbol)
        if name[k]=="e" or name[k]=="E":
          printer.E(i,symbol)     
        if name[k]=="f" or name[k]=="F":
          printer.F(i,symbol) 
        if name[k]=="g" or name[k]=="G":
          printer.G(i,symbol)                    
        if name[k]=="h" or name[k]=="H":
          printer.H(i,symbol)
        if name[k]=="i" or name[k]=="I":
          printer.I(i,symbol)
        if name[k]=="j" or name[k]=="J":
          printer.J(i,symbol)    
        if name[k]=="k" or name[k]=="K":
          printer.K(i,symbol)                     
        if name[k]=="l" or name[k]=="L":
          printer.L(i,symbol)
        if name[k]=="m" or name[k]=="M":
          printer.M(i,symbol)      
        if name[k]=="n" or name[k]=="N":
          printer.N(i,symbol)
        if name[k]=="o" or name[k]=="O":
          printer.O(i,symbol) 
        if name[k]=="p" or name[k]=="P":
          printer.P(i,symbol) 
        if name[k]=="q" or name[k]=="Q":
          printer.Q(i,symbol)              
        if name[k]=="r" or name[k]=="R":
          printer.R(i,symbol)
        if name[k]=="s" or name[k]=="S":
          printer.S(i,symbol)
        if name[k]=="t" or name[k]=="T":
          printer.T(i,symbol)     
        if name[k]=="u" or name[k]=="U":
          printer.U(i,symbol)
        if name[k]=="v" or name[k]=="V":
          printer.V(i,symbol)
        if name[k]=="w" or name[k]=="W":
          printer.W(i,symbol)
        if name[k]=="x" or name[k]=="X":
          printer.X(i,symbol) 
        if name[k]=="y" or name[k]=="Y":
          printer.Y(i,symbol) 
        if name[k]=="z" or name[k]=="Z":
          printer.Z(i,symbol)                                   
      print()  
  
def display(name,symbol='*'):
  print()
  control.main(name,symbol)
  print()
