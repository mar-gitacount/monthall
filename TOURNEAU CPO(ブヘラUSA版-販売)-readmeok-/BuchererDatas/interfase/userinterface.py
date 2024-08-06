import tkinter as tk

def main():
    root = tk.Tk()
    root.title("シンプルなウィンドウ")
    root.geometry("300x200")
    
    label = tk.Label(root, text="こんにちは、tkinter!")
    label.pack(pady=20)
    
    button = tk.Button(root, text="閉じる", command=root.quit)
    button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
