import re
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date, datetime
import random
from modules.entities import Clients, Users, Rooms, Reservations
import modules.utils as utils


# ─────────────────────────────────────────────
#  PALETA / CONSTANTES VISUAIS
# ─────────────────────────────────────────────
BG       = "#FFFFFF"
SIDEBAR  = "#F5F5F5"
BORDER   = "#1A1A1A"
ACCENT   = "#1A1A1A"
TEXT     = "#1A1A1A"
TEXT2    = "#555555"
BTN_ACT  = "#1A1A1A"
BTN_TXT  = "#FFFFFF"
BTN_HVR  = "#333333"
GREEN    = "#2E7D32"
RED      = "#C62828"
ORANGE   = "#E65100"
FONT     = ("Helvetica", 10)
FONT_B   = ("Helvetica", 10, "bold")
FONT_H   = ("Helvetica", 13, "bold")
FONT_T   = ("Helvetica", 18, "bold")


# ═══════════════════════════════════════════
#  DADOS DA APLICAÇÃO
# ═══════════════════════════════════════════

TARIFS = {
    "Single":  {"Baixa": 40,  "Média": 50,  "Alta": 70},
    "Double":  {"Baixa": 65,  "Média": 80,  "Alta": 110},
    "Suite":   {"Baixa": 120, "Média": 150, "Alta": 200},
}

rooms_data = utils.get_all('rooms')
clients_data = utils.get_all('clients')
reservations_data = utils.get_all('reservations')
users_data = utils.get_all('users')

ROOMS = {}
CLIENTS = {}
RESERVATIONS = []
USERS = {}

for r in rooms_data:
    room = Rooms(r[0], r[1], r[2], r[3], r[6], r[4], r[5])
    ROOMS[room.id] = room

for c in clients_data:
    CLIENTS[c[0]] = Clients(c[0], c[1], c[2], c[3], c[5], c[4])

for rs in reservations_data:
    RESERVATIONS.append(Reservations(rs[0], rs[1], rs[2], rs[3], rs[4], rs[5], rs[6]))

for u in users_data:
    USERS[u[0]] = Users(u[0], u[1], u[2], u[3], u[4], u[5])

# ═══════════════════════════════════════════
#  JANELA PRINCIPAL
# ═══════════════════════════════════════════
class CaboGest(tk.Tk):
    def __init__(self):
        """Initialize the object and set up its starting values."""
        super().__init__()
        self.title("CaboGest")
        self.geometry("900x580")
        self.minsize(750, 500)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._build_layout()
        self._show_page("inicio")

    # ── Layout principal ──────────────────
    def _build_layout(self):
        """Create the main window layout and the content area."""
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR, bd=0,
                                highlightbackground=BORDER,
                                highlightthickness=1, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Área de conteúdo
        self.content = tk.Frame(self, bg=BG,
                                highlightbackground=BORDER,
                                highlightthickness=1)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_sidebar()

    def _build_sidebar(self):
        """Create the sidebar area with logo, navigation, and footer buttons."""
        # Logo
        logo_f = tk.Frame(self.sidebar, bg=SIDEBAR, pady=16)
        logo_f.pack(fill=tk.X)
        tk.Label(logo_f, text="CaboGest", font=("Helvetica", 16, "bold"),
                 bg=SIDEBAR, fg=TEXT).pack()
        tk.Label(logo_f, text="Sistema de Gestão", font=("Helvetica", 8),
                 bg=SIDEBAR, fg=TEXT2).pack()

        sep = tk.Frame(self.sidebar, bg=BORDER, height=1)
        sep.pack(fill=tk.X, padx=10, pady=4)

        # Botões de navegação
        nav_items = [
            ("🏠", "Inicio",    "inicio"),
            ("📅", "Reservas",  "reservas"),
            ("👥", "Clientes",  "clientes"),
            ("🛏", "Quartos",   "quartos"),
            ("💲", "Tarifario", "tarifario"),
            ("📊", "Relatório", "relatorio"),
        ]

        self._nav_btns = {}
        for icon, label, page in nav_items:
            btn = self._nav_button(self.sidebar, icon, label, page)
            self._nav_btns[page] = btn

        # Rodapé sidebar: config + ajuda
        bot = tk.Frame(self.sidebar, bg=SIDEBAR)
        bot.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=12)
        sep2 = tk.Frame(self.sidebar, bg=BORDER, height=1)
        sep2.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=2)

        self._icon_btn(bot, "⚙", self._abrir_config).pack(side=tk.LEFT)
        self._icon_btn(bot, "?", self._abrir_ajuda).pack(side=tk.LEFT, padx=8)

    def _nav_button(self, parent, icon, label, page):
        """Create one sidebar navigation button with hover and click actions."""
        frame = tk.Frame(parent, bg=SIDEBAR, cursor="hand2")
        frame.pack(fill=tk.X, padx=12, pady=3)

        inner = tk.Frame(frame, bg=SIDEBAR, bd=1,
                         highlightbackground=BORDER, highlightthickness=1,
                         cursor="hand2")
        inner.pack(fill=tk.X)

        icon_lbl = tk.Label(inner, text=icon, font=FONT_B,
                             bg=SIDEBAR, fg=TEXT, cursor="hand2")
        icon_lbl.pack(side=tk.LEFT, padx=(8, 0), pady=10)

        lbl = tk.Label(inner, text=f"  {label}", font=FONT_B,
                       bg=SIDEBAR, fg=TEXT, anchor="w", padx=8, pady=10,
                       cursor="hand2")
        lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        def on_click(p=page):
            """Run the sidebar action for this page and show its content."""
            self._show_page(p)

        def on_enter(e, f=inner, l=lbl):
            """Highlight the button when the mouse pointer enters it."""
            f.configure(bg=ACCENT)
            l.configure(bg=ACCENT, fg=BTN_TXT)

        def on_leave(e, f=inner, l=lbl, p=page):
            """Return the button to normal style when the mouse leaves it."""
            if self._active != p:
                f.configure(bg=SIDEBAR)
                l.configure(bg=SIDEBAR, fg=TEXT)

        # Make icon and label react jointly as a single button
        icon_lbl.bind("<Button-1>", lambda e: on_click())
        icon_lbl.bind("<Enter>", on_enter)
        icon_lbl.bind("<Leave>", on_leave)
        inner.bind("<Button-1>", lambda e: on_click())
        lbl.bind("<Button-1>",   lambda e: on_click())
        inner.bind("<Enter>", on_enter)
        inner.bind("<Leave>", on_leave)
        lbl.bind("<Enter>",   on_enter)
        lbl.bind("<Leave>",   on_leave)

        return (inner, lbl)

    def _icon_btn(self, parent, symbol, cmd):
        """Create a small icon button for the sidebar footer."""
        btn = tk.Label(parent, text=symbol, font=FONT_B,
                       bg=SIDEBAR, fg=TEXT, cursor="hand2",
                       relief="solid", bd=1, width=3, pady=4)
        btn.bind("<Button-1>", lambda e: cmd())
        btn.bind("<Enter>", lambda e: btn.configure(bg=ACCENT, fg=BTN_TXT))
        btn.bind("<Leave>", lambda e: btn.configure(bg=SIDEBAR, fg=TEXT))
        return btn

    # ── Navegação ─────────────────────────
    def _show_page(self, name):
        """Switch the main content area to the requested page."""
        self._active = name

        # Reset todos os botões
        for p, (frame, lbl) in self._nav_btns.items():
            if p == name:
                frame.configure(bg=ACCENT)
                lbl.configure(bg=ACCENT, fg=BTN_TXT)
            else:
                frame.configure(bg=SIDEBAR)
                lbl.configure(bg=SIDEBAR, fg=TEXT)

        # Limpar conteúdo
        for w in self.content.winfo_children():
            w.destroy()

        pages = {
            "inicio":    PaginaInicio,
            "reservas":  PaginaReservas,
            "clientes":  PaginaClientes,
            "quartos":   PaginaQuartos,
            "tarifario": PaginaTarifario,
            "relatorio": PaginaRelatorio,
        }
        if name in pages:
            pages[name](self.content)

    # ── Diálogos especiais ─────────────────
    def _abrir_config(self):
        """Open a simple configuration dialog window."""
        w = tk.Toplevel(self)
        w.title("Configurações")
        w.geometry("340x200")
        w.resizable(False, False)
        w.configure(bg=BG)
        tk.Label(w, text="⚙  Configurações", font=FONT_H, bg=BG).pack(pady=20)
        tk.Label(w, text="Nome do estabelecimento:", font=FONT, bg=BG).pack()
        e = tk.Entry(w, font=FONT, width=28)
        e.insert(0, "CaboGest Hotel")
        e.pack(pady=6)
        tk.Button(w, text="Guardar", font=FONT_B, bg=ACCENT, fg=BTN_TXT,
                  relief="flat", padx=20, pady=6,
                  command=lambda: (messagebox.showinfo("OK", "Configurações guardadas!"), w.destroy())
                  ).pack(pady=10)

    def _abrir_ajuda(self):
        """Show the help dialog with basic instructions."""
        msg = (
            "CaboGest — Sistema de Gestão Hoteleira\n\n"
            "• Inicio: painel de resumo\n"
            "• Reservas: gerir todas as reservas\n"
            "• Quartos: ver e editar quartos\n"
            "• Tarifario: gerir preços por temporada\n"
            "• Relatório: estatísticas e exportação\n\n"
            "Versão 1.0  |  Tkinter + Python"
        )
        messagebox.showinfo("Ajuda — CaboGest", msg)


# ═══════════════════════════════════════════
#  HELPERS REUTILIZÁVEIS
# ═══════════════════════════════════════════
def titulo(parent, texto):
    """Display a section title and separator line on the page."""
    tk.Label(parent, text=texto, font=FONT_T, bg=BG, fg=TEXT,
             anchor="w").pack(fill=tk.X, padx=24, pady=(20, 4))
    tk.Frame(parent, bg=BORDER, height=2).pack(fill=tk.X, padx=24, pady=(0, 16))


def btn_primario(parent, texto, cmd, **kw):
    """Create a primary action button with hover styling."""
    b = tk.Button(parent, text=texto, font=FONT_B, bg=ACCENT, fg=BTN_TXT,
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  activebackground=BTN_HVR, activeforeground=BTN_TXT,
                  command=cmd, **kw)
    b.bind("<Enter>", lambda e: b.configure(bg=BTN_HVR))
    b.bind("<Leave>", lambda e: b.configure(bg=ACCENT))
    return b


def btn_perigo(parent, texto, cmd, **kw):
    """Create a red danger button for destructive actions."""
    b = tk.Button(parent, text=texto, font=FONT_B, bg=RED, fg=BTN_TXT,
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  activebackground="#8B0000", activeforeground=BTN_TXT,
                  command=cmd, **kw)
    return b


def card(parent, **kw):
    """Create a simple framed container for grouping widgets."""
    return tk.Frame(parent, bg=BG, bd=1,
                    highlightbackground="#CCCCCC",
                    highlightthickness=1, **kw)


def stat_card(parent, valor, rotulo, cor=TEXT):
    """Create a small statistics card with value, label and color."""
    f = card(parent, padx=16, pady=12)
    tk.Label(f, text=str(valor), font=("Helvetica", 26, "bold"),
             bg=BG, fg=cor).pack()
    tk.Label(f, text=rotulo, font=("Helvetica", 9),
             bg=BG, fg=TEXT2).pack()
    return f


def normalize_datetime(value):
    """Convert a date or text value into a datetime object if possible."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


def format_date(value):
    """Format a date or datetime value as a human-readable string."""
    dt = normalize_datetime(value)
    return dt.strftime("%d/%m/%Y") if dt else str(value)


def reservation_guest_name(reservation):
    """Return the guest name for a reservation, using the reservation data."""
    name = reservation.client_name()
    if name and name != "Unknown":
        return name
    client = CLIENTS.get(reservation.client_id)
    if client:
        return f"{client.f_name} {client.l_name}"
    return "Desconhecido"


# ═══════════════════════════════════════════
#  PÁGINA: INÍCIO
# ═══════════════════════════════════════════
class PaginaInicio(tk.Frame):
    def __init__(self, parent):
        """Initialize the object and set up its starting values."""
        super().__init__(parent, bg=BG)
        self.pack(fill=tk.BOTH, expand=True)
        titulo(self, "🏠  Painel de Início")
        self._stats()
        self._proximas()

    def _stats(self):
        """Calculate and display summary statistics on the page."""
        f = tk.Frame(self, bg=BG)
        f.pack(fill=tk.X, padx=24, pady=8)

        disponiveis = sum(1 for q in ROOMS.values() if q.occupied == 0)
        ocupados    = len(ROOMS) - disponiveis
        hoje        = sum(1 for r in RESERVATIONS
                         if normalize_datetime(r.start_date).date() == date.today())

        receita = sum(r.total_price for r in RESERVATIONS)

        cards = [
            (len(ROOMS), "Total de Quartos", TEXT),
            (disponiveis,  "Disponíveis",      GREEN),
            (ocupados,     "Ocupados",          RED),
            (f"{receita}€","Receita Total",     ORANGE),
        ]
        for v, r, c in cards:
            s = stat_card(f, v, r, c)
            s.pack(side=tk.LEFT, padx=6, pady=4, fill=tk.X, expand=True)

    def _proximas(self):
        """Show the most recent reservations in a list."""
        tk.Label(self, text="Reservas Recentes", font=FONT_B,
                 bg=BG, fg=TEXT2, anchor="w").pack(fill=tk.X, padx=24, pady=(12, 4))

        cols = ("ID", "Hóspede", "Quarto", "Check-in", "Check-out", "Total")
        tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor="center")
        tree.column("Hóspede", width=160)

        for r in RESERVATIONS[-10:][::-1]:
            tree.insert("", tk.END, values=(
                r.id, reservation_guest_name(r), r.room_id,
                format_date(r.start_date), format_date(r.end_date), f"{r.total_price}€"
            ))

        sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(fill=tk.BOTH, expand=True, padx=24, pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y)


# ═══════════════════════════════════════════
#  PÁGINA: RESERVATIONS
# ═══════════════════════════════════════════
class PaginaReservas(tk.Frame):
    def __init__(self, parent):
        """Initialize the object and set up its starting values."""
        super().__init__(parent, bg=BG)
        self.pack(fill=tk.BOTH, expand=True)
        titulo(self, "📅  Gestão de Reservas")

        bar = tk.Frame(self, bg=BG)
        bar.pack(fill=tk.X, padx=24, pady=(0, 8))
        btn_primario(bar, "+ Novo Hóspede", self._novo_cliente).pack(side=tk.LEFT, padx=(0, 8))
        btn_primario(bar, "+ Nova Reserva", self._nova).pack(side=tk.LEFT, padx=(0, 8))
        btn_primario(bar, "Transferir Selecionada", self._transferir).pack(side=tk.LEFT, padx=(0, 8))
        btn_perigo(bar, "Cancelar Selecionada", self._cancelar).pack(side=tk.LEFT)

        # Pesquisa
        tk.Label(bar, text="Pesquisar:", font=FONT, bg=BG).pack(side=tk.LEFT, padx=(20, 4))
        self.pesq = tk.StringVar()
        self.pesq.trace_add("write", lambda *a: self._filtrar())
        tk.Entry(bar, textvariable=self.pesq, font=FONT, width=18,
                 relief="solid", bd=1).pack(side=tk.LEFT)

        self._build_tree()
        self._carregar()

    def _build_tree(self):
        """Create the table view and its columns for this page."""
        cols = ("ID", "Hóspede", "Quarto", "Check-in", "Check-out", "Noites", "Total", "Estado")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        widths = [40, 160, 70, 90, 90, 60, 70, 90]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c, command=lambda _c=c: self._ordenar(_c))
            self.tree.column(c, width=w, anchor="center")
        self.tree.column("Hóspede", anchor="w")

        sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=24, pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.tag_configure("ativa",     background="#E8F5E9")
        self.tree.tag_configure("cancelada", background="#FFEBEE", foreground="#999")

    def _carregar(self, dados=None):
        """Load the current records into the table display."""
        self.tree.delete(*self.tree.get_children())
        lista = dados if dados is not None else RESERVATIONS
        for r in lista:
            tag = "cancelada" if r.status == "canceled" else "ativa"
            start_dt = normalize_datetime(r.start_date)
            end_dt = normalize_datetime(r.end_date)
            noites = (end_dt - start_dt).days if start_dt and end_dt else 0
            self.tree.insert("", tk.END, iid=r.id, tags=(tag,), values=(
                r.id, reservation_guest_name(r), r.room_id,
                format_date(r.start_date), format_date(r.end_date),
                noites, f"{r.total_price}€",
                r.status
            ))

    def _filtrar(self):
        """Filter the displayed records using the search text."""
        q = self.pesq.get().lower()
        filtrado = [r for r in RESERVATIONS
                    if q in r.client_name().lower() or q in str(r.room_id)]
        self._carregar(filtrado)

    def _ordenar(self, col):
        """Sort the records shown in the table by the selected column."""
        # Map the column names directly to a lambda function that reads the object
        key_map = {
          "ID": lambda r: r.id,
          "Hóspede": lambda r: r.get_client_name() or "",
          "Quarto": lambda r: r.room_id,
          "Check-in": lambda r: r.start_date,
          "Total": lambda r: r.total_price
      }
      
        # Fallback to getattr if the column isn't in the map (uses lowercase attribute name)
        sort_key = key_map.get(col, lambda r: getattr(r, col.lower(), ""))
      
        try:
          # Sort the list in place using the extracted key function
          RESERVATIONS.sort(key=sort_key)
        except Exception as e:
          print(f"Sorting error: {e}") # Temporarily print error for debugging
          
        self._carregar()

    def _novo_cliente(self):
        """Open the window to add a new client."""
        JanelaNovoCliente(self, self._carregar)

    def _nova(self):
        """Open the window to create a new reservation."""
        JanelaNovaReserva(self, self._carregar)

    def _cancelar(self):
        """Cancel the currently selected reservation."""
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Seleciona uma reserva primeiro.")
            return
        rid = int(sel)
        for r in RESERVATIONS:
            if r.id == rid:
                if r.status == "canceled":
                    messagebox.showinfo("Info", "Reserva já cancelada.")
                    return
                if messagebox.askyesno("Cancelar", f"Cancelar reserva #{rid}?"):
                    r.status = "canceled"
                    # Libertar quarto
                    room = ROOMS.get(r.room_id)
                    if room is not None:
                        room.occupied = 0
                    self._carregar()
                return

    def _transferir(self):
        """Transfer the currently selected reservation to another client."""
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Seleciona uma reserva primeiro.")
            return

        rid = int(sel)
        reserva = next((r for r in RESERVATIONS if r.id == rid), None)
        if reserva is None:
            messagebox.showerror("Erro", "Reserva não encontrada.")
            return
        if reserva.status == "canceled":
            messagebox.showwarning("Aviso", "Não é possível transferir uma reserva cancelada.")
            return

        novo_email = simpledialog.askstring("Transferir Reserva",
                                           "Email do novo hóspede:", parent=self)
        if not novo_email:
            return

        novo_cliente_id = utils.get_client_id_by_email(novo_email.strip())
        if novo_cliente_id is None:
            if messagebox.askyesno("Cliente não encontrado",
                                   "Cliente não encontrado. Deseja cadastrar um novo cliente?", parent=self):
                JanelaNovoCliente(self, self._carregar, novo_email.strip())
            return

        if reserva.transfer_to_client(novo_cliente_id):
            messagebox.showinfo("Transferido", f"Reserva #{rid} transferida para {novo_email.strip()}.")
            self._carregar()
        else:
            messagebox.showerror("Erro", "Não foi possível transferir a reserva.")


# ── Janela: Nova Reserva ──────────────────
class JanelaNovaReserva(tk.Toplevel):
    def __init__(self, parent, callback):
        """Initialize the object and set up its starting values."""
        super().__init__(parent)
        self.callback = callback
        self.title("Nova Reserva")
        self.geometry("420x380")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.grab_set()

        tk.Label(self, text="Nova Reserva", font=FONT_H, bg=BG).pack(pady=14)

        form = tk.Frame(self, bg=BG)
        form.pack(padx=30, fill=tk.X)

        campos = [
            ("Email do Hóspede:",    "hospede",   "entry"),
            ("Quarto nº:",  "quarto",    "combo"),
            ("Check-in\n(dd/mm/aaaa):", "checkin",  "entry"),
            ("Check-out\n(dd/mm/aaaa):","checkout", "entry"),
        ]

        self.vars = {}
        for i, (label, key, tipo) in enumerate(campos):
            tk.Label(form, text=label, font=FONT, bg=BG, anchor="e",
                     width=16).grid(row=i, column=0, pady=6, sticky="e")
            if tipo == "entry":
                v = tk.StringVar()
                tk.Entry(form, textvariable=v, font=FONT, width=20,
                         relief="solid", bd=1).grid(row=i, column=1, padx=8, sticky="w")
            else:
                v = tk.StringVar()
                disponiveis = [str(room.id) for room in ROOMS.values() if room.occupied == 0]
                cb = ttk.Combobox(form, textvariable=v, values=disponiveis,
                                  font=FONT, width=18, state="readonly")
                cb.grid(row=i, column=1, padx=8, sticky="w")
            self.vars[key] = v

        btn_primario(self, "✔  Confirmar Reserva", self._confirmar).pack(pady=18)

    def _confirmar(self):
        """Validate the form data and create the reservation."""
        h  = self.vars["hospede"].get().strip()
        q  = self.vars["quarto"].get().strip()
        ci = self.vars["checkin"].get().strip()
        co = self.vars["checkout"].get().strip()

        if not all([h, q, ci, co]):
            messagebox.showwarning("Campos em falta", "Preenche todos os campos.", parent=self)
            return
        try:
            q = int(q)
            d_in  = datetime.strptime(ci, "%d/%m/%Y").date()
            d_out = datetime.strptime(co, "%d/%m/%Y").date()
            noites = (d_out - d_in).days
            if noites <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas ou check-out antes do check-in.", parent=self)
            return
        
        client_id = utils.get_client_id_by_email(h)
        if client_id is None:
            if messagebox.askyesno("Cliente não encontrado", "Cliente não encontrado. Deseja cadastrar um novo cliente?", parent=self):
                JanelaNovoCliente(self, self._on_new_client_added, h)
            return

        room = ROOMS.get(q)
        if room is None or room.occupied == 1:
            messagebox.showerror("Erro", "Quarto inválido ou indisponível.", parent=self)
            return

        preco  = room.price_per_night
        total  = preco * noites

        start_dt = datetime.combine(d_in, datetime.min.time())
        end_dt = datetime.combine(d_out, datetime.min.time())
        reservation = Reservations(None, client_id, q, start_dt, end_dt, 'active', total)
        reservation_id = reservation.add_reservation()
        if reservation_id is None:
            messagebox.showerror("Erro", "Não foi possível criar a reserva.", parent=self)
            return

        RESERVATIONS.append(reservation)
        room.occupied = 1

        messagebox.showinfo("Reserva criada",
                            f"Reserva #{reservation_id} criada!\n{noites} noite(s) × {preco}€ = {total}€",
                            parent=self)
        self.callback()
        self.destroy()

    def _on_new_client_added(self, client):
        """Handle the new client created during reservation flow."""
        if client is None:
            return
        self.vars["hospede"].set(client.email)
        messagebox.showinfo("Cliente Adicionado",
                            f"Cliente {client.f_name} {client.l_name} foi adicionado. Agora pode criar a reserva.",
                            parent=self)


# ═══════════════════════════════════════════
#  PÁGINA: CLIENTES
# ═══════════════════════════════════════════
class PaginaClientes(tk.Frame):
    def __init__(self, parent):
        """Initialize the object and set up its starting values."""
        super().__init__(parent, bg=BG)
        self.pack(fill=tk.BOTH, expand=True)
        titulo(self, "👥  Gestão de Clientes")

        bar = tk.Frame(self, bg=BG)
        bar.pack(fill=tk.X, padx=24, pady=(0, 8))
        btn_primario(bar, "+ Novo Cliente", self._novo_cliente).pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(bar, text="Pesquisar:", font=FONT, bg=BG).pack(side=tk.LEFT, padx=(20, 4))
        self.pesq = tk.StringVar()
        self.pesq.trace_add("write", lambda *a: self._filtrar())
        tk.Entry(bar, textvariable=self.pesq, font=FONT, width=22,
                 relief="solid", bd=1).pack(side=tk.LEFT)

        self._build_tree()
        self._carregar()

    def _build_tree(self):
        """Create the table view and its columns for this page."""
        cols = ("ID", "Nome", "Email", "Nacionalidade", "Nascimento")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        widths = [40, 180, 200, 140, 100]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
        self.tree.column("Nome", anchor="w")

        sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=24, pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

    def _carregar(self, dados=None):
        """Load the current records into the table display."""
        self.tree.delete(*self.tree.get_children())
        lista = dados if dados is not None else list(CLIENTS.values())
        for client in sorted(lista, key=lambda c: c.id):
            self.tree.insert("", tk.END, iid=client.id, values=(
                client.id,
                f"{client.f_name} {client.l_name}",
                client.email,
                client.nationality,
                format_date(client.birth_date)
            ))

    def _filtrar(self):
        """Filter the displayed records using the search text."""
        q = self.pesq.get().lower()
        filtrado = [c for c in CLIENTS.values()
                    if q in c.f_name.lower() or q in c.l_name.lower() or q in c.email.lower() or q in c.nationality.lower()]
        self._carregar(filtrado)

    def _novo_cliente(self):
        """Open the window to add a new client."""
        JanelaNovoCliente(self, self._carregar)


class JanelaNovoCliente(tk.Toplevel):
    def __init__(self, parent, callback, email_hint=None):
        """Initialize the object and set up its starting values."""
        super().__init__(parent)
        self.callback = callback
        self.title("Novo Cliente")
        self.geometry("420x320")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.grab_set()

        tk.Label(self, text="Cadastro de Cliente", font=FONT_H, bg=BG).pack(pady=14)

        form = tk.Frame(self, bg=BG)
        form.pack(padx=30, fill=tk.X)

        campos = [
            ("Nome:", "nome"),
            ("Sobrenome:", "sobrenome"),
            ("Email:", "email"),
            ("Nacionalidade:", "nacionalidade"),
            ("Nascimento (dd/mm/aaaa):", "birth_date"),
        ]

        self.vars = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(form, text=label, font=FONT, bg=BG, anchor="e",
                     width=18).grid(row=i, column=0, pady=6, sticky="e")
            v = tk.StringVar()
            tk.Entry(form, textvariable=v, font=FONT, width=22,
                     relief="solid", bd=1).grid(row=i, column=1, padx=8, sticky="w")
            self.vars[key] = v

        if email_hint:
            self.vars["email"].set(email_hint)

        btn_primario(self, "✔  Guardar Cliente", self._guardar).pack(pady=16)

    def _validar_email(self, email):
        """Check that the provided email text matches a valid pattern."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.fullmatch(pattern, email))

    def _guardar(self):
        """Validate the form inputs and save the current data."""
        nome = self.vars["nome"].get().strip()
        sobrenome = self.vars["sobrenome"].get().strip()
        email = self.vars["email"].get().strip()
        nacionalidade = self.vars["nacionalidade"].get().strip()
        nascimento = self.vars["birth_date"].get().strip()

        if not all([nome, sobrenome, email, nacionalidade, nascimento]):
            messagebox.showwarning("Campos em falta", "Preenche todos os campos.", parent=self)
            return
        if not self._validar_email(email):
            messagebox.showerror("Erro", "Email inválido.", parent=self)
            return
        try:
            nascimento_dt = datetime.strptime(nascimento, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Erro", "Data de nascimento inválida.", parent=self)
            return

        existing_id = utils.get_client_id_by_email(email)
        if existing_id is not None:
            messagebox.showwarning("Já existente", "Já existe um cliente com esse email.", parent=self)
            return

        try:
            client = Clients(None, nome, sobrenome, email, nacionalidade, nascimento_dt)
            if not client.id:
                raise ValueError("Não foi possível obter o ID do cliente.")
            CLIENTS[client.id] = client
            messagebox.showinfo("Cliente adicionado", f"Cliente {nome} {sobrenome} adicionado com sucesso.", parent=self)
            try:
                self.callback(client)
            except TypeError:
                self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível adicionar o cliente.\n{e}", parent=self)
            return


# ═══════════════════════════════════════════
#  PÁGINA: QUARTOS
# ═══════════════════════════════════════════
class PaginaQuartos(tk.Frame):
    def __init__(self, parent):
        """Initialize the object and set up its starting values."""
        super().__init__(parent, bg=BG)
        self.pack(fill=tk.BOTH, expand=True)
        titulo(self, "🛏  Gestão de Quartos")

        bar = tk.Frame(self, bg=BG)
        bar.pack(fill=tk.X, padx=24, pady=(0, 8))
        btn_primario(bar, "✎ Editar Selecionado", self._editar).pack(side=tk.LEFT, padx=(0, 8))
        btn_primario(bar, "↻ Atualizar Estado", self._toggle_estado).pack(side=tk.LEFT)

        self._build_tree()
        self._carregar()

    def _build_tree(self):
        """Create the table view and its columns for this page."""
        cols = ("Nº", "Tipo", "Preço/noite", "Estado")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160, anchor="center")
        sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=24, pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.tag_configure("Disponível", background="#E8F5E9", foreground=GREEN)
        self.tree.tag_configure("Ocupado",    background="#FFEBEE", foreground=RED)
        self.tree.tag_configure("Manutenção", background="#FFF8E1", foreground=ORANGE)

    def _carregar(self):
        """Load the current records into the table display."""
        self.tree.delete(*self.tree.get_children())
        for num in sorted(ROOMS):
            q = ROOMS[num]
            estado = "Disponível" if q.occupied == 0 else "Ocupado"
            self.tree.insert("", tk.END, iid=num, tags=(estado,), values=(
                num, q.type, f"{q.price_per_night}€", estado
            ))

    def _editar(self):
        """Open the selected room for editing."""
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Seleciona um quarto."); return
        num = int(sel)
        q   = ROOMS.get(num)
        if q is None:
            messagebox.showerror("Erro", "Quarto não encontrado."); return
        JanelaEditarQuarto(self, num, q, self._carregar)

    def _toggle_estado(self):
        """Switch the selected room between occupied and available."""
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Seleciona um quarto."); return
        num = int(sel)
        room = ROOMS.get(num)
        if room is None:
            messagebox.showerror("Erro", "Quarto não encontrado."); return
        room.occupied = 0 if room.occupied == 1 else 1
        self._carregar()


class JanelaEditarQuarto(tk.Toplevel):
    def __init__(self, parent, num, quarto: Rooms, callback):
        """Initialize the object and set up its starting values."""
        super().__init__(parent)
        self.callback = callback
        self.num      = num
        self.title(f"Editar Quarto {num}")
        self.geometry("340x240")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.grab_set()

        tk.Label(self, text=f"Quarto {num}", font=FONT_H, bg=BG).pack(pady=14)

        form = tk.Frame(self, bg=BG)
        form.pack(padx=24, fill=tk.X)

        self.tipo  = tk.StringVar(value=quarto.type)
        self.preco = tk.StringVar(value=str(quarto.price_per_night))
        self.estado= tk.StringVar(value="Disponível" if quarto.occupied == 0 else "Ocupado")

        for i, (lbl, var, opts) in enumerate([
            ("Tipo:",  self.tipo,   ["Single", "Double", "Suite"]),
            ("Estado:",self.estado, ["Disponível", "Ocupado"]),
        ]):
            tk.Label(form, text=lbl, font=FONT, bg=BG, width=10, anchor="e").grid(row=i, column=0, pady=6)
            ttk.Combobox(form, textvariable=var, values=opts,
                         state="readonly", width=18).grid(row=i, column=1, padx=8)

        tk.Label(form, text="Preço (€):", font=FONT, bg=BG, width=10, anchor="e").grid(row=2, column=0, pady=6)
        tk.Entry(form, textvariable=self.preco, font=FONT, width=20,
                 relief="solid", bd=1).grid(row=2, column=1, padx=8)

        btn_primario(self, "Guardar", self._guardar).pack(pady=14)

    def _guardar(self):
        """Validate the form inputs and save the current data."""
        try:
            p = int(self.preco.get())
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido.", parent=self)
            return
        room = ROOMS.get(self.num)
        if room is None:
            messagebox.showerror("Erro", "Quarto não encontrado.", parent=self)
            return
        room.type = self.tipo.get()
        room.price_per_night = p
        room.occupied = 0 if self.estado.get() == "Disponível" else 1
        self.callback()
        self.destroy()


# ═══════════════════════════════════════════
#  PÁGINA: TARIFÁRIO
# ═══════════════════════════════════════════
class PaginaTarifario(tk.Frame):
    def __init__(self, parent):
        """Initialize the object and set up its starting values."""
        super().__init__(parent, bg=BG)
        self.pack(fill=tk.BOTH, expand=True)
        titulo(self, "💲  Tarifário por Temporada")
        self._build()

    def _build(self):
        """Create the widgets needed for this page section."""
        # Tabela visual
        header = tk.Frame(self, bg=ACCENT)
        header.pack(fill=tk.X, padx=24, pady=(0, 1))
        for h, w in [("Tipo de Quarto", 200), ("Época Baixa", 140),
                     ("Época Média", 140), ("Época Alta", 140), ("", 60)]:
            tk.Label(header, text=h, font=FONT_B, bg=ACCENT, fg=BTN_TXT,
                     width=w//8, anchor="center", pady=8).pack(side=tk.LEFT, padx=2)

        self.linhas = {}
        for tipo, precos in TARIFS.items():
            row = tk.Frame(self, bg=BG, bd=0,
                           highlightbackground="#DDDDDD", highlightthickness=1)
            row.pack(fill=tk.X, padx=24, pady=1)

            tk.Label(row, text=tipo, font=FONT_B, bg=BG, width=22,
                     anchor="w", padx=12, pady=10).pack(side=tk.LEFT)

            self.linhas[tipo] = {}
            for epoca in ["Baixa", "Média", "Alta"]:
                v = tk.StringVar(value=str(precos[epoca]))
                e = tk.Entry(row, textvariable=v, font=FONT, width=10,
                             relief="solid", bd=1, justify="center")
                e.pack(side=tk.LEFT, padx=12, pady=6)
                self.linhas[tipo][epoca] = v

            tk.Label(row, text="€/noite", font=("Helvetica", 9),
                     bg=BG, fg=TEXT2).pack(side=tk.LEFT)

        tk.Frame(self, bg=BG, height=12).pack()
        btn_primario(self, "💾  Guardar Tarifário", self._guardar).pack(padx=24, anchor="w")

        # Nota
        tk.Label(self, text="As alterações ao tarifário aplicam-se a novas reservas.",
                 font=("Helvetica", 9), bg=BG, fg=TEXT2).pack(padx=24, pady=8, anchor="w")

    def _guardar(self):
        """Validate the form inputs and save the current data."""
        try:
            for tipo, epocas in self.linhas.items():
                for epoca, var in epocas.items():
                    TARIFS[tipo][epoca] = int(var.get())
                    # Sincronizar preço padrão do quarto
                    for q in ROOMS.values():
                        if q.type == tipo:
                            q.price_per_night = TARIFS[tipo]["Média"]
        except ValueError:
            messagebox.showerror("Erro", "Todos os preços devem ser números inteiros.")
            return
        messagebox.showinfo("OK", "Tarifário guardado com sucesso!")


# ═══════════════════════════════════════════
#  PÁGINA: RELATÓRIO
# ═══════════════════════════════════════════
class PaginaRelatorio(tk.Frame):
    def __init__(self, parent):
        """Initialize the object and set up its starting values."""
        super().__init__(parent, bg=BG)
        self.pack(fill=tk.BOTH, expand=True)
        titulo(self, "📊  Relatório de Ocupação")
        self._stats()
        self._grafico()
        btn_primario(self, "📋  Exportar (consola)", self._exportar).pack(padx=24, anchor="w", pady=8)

    def _stats(self):
        """Calculate and display summary statistics on the page."""
        f = tk.Frame(self, bg=BG)
        f.pack(fill=tk.X, padx=24, pady=4)

        total_res  = len(RESERVATIONS)
        ativas     = sum(1 for r in RESERVATIONS if r.status != "canceled")
        canceladas = total_res - ativas
        receita    = sum(r.total_price for r in RESERVATIONS if r.status != "canceled")
        ocup_pct   = round((sum(1 for q in ROOMS.values() if q.occupied == 1)
                            / len(ROOMS)) * 100) if ROOMS else 0

        cards = [
            (total_res,  "Total Reservas", TEXT),
            (ativas,     "Reservas Ativas", GREEN),
            (canceladas, "Canceladas",      RED),
            (f"{receita}€", "Receita",     ORANGE),
            (f"{ocup_pct}%","Ocupação",    "#1565C0"),
        ]
        for v, r, c in cards:
            s = stat_card(f, v, r, c)
            s.pack(side=tk.LEFT, padx=4, pady=4, fill=tk.X, expand=True)

    def _grafico(self):
        """Draw the simple occupancy chart on the report page."""
        tk.Label(self, text="Ocupação por tipo de quarto", font=FONT_B,
                 bg=BG, fg=TEXT2, anchor="w").pack(fill=tk.X, padx=24, pady=(12, 4))

        canvas = tk.Canvas(self, bg=BG, height=120, highlightthickness=0)
        canvas.pack(fill=tk.X, padx=24)

        tipos = ["Single", "Double", "Suite"]
        cores = [ACCENT, "#555", "#888"]
        for i, (tipo, cor) in enumerate(zip(tipos, cores)):
            total   = sum(1 for q in ROOMS.values() if q.type == tipo)
            ocup    = sum(1 for q in ROOMS.values() if q.type == tipo and q.occupied == 1)
            pct     = (ocup / total * 100) if total else 0
            x0, y0  = 40 + i * 200, 20
            larg, alt = 140, 80
            canvas.create_rectangle(x0, y0 + alt * (1 - pct/100), x0 + larg, y0 + alt,
                                     fill=cor, outline="")
            canvas.create_rectangle(x0, y0, x0 + larg, y0 + alt,
                                     fill="", outline="#CCCCCC")
            canvas.create_text(x0 + larg//2, y0 + alt + 14,
                               text=f"{tipo}  {ocup}/{total}", font=("Helvetica", 9), fill=TEXT2)
            canvas.create_text(x0 + larg//2, y0 + alt * (1 - pct/100) - 6,
                               text=f"{round(pct)}%", font=("Helvetica", 9, "bold"), fill=TEXT)

    def _exportar(self):
        """Export the report data to the terminal and show confirmation."""
        print("\n" + "="*50)
        print("RELATÓRIO CaboGest —", datetime.now().strftime("%d/%m/%Y %H:%M"))
        print("="*50)
        for r in RESERVATIONS:
            print(f"#{r.id:03d} | {r.client_name():<20} | Q{r.room_id} | "
                  f"{format_date(r.start_date)}→{format_date(r.end_date)} | {r.total_price}€ | {r.status}")
        print("="*50)
        messagebox.showinfo("Exportado", "Relatório exportado para a consola/terminal.")
