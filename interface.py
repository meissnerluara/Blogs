# Importando as Bibliotecas
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
import grafo_matriz_grafico
from ia import gerar_titulo

class BlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BLOGS E FÓRUNS")
        self.root.geometry("600x400")
        
        self.db_config = {
            'host': 'localhost',
            'database': 'bdblog',
            'user': 'root',
            'password': ''
        }
        
        self.create_main_menu()

    def create_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as e:
            messagebox.showerror("Erro de conexão", f"Erro ao conectar ao MySQL: {e}")
            return None

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()
        
        lbl_title = tk.Label(self.root, text="BLOGS E FÓRUNS", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=20)
        
        menus = [
            ("USUÁRIO", lambda: FormsUsuario(self)),
            ("TÓPICO", lambda: FormsTopico(self)),
            ("POSTAGEM", lambda: FormsPostagem(self)),
            ("MATRIZ, GRAFO E GRÁFICO", lambda: FormsGrafo(self)),
            ("SAIR", self.root.quit)
        ]
        
        for text, command in menus:
            tk.Button(self.root, text=text, width=25, command=command).pack(pady=5)

class BaseForm(tk.Toplevel):
    def __init__(self, master, title, size="500x400"):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.master_app = master
        
        tk.Label(self, text=title, font=("Arial", 14, "bold")).pack(pady=10)
        
    def create_form(self, buttons):
        for text, command in buttons:
            tk.Button(self, text=text, width=20, command=command).pack(pady=5)

class FormsUsuario(BaseForm):
    def __init__(self, master):
        super().__init__(master, "MENU USUÁRIO")
        self.create_form([
            ("Cadastrar", self.user_register),
            ("Atualizar", self.user_update),
            ("Consultar", self.user_view),
            ("Remover", self.user_delete),
            ("Voltar", self.destroy)
        ])

    def user_register(self):
        self.clear_form("Cadastrar Usuário")
        
        fields = ["Nome:", "Email:", "Senha:"]
        entries = self.create_entries(fields, show={"Senha:": "*"})
        
        tk.Button(self, text="Cadastrar", command=lambda: self.process_user(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            [entries[f].get() for f in fields],
            "Usuário cadastrado com sucesso!"
        )).pack(pady=10)
        
        self.add_back_button()

    def user_update(self):
        self.clear_form("Atualizar Usuário")
        
        tk.Label(self, text="ID do Usuário:").pack()
        entry_id = tk.Entry(self, width=40)
        entry_id.pack()
        
        fields = ["Novo Nome:", "Novo Email:", "Nova Senha:"]
        entries = self.create_entries(fields, show={"Nova Senha:": "*"})
        
        tk.Button(self, text="Atualizar", command=lambda: self.process_user(
            "UPDATE usuarios SET nome = %s, email = %s, senha = %s WHERE id_usuario = %s",
            [entries[f].get() for f in fields] + [entry_id.get()],
            "Usuário atualizado com sucesso!",
            id_field=entry_id.get()
        )).pack(pady=10)
        
        self.add_back_button()

    def user_view(self):
        self.clear_form("Consultar Usuários")
        self.show_table(["ID", "Nome", "Email", "Senha"], "SELECT * FROM usuarios")

    def user_delete(self):
        self.clear_form("Remover Usuário")
        
        tk.Label(self, text="ID do Usuário:").pack()
        entry_id = tk.Entry(self, width=40)
        entry_id.pack()
        
        def delete():
            user_id = entry_id.get()
            if user_id:
                conn = self.master_app.create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
                        if not cursor.fetchone():
                            messagebox.showerror("Erro", "Usuário não encontrado!")
                            return
                            
                        cursor.execute("SELECT * FROM postagens WHERE id_usuario = %s", (user_id,))
                        if cursor.fetchone():
                            messagebox.showerror("Erro", "Não é possível excluir usuário com postagens!")
                            return
                            
                        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (user_id,))
                        conn.commit()
                        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                        self.destroy()
                        FormsUsuario(self.master_app)
                    except Error as e:
                        messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}")
                    finally:
                        if conn.is_connected():
                            cursor.close()
                            conn.close()
            else:
                messagebox.showerror("Erro", "Informe o ID do usuário!")
        
        tk.Button(self, text="Remover", command=delete).pack(pady=10)
        self.add_back_button()

    def process_user(self, query, values, success_msg, id_field=None):
        if all(values) and (id_field is None or id_field):
            conn = self.master_app.create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    messagebox.showinfo("Sucesso", success_msg)
                    self.destroy()
                    FormsUsuario(self.master_app)
                except Error as e:
                    messagebox.showerror("Erro", f"Erro ao processar usuário: {e}")
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def clear_form(self, title):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=title, font=("Arial", 12, "bold")).pack(pady=10)

    def create_entries(self, fields, show=None):
        entries = {}
        show = show or {}
        for field in fields:
            tk.Label(self, text=field).pack()
            entry = tk.Entry(self, width=40, show=show.get(field, ""))
            entry.pack()
            entries[field] = entry
        return entries

    def show_table(self, columns, query):
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col != "ID" else 50)
        
        conn = self.master_app.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                for row in cursor.fetchall():
                    tree.insert("", "end", values=row)
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao consultar dados: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        
        tree.pack(fill="both", expand=True)
        self.add_back_button()

    def add_back_button(self):
        tk.Button(self, text="Voltar", command=lambda: [self.destroy(), FormsUsuario(self.master_app)]).pack(pady=10)

class FormsTopico(BaseForm):
    def __init__(self, master):
        super().__init__(master, "MENU TÓPICO")
        self.create_form([
            ("Criar", self.topic_create),
            ("Editar", self.topic_edit),
            ("Visualizar", self.topic_view),
            ("Excluir", self.topic_delete),
            ("Voltar", self.destroy)
        ])

    def topic_create(self):
        self.clear_form("Criar Tópico")
        fields = ["Nome:", "Descrição:"]
        entries = self.create_entries(fields)
        
        tk.Button(self, text="Criar", command=lambda: self.process_topic(
            "INSERT INTO topicos (nome, descricao) VALUES (%s, %s)",
            [entries[f].get() for f in fields],
            "Tópico criado com sucesso!"
        )).pack(pady=10)
        
        self.add_back_button()

    def topic_edit(self):
        self.clear_form("Editar Tópico")
        
        tk.Label(self, text="ID do Tópico:").pack()
        entry_id = tk.Entry(self, width=40)
        entry_id.pack()
        
        fields = ["Novo Nome:", "Nova Descrição:"]
        entries = self.create_entries(fields)
        
        tk.Button(self, text="Editar", command=lambda: self.process_topic(
            "UPDATE topicos SET nome = %s, descricao = %s WHERE id_topico = %s",
            [entries[f].get() for f in fields] + [entry_id.get()],
            "Tópico atualizado com sucesso!",
            id_field=entry_id.get()
        )).pack(pady=10)
        
        self.add_back_button()

    def topic_view(self):
        self.clear_form("Visualizar Tópicos")
        self.show_table(["ID", "Nome", "Descrição"], "SELECT * FROM topicos")

    def topic_delete(self):
        self.clear_form("Excluir Tópico")
        
        tk.Label(self, text="ID do Tópico:").pack()
        entry_id = tk.Entry(self, width=40)
        entry_id.pack()
        
        def delete():
            topic_id = entry_id.get()
            if topic_id:
                conn = self.master_app.create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM topicos WHERE id_topico = %s", (topic_id,))
                        if not cursor.fetchone():
                            messagebox.showerror("Erro", "Tópico não encontrado!")
                            return
                            
                        cursor.execute("SELECT * FROM postagens WHERE id_topico = %s", (topic_id,))
                        if cursor.fetchone():
                            messagebox.showerror("Erro", "Não é possível excluir tópico com postagens!")
                            return
                            
                        cursor.execute("DELETE FROM topicos WHERE id_topico = %s", (topic_id,))
                        conn.commit()
                        messagebox.showinfo("Sucesso", "Tópico excluído com sucesso!")
                        self.destroy()
                        FormsTopico(self.master_app)
                    except Error as e:
                        messagebox.showerror("Erro", f"Erro ao excluir tópico: {e}")
                    finally:
                        if conn.is_connected():
                            cursor.close()
                            conn.close()
            else:
                messagebox.showerror("Erro", "Informe o ID do tópico!")
        
        tk.Button(self, text="Excluir", command=delete).pack(pady=10)
        self.add_back_button()

    def process_topic(self, query, values, success_msg, id_field=None):
        if all(values) and (id_field is None or id_field):
            conn = self.master_app.create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    messagebox.showinfo("Sucesso", success_msg)
                    self.destroy()
                    FormsTopico(self.master_app)
                except Error as e:
                    messagebox.showerror("Erro", f"Erro ao processar tópico: {e}")
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def clear_form(self, title):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=title, font=("Arial", 12, "bold")).pack(pady=10)

    def create_entries(self, fields):
        entries = {}
        for field in fields:
            tk.Label(self, text=field).pack()
            entry = tk.Entry(self, width=40)
            entry.pack()
            entries[field] = entry
        return entries

    def show_table(self, columns, query):
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150 if col != "ID" else 50)
            if col == "Descrição":
                tree.column(col, width=300)
        
        conn = self.master_app.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                for row in cursor.fetchall():
                    tree.insert("", "end", values=row)
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao consultar dados: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        
        tree.pack(fill="both", expand=True)
        self.add_back_button()

    def add_back_button(self):
        tk.Button(self, text="Voltar", command=lambda: [self.destroy(), FormsTopico(self.master_app)]).pack(pady=10)

class FormsPostagem(BaseForm):
    def __init__(self, master):
        super().__init__(master, "MENU POSTAGEM", "600x500")
        self.create_form([
            ("Criar", self.post_create),
            ("Visualizar", self.post_view),
            ("Voltar", self.destroy)
        ])

    def post_create(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        tk.Label(self, text="Criar Postagem", font=("Arial", 12, "bold")).pack(pady=10)
        
        frame_ia = tk.Frame(self)
        frame_ia.pack(pady=5)
        tk.Label(frame_ia, text="Gerar título com IA:").pack(side=tk.LEFT)
        self.var_ia = tk.BooleanVar(value=False)
        tk.Checkbutton(frame_ia, variable=self.var_ia).pack(side=tk.LEFT)
        
        fields = {
            "Título:": {"width": 60},
            "Conteúdo:": {"widget": tk.Text, "width": 60, "height": 10},
            "ID do Usuário:": {"width": 60},
            "ID do Tópico:": {"width": 60}
        }
        
        self.entries = {}
        for label, config in fields.items():
            tk.Label(self, text=label).pack()
            widget_class = config.get("widget", tk.Entry)
            entry = widget_class(self, width=config["width"])
            if widget_class == tk.Text and "height" in config:
                entry.config(height=config["height"])
            entry.pack()
            self.entries[label] = entry
        
        tk.Button(self, text="Gerar Título com IA", command=self.generate_title).pack(pady=5)
        tk.Button(self, text="Criar", command=self.process_post).pack(pady=10)
        self.add_back_button()

    def generate_title(self):
        conteudo = self.entries["Conteúdo:"].get("1.0", "end-1c")
        if conteudo:
            try:
                titulo = gerar_titulo(conteudo)
                self.entries["Título:"].delete(0, tk.END)
                self.entries["Título:"].insert(0, titulo)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao gerar título com IA: {e}")
        else:
            messagebox.showwarning("Aviso", "Digite o conteúdo primeiro para gerar o título")

    def process_post(self):
        titulo = self.entries["Título:"].get()
        conteudo = self.entries["Conteúdo:"].get("1.0", "end-1c") if isinstance(self.entries["Conteúdo:"], tk.Text) else self.entries["Conteúdo:"].get()
        id_usuario = self.entries["ID do Usuário:"].get()
        id_topico = self.entries["ID do Tópico:"].get()
        
        if titulo and conteudo and id_usuario and id_topico:
            conn = self.master_app.create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
                    if not cursor.fetchone():
                        messagebox.showerror("Erro", "Usuário não encontrado!")
                        return
                        
                    cursor.execute("SELECT * FROM topicos WHERE id_topico = %s", (id_topico,))
                    if not cursor.fetchone():
                        messagebox.showerror("Erro", "Tópico não encontrado!")
                        return
                        
                    cursor.execute("""
                        INSERT INTO postagens (titulo, conteudo, id_usuario, id_topico) 
                        VALUES (%s, %s, %s, %s)
                    """, (titulo, conteudo, id_usuario, id_topico))
                    conn.commit()
                    messagebox.showinfo("Sucesso", f"Postagem '{titulo}' criada com sucesso!")
                    self.destroy()
                    FormsPostagem(self.master_app)
                except Error as e:
                    messagebox.showerror("Erro", f"Erro ao criar postagem: {e}")
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def post_view(self):
        self.clear_form("Visualizar Postagens")
        columns = ["ID", "Título", "Conteúdo", "Data", "ID Usuário", "ID Tópico"]
        tree = ttk.Treeview(self, columns=columns, show="headings")
        
        col_widths = {
            "ID": 50, "Título": 150, "Conteúdo": 200, 
            "Data": 120, "ID Usuário": 80, "ID Tópico": 80
        }
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=col_widths[col])
        
        conn = self.master_app.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM postagens")
                for row in cursor.fetchall():
                    tree.insert("", "end", values=row)
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao consultar postagens: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        
        tree.pack(fill="both", expand=True)
        self.add_back_button()

    def clear_form(self, title):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=title, font=("Arial", 12, "bold")).pack(pady=10)

    def add_back_button(self):
        tk.Button(self, text="Voltar", command=lambda: [self.destroy(), FormsPostagem(self.master_app)]).pack(pady=10)

class FormsGrafo(BaseForm):
    def __init__(self, master):
        super().__init__(master, "VISUALIZAÇÕES", "500x300")
        self.create_form([
            ("Visualizar Matriz", self.show_matrix),
            ("Visualizar Grafo", self.show_graph),
            ("Visualizar Gráfico", self.show_chart),
            ("Voltar", self.destroy)
        ])
    
    def show_matrix(self):
        import threading
        threading.Thread(target=grafo_matriz_grafico.visualizar_matriz, daemon=True).start()
    
    def show_graph(self):
        import threading
        threading.Thread(target=grafo_matriz_grafico.visualizar_grafo, daemon=True).start()
    
    def show_chart(self):
        import threading
        threading.Thread(target=grafo_matriz_grafico.visualizar_grafico, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogApp(root)
    root.mainloop()