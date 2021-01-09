from tkinter import *
import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import DES3
from Crypto import Random
import string 
import random 


class MainWindow(tk.Frame):
    def __init__(self, parent, *args,**kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Cifrado de imagenes")
        self.parent.geometry("510x380")
        self.configure(bg='NavajoWhite2')
        self.filename = ""
        self.var_key = StringVar()
        self.var_iv = StringVar()
        self.var_selected = IntVar()
        self.ivname=""
        self.imagen = []
        self.img_enc = []
        self.cabecera = []
    
        lbl = tk.Label(self, text="Ruta de archivo:",font=('Arial',12,'bold italic')
                        ,background='NavajoWhite2', foreground = 'grey1')
        lbl.grid(row=1,column=0)
        
        self.bar = tk.Entry(self, width = 40,state='disabled')
        self.bar.grid(row=1, column=1,pady=30)
        
        btn_ex = tk.Button(self,text="Examinar",font=('Helvetica',10),
                           bg="saddle brown",command=self.abrir,
                           foreground='white',width=10)
        btn_ex.grid(row = 1,column=2,padx="15")
        
        lbla = tk.Label(self, text="Introduzca la llave:",font=('Arial',12,'bold italic')
                        ,background='NavajoWhite2', foreground = 'grey1')
        lbla.grid(row=2,column=0,pady=15)
        
        self.key = tk.Entry(self, width = 20,textvariable=self.var_key,
                             font=('Arial',12))
        self.key.grid(row=2, column=1)
        
        lbliv = tk.Label(self, text="Introduzca IV:",
                         font=('Arial',12,'bold italic')
                        ,background='NavajoWhite2', foreground = 'grey1')
        lbliv.grid(row=3,column=0,pady=15)
        
        self.iv = tk.Entry(self, width = 20,textvariable=self.var_iv,
                             font=('Arial',12))
        self.iv.grid(row=3, column=1)
        
        btn_ex_iv = tk.Button(self,text="Examinar",font=('Helvetica',10),
                           bg="saddle brown",command=self.abrir_iv,
                           foreground='white',width=10)
        btn_ex_iv.grid(row = 3,column=2,padx="15")
        
        
        lblmod = tk.Label(self, text="Seleccione un modo de operacion:",
                         font=('Arial',12,'bold italic')
                        ,background='NavajoWhite2', foreground = 'grey1')
        lblmod.grid(row=4,column=0,columnspan=2,pady=15)
        
        
        rad0 = Radiobutton(self,text='ECB', value=1,
                           font=('Arial',10,'bold italic'), 
                           background='NavajoWhite2',variable=self.var_selected)
        rad0.grid(row=5, column=0)
        
        rad1 = Radiobutton(self,text='CBC', value=2,
                           font=('Arial',10,'bold italic'), 
                           background='NavajoWhite2',variable=self.var_selected)
        rad1.grid(row=5, column=1) 
        
        rad2 = Radiobutton(self,text='CFB', value=3,
                           font=('Arial',10,'bold italic'),
                           background='NavajoWhite2',variable=self.var_selected)
        rad2.grid(row=5, column=2)

        rad3 = Radiobutton(self,text='OFB', value=4,
                           font=('Arial',10,'bold italic'),
                           background='NavajoWhite2',variable=self.var_selected)
        rad3.grid(row=6, column=1)        

        btn_cifrar = tk.Button(self, text="Cifrar", command=self.cifrar,
                               bg='saddle brown',width=10,height = 2,
                               foreground='white',font=('Arial',10,'bold italic'))
        btn_cifrar.grid(row=7, column=0,pady=20)
        
        btn_Descifrar = tk.Button(self, text="Descifrar", command=self.descifrar,
                               bg='saddle brown',width=10,height = 2,
                               foreground='white',font=('Arial',10,'bold italic'))
        btn_Descifrar.grid(row=7,column=1)
        
        btn_borrar = tk.Button(self,text="Borrar",font=('Helvetica',10),
                           bg="saddle brown",command=self.borrar,
                           foreground='white',height=2,width=10)
        btn_borrar.grid(row=7,column=2)
        
    def borrar(self):
        self.ivname = ""
        self.filename = ""
        self.key.delete(0,'end')
        self.iv.delete(0,'end')
        self.bar.configure(state="normal")
        self.bar.delete(0,'end')
        self.bar.configure(state="disable")

        
    def abrir(self):
        self.filename = filedialog.askopenfilename(defaultextension = '.bmp',
                                                   initialdir = "C:/",
                                             title="Seleccionar archivo",
                                  filetypes=(("Bitmap",".bmp"),("JPG",".jpg")))
        if self.filename is not None:
            self.bar.configure(state='normal')
            self.bar.insert(END,self.filename)
            self.bar.configure(state='disabled')
            img = open(self.filename,'rb').read()
            self.imagen = img[54:]
            self.cabecera = img[:54]
            
    def abrir_iv(self):
        self.ivname = filedialog.askopenfilename(defaultextension = '.txt',
                                                   initialdir = "C:/",
                                             title="Seleccionar archivo",
                                 filetypes=[("Text","*.txt")])
        if self.ivname is not None:
            
            text = self.get_text_string()
            self.iv.insert(END,text)
            self.iv.configure(state='disabled')
                   
    def cifrar(self):
        select = self.var_selected.get()
        k = self.var_key.get()
        if len(k)==16 or len(k)==24:
            k = k.encode('utf-8')
            if select == 1:
                if self.var_iv.get() is not '':
                    messagebox.showinfo(message="El modo de operación ECB no" 
                                        +"requiere un vector de inicialización")    
                cipher = DES3.new(k, DES3.MODE_ECB)
                modo = "ECB"
                
            elif select == 2:
                if self.var_iv.get() is not '':
                    iv = self.var_iv.get()
                    if len(iv) != 8:
                        messagebox.showinfo(message="El IV debe tener 8 caracteres")
                    iv = iv.encode('utf-8')
                else:
                    iv = ''.join(random.choices(string.ascii_uppercase 
                                                + string.digits, k=8))
                    iv = iv.encode('utf-8')
                cipher = DES3.new(k, DES3.MODE_CBC, iv)
                modo = "CBC"
                self.save_text(iv.decode('utf-8'))
            elif select == 3:
                if self.var_iv.get() is not '':
                    iv = self.var_iv.get()
                    if len(iv) != 8:
                        messagebox.showinfo(message="El IV debe tener 8 caracteres")
                    iv = iv.encode('utf-8')
                else:
                    iv = ''.join(random.choices(string.ascii_uppercase 
                                                + string.digits, k=8))
                    iv = iv.encode('utf-8')
                cipher = DES3.new(k, DES3.MODE_CFB, iv)
                modo = "CFB"
                self.save_text(iv.decode('utf-8'))
            elif select == 4.:
                if self.var_iv.get() is not '':
                    iv = self.var_iv.get()
                    if len(iv) != 8:
                        messagebox.showinfo(message="El IV debe tener 8 caracteres")
                    iv = iv.encode('utf-8')
                else:
                    iv = ''.join(random.choices(string.ascii_uppercase 
                                                + string.digits, k=8))
                    iv = iv.encode('utf-8')
                cipher = DES3.new(k, DES3.MODE_OFB, iv)
                modo = "OFB"
                self.save_text(iv.decode('utf-8'))
            else:
                messagebox.showinfo(message="seleccione un modo de operación")
                return
            self.img_enc = cipher.encrypt(self.imagen)
            f1 = open(self.filename[:-4]+"_enc_"+modo+".bmp",'wb')
            f1.write(self.cabecera)
            f1.write(self.img_enc)
            f1.close()
        else:
            messagebox.showinfo(message="La llave debe tener una longitud de" 
                                    +" 16 o 24 caracteres")
            return
        
    def descifrar(self):
        select = self.var_selected.get()
        k = self.var_key.get()
        if len(k)==16 or len(k)==24:
            k = k.encode('utf-8')
            if select == 1:
                if self.var_iv.get() is not '':
                    messagebox.showinfo(message="El modo de operación ECB no" 
                                        +"requiere un vector de inicialización")    
                cipher = DES3.new(k, DES3.MODE_ECB)
                modo = "ECB"
                
            elif select == 2:
                if self.var_iv.get() is not '':
                    iv = self.var_iv.get()
                    if len(iv) != 8:
                        messagebox.showinfo(message="El IV debe tener 8 caracteres")
                    iv = iv.encode('utf-8')
                else:
                    iv = ''.join(random.choices(string.ascii_uppercase 
                                                + string.digits, k=8))
                    iv = iv.encode('utf-8')
                cipher = DES3.new(k, DES3.MODE_CBC, iv)
                modo = "CBC"
            elif select == 3:
                if self.var_iv.get() is not '':
                    iv = self.var_iv.get()
                    if len(iv) != 8:
                        messagebox.showinfo(message="El IV debe tener 8 caracteres")
                    iv = iv.encode('utf-8')
                else:
                    iv = ''.join(random.choices(string.ascii_uppercase 
                                                + string.digits, k=8))
                    iv = iv.encode('utf-8')
                cipher = DES3.new(k, DES3.MODE_CFB, iv)
                modo = "CFB"
            elif select == 4.:
                if self.var_iv.get() is not '':
                    iv = self.var_iv.get()
                    if len(iv) != 8:
                        messagebox.showinfo(message="El IV debe tener 8 caracteres")
                    iv = iv.encode('utf-8')
                else:
                    iv = ''.join(random.choices(string.ascii_uppercase 
                                                + string.digits, k=8))
                    iv = iv.encode('utf-8')
                cipher = DES3.new(k, DES3.MODE_OFB, iv)
                modo = "OFB"
            else:
                messagebox.showinfo(message="seleccione un modo de operación")
                return
            self.img_enc = cipher.decrypt(self.imagen)
            f1 = open(self.filename[:-11]+"_dec_"+modo+".bmp",'wb')
            f1.write(self.cabecera)
            f1.write(self.img_enc)
            f1.close()
        else:
            messagebox.showinfo(message="La llave debe tener una longitud de" 
                                    +" 16 o 24 caracteres")
            return
        
        
    def save_text(self,texto):
        f = open(self.filename[:-4]+'_iv.txt', 'w',encoding = 'utf-8')
        f.write(texto)
        f.close()
        
    def get_text_string(self):
        ##abrimos el archivo
        f = open(self.ivname,encoding='utf-8')
        ##obtenemos el texto
        textString = f.read()
        f.close()
        return textString
        
if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

