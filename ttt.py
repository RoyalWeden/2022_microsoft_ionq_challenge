from typing import List
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
from rich import print
from rich import box
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.compiler import assemble
import asyncio
backend = QasmSimulator()



class board:
    def __init__(self) -> None:
        self.board=[
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]
                    ]
        self.PlayerX_turn=True
        self.board_state={
            0: ' ',
            1: ' ',
            2: ' ',
            3: ' ',
            4: ' ',
            5: ' ',
            6: ' ',
            7: ' ',
            8: ' ',
        }

    async def q_measure(self,state,key):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr)
        for i in state:
            if i =='1':
                qc.x(qr[0])
                qc.h(qr[0])
        
            elif i=='0':
                qc.h(qr[0])
        qc.measure(qr, cr)
        print(qc.draw(output='text'))
        qc_compiled = transpile(qc, backend)
        qc_compiled=assemble(qc)
        job = backend.run(qc_compiled, shots=1)
        result = job.result()
        counts = result.get_counts(qc)
        print(counts)
        if '0'in counts.keys():
            self.board_state[key]="⭕"
            print("⭕")
        else:
            self.board_state[key]="❌"
            print("❌")

    def update_board(self):
        for i in range(3):
            for j in range(3):
                if self.board_state[i*3+j]=="❌":
                    self.board[i][j]=1
                elif self.board_state[i*3+j]=="⭕":
                    self.board[i][j]=-1
                else:
                    self.board[i][j]=0
    
    def win(self):
        self.update_board()
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != 0:
                print(self)
                print("\n[center][green][bold]Game Over.\n")
                if self.PlayerX_turn:
                    print("[green]❌ wins!")
                else:
                    print("[green]⭕ wins!")
                return True
        return False                 
               
    async def mes(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j]==0 and self.board_state[i*3+j]!=" ":
                    await self.q_measure(self.board_state[i*3+j],i*3+j)
                    self.update_board()


    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        table = Table(title="[green]Board",show_header=False,show_lines=True,border_style=None,box=box.ROUNDED)
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_row(self.board_state[0], self.board_state[1], self.board_state[2])
        table.add_row(self.board_state[3], self.board_state[4], self.board_state[5])
        table.add_row(self.board_state[6], self.board_state[7], self.board_state[8])
        yield table

        

if __name__=='__main__':
    board=board()
    print("[bold italic yellow on red blink]Welcome to Tic Tac Toe!\n")
    while not board.win():
        if board.PlayerX_turn:
            print("[green]❌ turn")
        else:
            print("[red]⭕[/] turn")
        print(board)
        print("\n[green]Enter the number of the cell you want to mark or m to measure:")
        inp=input()
        if inp=="m":
            asyncio.run(board.mes())
            board.PlayerX_turn=not board.PlayerX_turn
        else:
            cell=int(inp)
            if cell>=0 and cell<=8 and board.board[cell//3][cell%3]==0:
                if board.PlayerX_turn:
                    board.board_state[cell]=board.board_state[cell]+"1"
                    board.PlayerX_turn=False
                else:
                    board.board_state[cell]=board.board_state[cell]+"0"
                    board.PlayerX_turn=True
            else:
                print("[red]This cell is already marked.")

        
    