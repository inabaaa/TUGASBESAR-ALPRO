import ttkbootstrap as ttk
from tkinter import messagebox, PhotoImage, simpledialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from typing import List

# =========================
# Tipe Bentukan dan Array
# =========================

# Kelas untuk menyimpan data jadwal tiket
class Jadwal:
    def __init__(self, nik, stasiun_asal, stasiun_tujuan, waktu, tanggal, jumlah_penumpang):
        self.nik = nik
        self.stasiun_asal = stasiun_asal
        self.stasiun_tujuan = stasiun_tujuan
        self.waktu = waktu
        self.tanggal = tanggal
        self.jumlah_penumpang = jumlah_penumpang

# Array statis utama (maksimal 100 data)
MAX = 10
data_jadwal: List[Jadwal] = [None] * MAX
jumlah_data = 0

# =========================
# Fungsi Pemesanan Tiket
# =========================

def booking():
    # Tambah data baru ke data_jadwal dari form pemesanan
    global jumlah_data
    nikbuattiket = entryNikForm.get()
    stasiunAsalbuattiket = entryStasiunAwalForm.get().upper()
    stasiunTujuanbuattiket = entryStasiunTujuanForm.get().upper()
    waktubuattiket = data_pesanan["waktu"]
    tanggalbuattiket = dateentryTanggalForm.entry.get()
    try:
        jumlahPenumpangbuattiket = int(entryJumlahPenumpangForm.get())
    except ValueError:
        messagebox.showerror("Error", "Jumlah penumpang harus angka!")
        return
    if not nikbuattiket or not stasiunAsalbuattiket or not stasiunTujuanbuattiket or not waktubuattiket or not tanggalbuattiket:
        messagebox.showerror("Error", "Semua data harus diisi!")
        return
    if jumlah_data < MAX:
        data_jadwal[jumlah_data] = Jadwal(
            nikbuattiket,
            stasiunAsalbuattiket,
            stasiunTujuanbuattiket,
            waktubuattiket,
            tanggalbuattiket,
            jumlahPenumpangbuattiket
        )
        jumlah_data += 1
        refresh_tree()
        messagebox.showinfo("Pemesanan Tiket Berhasil", "Berhasil, Periksa Email Anda !!")
    else:
        messagebox.showerror("Error", "Data penuh, tidak bisa menambah data baru.")
    update_grafik()
    halamanForm()


# =========================
# Fungsi Manipulasi Data
# =========================

def cari_data_sequential():
    # Cari data berdasarkan NIK (sequential search)
    keyword = entrycari.get().strip().lower()
    for item in tree.get_children():
        tree.delete(item)
    found = False
    for i in range(jumlah_data):
        jadwal = data_jadwal[i]
        if jadwal:
            if not keyword or keyword in jadwal.nik.lower():
                tree.insert(
                    "", "end",
                    values=(
                        jadwal.nik,
                        jadwal.stasiun_asal,
                        jadwal.stasiun_tujuan,
                        jadwal.waktu,
                        jadwal.tanggal,
                        jadwal.jumlah_penumpang
                    )
                )
                tree.insert("", "end", values=("", "", "", "", "", ""))
                found = True
    if not found and keyword:
        messagebox.showinfo("Info", "Data tidak ditemukan.")

def urutkan_data_tanggal_manual():
    # Urutkan data berdasarkan tanggal (manual bubble sort)
    global data_jadwal, jumlah_data
    urutan = comboboxurut.get()
    for i in range(jumlah_data-1):
        for j in range(jumlah_data-1-i):
            a = data_jadwal[j]
            b = data_jadwal[j+1]
            if a and b:
                try:
                    tgl_a = datetime.strptime(a.tanggal, "%d/%m/%Y")
                    tgl_b = datetime.strptime(b.tanggal, "%d/%m/%Y")
                except Exception:
                    continue
                if urutan == "1 - 31" and tgl_a > tgl_b:
                    data_jadwal[j], data_jadwal[j+1] = b, a
                elif urutan == "31 - 1" and tgl_a < tgl_b:
                    data_jadwal[j], data_jadwal[j+1] = b, a
    refresh_tree()

def filter_jumlah_penumpang():
    # Filter data berdasarkan jumlah penumpang
    try:
        jumlah_filter = int(entryFilterJumlahPenumpang.get())
    except ValueError:
        messagebox.showerror("Error", "Masukkan jumlah penumpang yang valid!")
        return
    for item in tree.get_children():
        tree.delete(item)
    found = False
    for i in range(jumlah_data):
        jadwal = data_jadwal[i]
        if jadwal and jadwal.jumlah_penumpang == jumlah_filter:
            tree.insert(
                "", "end",
                values=(
                    jadwal.nik,
                    jadwal.stasiun_asal,
                    jadwal.stasiun_tujuan,
                    jadwal.waktu,
                    jadwal.tanggal,
                    jadwal.jumlah_penumpang
                )
            )
            tree.insert("", "end", values=("", "", "", "", "", ""))
            found = True
    if not found:
        messagebox.showinfo("Info", "Data tidak ditemukan dengan jumlah penumpang tersebut.")

def edit_data():
    # Edit hanya kolom waktu berdasarkan NIK
    nik_edit = entryEditAdmin.get().strip()
    if not nik_edit:
        messagebox.showerror("Error", "Masukkan NIK yang ingin diedit!")
        return
    found = False
    for i in range(jumlah_data):
        jadwal = data_jadwal[i]
        if jadwal and jadwal.nik == nik_edit:
            waktu_baru = simpledialog.askstring("Edit Waktu", "Masukkan waktu baru:", initialvalue=jadwal.waktu)
            if waktu_baru and waktu_baru.strip():
                jadwal.waktu = waktu_baru.strip()
                found = True
            else:
                messagebox.showerror("Error", "Waktu baru tidak boleh kosong!")
            break
    refresh_tree()
    if found:
        messagebox.showinfo("Sukses", "Waktu berhasil diedit!")
    else:
        messagebox.showerror("Error", "Data dengan NIK tersebut tidak ditemukan.")
    update_grafik()

def refresh_tree():
    # Refresh isi tabel treeview dari data_jadwal
    for item in tree.get_children():
        tree.delete(item)
    for i in range(jumlah_data):
        jadwal = data_jadwal[i]
        if jadwal:
            tree.insert(
                "", "end",
                values=(
                    jadwal.nik,
                    jadwal.stasiun_asal,
                    jadwal.stasiun_tujuan,
                    jadwal.waktu,
                    jadwal.tanggal,
                    jadwal.jumlah_penumpang
                )
            )
            tree.insert("", "end", values=("", "", "", "", "", ""))

def hapus_data():
    # Hapus data berdasarkan NIK
    nik_hapus = entryHapusAdmin.get().strip()
    if not nik_hapus:
        messagebox.showerror("Error", "Masukkan NIK yang ingin dihapus!")
        return
    global jumlah_data
    found = False
    for i in range(jumlah_data):
        jadwal = data_jadwal[i]
        if jadwal and jadwal.nik == nik_hapus:
            for j in range(i, jumlah_data - 1):
                data_jadwal[j] = data_jadwal[j + 1]
            data_jadwal[jumlah_data - 1] = None
            jumlah_data -= 1
            found = True
            break
    # Refresh tabel dan grafik
    refresh_tree()
    if found:
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    else:
        messagebox.showerror("Error", "Data dengan NIK tersebut tidak ditemukan.")
    update_grafik()

# =========================
# Fungsi Grafik
# =========================

def update_grafik():
    # Hitung jumlah penumpang per bulan dari data_jadwal
    bulan_dict = {i:0 for i in range(1,13)}
    for i in range(jumlah_data):
        jadwal = data_jadwal[i]
        if jadwal and jadwal.tanggal:
            try:
                bulan = int(jadwal.tanggal.split("/")[1])
                bulan_dict[bulan] += jadwal.jumlah_penumpang
            except Exception:
                continue
    x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    y = [bulan_dict[i] for i in range(1,13)]
    ax.clear()
    ax.plot(
        x, y,
        marker='o',
        color="#eeeeee",
        linestyle='-',
        linewidth=3,
        markersize=10,
        markerfacecolor='#EEEEEE',
        markeredgecolor='#00ADB5',
        label='Data Penumpang'
    )
    ax.set_title("Data Penumpang", fontsize=13, color="#EEEEEE", fontweight='bold', pad=20)
    ax.set_xlabel("Bulan", fontsize=10, color="#FFFFFF", fontweight='bold')
    ax.set_ylabel("Jumlah", fontsize=10, color='#FFFFFF', fontweight='bold')
    ax.grid(True, linestyle='--', color='#00ADB5', alpha=0.3)
    ax.legend(facecolor="#06334F", edgecolor='#00ADB5', fontsize=11, labelcolor='#EEEEEE')
    ax.set_facecolor("#222831")
    ax.tick_params(axis='x', colors='#EEEEEE', labelsize=11)
    ax.tick_params(axis='y', colors='#EEEEEE', labelsize=11)
    fig.tight_layout()
    canvas.draw()

# =========================
# Data Dummy Tiket & Pesanan
# =========================

data_pesanan = {
    "nik": "",
    "stasiun_awal": "",
    "stasiun_tujuan": "",
    "tanggal": "",
    "waktu": "",
    "kelas": "",
    "kereta": "",
    "harga": "",
    "metode": "",
    "jumlah_penumpang": 1
}

data_tiket = [
    {"kelas": "Ekonomi", "nama": "Kertajaya", "harga": "150k", "opsi": ["01.35", "14.30"]},
    {"kelas": "Luxury", "nama": "Taksaka", "harga": "350k", "opsi": ["11.46", "18.00"]},
    {"kelas": "Bisnis", "nama": "Gajayana", "harga": "250k", "opsi": ["09.10", "22.00"]}
]

# =========================
# Fungsi Login, Akun, dan Navigasi
# =========================

def kirim():
    # Login admin atau user
    Email = entryEmailLogin.get()
    Pass = entryPassLogin.get()
    if Email == "admin@gmail.com" and Pass == "admin123":
        halamanAdmin()
    elif not Email or not Pass:
        messagebox.showerror("Perhatikan!", "Email dan Password harus terisi")
    else:
        konfirmasi = messagebox.askyesno(
            title="Email dan Password tidak tersedia",
            message="Anda ingin membuat akun baru?"
        )
        if konfirmasi:
            halamanBuatAkun()

def Logout():
    # Logout dan kembali ke halaman login
    konfirmasi = messagebox.askyesno(
        title="Logout",
        message="Apakah Anda yakin ingin keluar?"
    )
    if konfirmasi:
        halamanLogin()

def buatAkun():
    # Simpan data akun baru ke label profil
    nomorIdentitas = entryNikBuatAkun.get()
    namaLengkap = entryNamaLengkap.get().upper()
    Emailpengguna = entryEmailpengguna.get()
    NoTelp = entryNoTelp.get()
    tanggalLahir = dateentrytanggalLahir.entry.get()
    OutputNikProfil.config(text=f" : {nomorIdentitas}")
    OutputNamaProfil.config(text=f" : {namaLengkap}")
    OutputEmailProfil.config(text=f" : {Emailpengguna}")
    OutputTelpProfil.config(text=f" : {NoTelp}")
    OutputTanggaLahirProfil.config(text=f" : {tanggalLahir}")

def CariTiket():
    # Simpan data pencarian tiket ke data_pesanan dan update label judul
    stasiun_awal = entryStasiunAwalForm.get().upper()
    stasiun_tujuan = entryStasiunTujuanForm.get().upper()
    tanggal = dateentryTanggalForm.entry.get()
    jumlah_penumpang = entryJumlahPenumpangForm.get()
    data_pesanan["nik"] = entryNikForm.get()
    data_pesanan["stasiun_awal"] = stasiun_awal
    data_pesanan["stasiun_tujuan"] = stasiun_tujuan
    data_pesanan["tanggal"] = tanggal
    data_pesanan["jumlah_penumpang"] = jumlah_penumpang
    judulRute.config(text=f"{stasiun_awal} > {stasiun_tujuan}")
    judulTanggal.config(text=f"Tanggal Keberangkatan: {tanggal}")
    
def dataTiket(parent_frame, detail_tiket):
    nama_kelas = detail_tiket['kelas']
    nama_kereta = detail_tiket['nama']
    harga = detail_tiket['harga']
    daftar_opsi = detail_tiket['opsi']
    kelas_frame = ttk.Frame(parent_frame, padding=(40, 10), relief="groove")
    label_nama = ttk.Label(kelas_frame, text=nama_kereta, font=("Helvetica", 10, "bold"))
    label_harga = ttk.Label(kelas_frame, text=harga, font=("Helvetica", 10, "bold"))
    label_rute = ttk.Label(kelas_frame, text="Stasiun Awal > Stasiun Tujuan", font=("Helvetica", 10))
    label_kelas = ttk.Label(kelas_frame, text=nama_kelas, font=("Helvetica", 9, "bold"))
    kelas_frame.pack(pady=10)
    label_nama.grid(row=0, column=0, sticky="w")
    label_harga.grid(row=0, column=1, sticky="e")
    label_rute.grid(row=1, column=0, columnspan=2)
    label_kelas.grid(row=2, column=0, sticky="w")
    for i, opsi in enumerate(daftar_opsi):
        tombol_pesan = ttk.Button(
            kelas_frame,
            text=opsi,
            bootstyle="primary-outline",
            command=lambda k=nama_kelas, o=opsi, nk=nama_kereta, h=harga: pesan_tiket(k, o, nk, h)
        )
        tombol_pesan.grid(row=2 + i, column=1, pady=10, sticky="ew")
        
def pesan_tiket(kelas, opsi, nama_kereta, harga):
    # Simpan data tiket yang dipilih user
    data_pesanan["kelas"] = kelas
    data_pesanan["waktu"] = opsi
    data_pesanan["kereta"] = nama_kereta
    jumlah = int(data_pesanan.get("jumlah_penumpang", 1) or 1)
    if "k" in harga.lower():
        harga_angka = int(harga.lower().replace("k", "")) * 1000
    else:
        harga_angka = int(harga)
    total = harga_angka * jumlah
    data_pesanan["harga"] = f"Rp {total:,}".replace(",", ".")
    halamanMetodePembayaran()
        
selected_metode_pembayaran = None
def pilih_metode_pembayaran(metode):
    # Simpan metode pembayaran yang dipilih user
    global selected_metode_pembayaran
    selected_metode_pembayaran = metode
    data_pesanan["metode"] = metode
    halamanBayarTiket()


# =========================
# Fungsi Halaman (Navigasi)
# =========================

def halamanLogin():
    # Tampilkan halaman login
    try:
        canvas.get_tk_widget().pack_forget()
    except:
        pass
    for f in [frameForm, frameProfil, frameEdit, frameTabel, frameBuatAkun, frameBayarTiket, frameMetodePembayaran, framePilihTiket]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    frameLogin.place(rely=0.5, relx=0.5, anchor="center", width=470, height=900)
    labelEmailLogin.pack(padx=10, pady=(300,25))
    entryEmailLogin.pack(padx=10)
    labelPassLogin.pack(padx=10, pady=(40, 25))
    entryPassLogin.pack(padx=10)
    buttonLogin.pack(pady=(30, 0))
    labelBuatAkun.pack(padx=100, pady=(30, 0))
    buttonBuatAkun.pack(padx=100, pady=25)
    
def halamanAdmin():
    # Tampilkan halaman admin (edit data)
    for f in [frameLogin, frameForm, frameProfil, framePilihTiket]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    frameEdit.pack(side="left", fill="y")
    buttonLogoutAdmin.grid(row=0, column=1, sticky="e", padx=(10, 0))
    labelJudulEdit.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(30, 60))
    labelcari.grid(row=2, column=0, sticky="w")
    entrycari.grid(row=2, column=1, sticky="ew", padx=(10, 0))
    buttoncari.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=40)
    labelurut.grid(row=4, column=0, sticky="w")
    comboboxurut.grid(row=4, column=1, sticky="ew", padx=(10, 0))
    buttonurut.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=40)
    labelFilter.grid(row=6, column=0, sticky="w")
    entryFilterJumlahPenumpang.grid(row=6, column=1, sticky="ew", padx=(10, 0))
    buttonfilter.grid(row=7, column=1, sticky="ew", padx=(10, 0), pady=40)
    labelEditAdmin.grid(row=8, column=0, sticky="w")
    entryEditAdmin.grid(row=8, column=1, sticky="ew", padx=(10, 0))
    buttonEditAdmin.grid(row=9, column=1, sticky="ew", padx=(10, 0), pady=40)
    labelHapusAdmin.grid(row=10, column=0, sticky="w")
    entryHapusAdmin.grid(row=10, column=1, sticky="ew", padx=(10, 0))
    buttonHapusAdmin.grid(row=11, column=1, sticky="ew", padx=(10, 0), pady=40)
    canvas.get_tk_widget().pack(padx=20, pady=20, fill="x")
    frameTabel.pack(fill="both", expand=True)
    tree.pack(fill="both", expand=True)

def halamanBuatAkun():
    # Tampilkan halaman buat akun
    for f in [frameLogin, frameProfil, frameEdit, frameTabel, framePilihTiket]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    frameBuatAkun.place(rely=0.5, relx=0.5, anchor="center", width=470, height=900)
    buttonLogoutBuatAkun.grid(row=0, column=1, sticky="e", pady=20)
    labelJudulBuatAkun.grid(row=1, column=0, pady=30, sticky="w")
    labelNikBuatAkun.grid(row=2, column=0, sticky="w", pady=40)
    entryNikBuatAkun.grid(row=2, column=1, pady=40, padx=(30, 0))
    labelNamaLengkap.grid(row=3, column=0, sticky="w")
    entryNamaLengkap.grid(row=3, column=1, padx=(30, 0))
    labelEmailpengguna.grid(row=4, column=0, sticky="w", pady=40)
    entryEmailpengguna.grid(row=4, column=1, pady=40, padx=(30, 0))
    labelNoTelp.grid(row=5, column=0, sticky="w")
    entryNoTelp.grid(row=5, column=1, padx=(30, 0))
    labeltanggalLahir.grid(row=6, column=0, pady=40, sticky="w")
    dateentrytanggalLahir.grid(row=6, column=1, pady=40, padx=(30, 0))
    buttonKirimBuatAkun.grid(row=7, column=0, pady=(40, 0), ipadx=30)
    
def halamanForm():
    # Tampilkan halaman form pemesanan tiket
    for f in [frameLogin, frameProfil, frameEdit, frameTabel, frameBayarTiket, framePilihTiket]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    frameForm.place(rely=0.5, relx=0.5, anchor="center", width=470, height=900)
    buttonProfil.pack(anchor="e", pady=(30, 60))
    labelNikForm.pack()
    entryNikForm.pack(pady=20)
    labelStasiunAwalForm.pack()
    entryStasiunAwalForm.pack(pady=20)
    labelStasiunTujuanForm.pack()
    entryStasiunTujuanForm.pack(pady=20)
    labelTanggalForm.pack()
    dateentryTanggalForm.pack(pady=20)
    labelJumlahPenumpangForm.pack()
    entryJumlahPenumpangForm.pack(pady=20)
    buttonKirimForm.pack(pady=(40, 0))

def halamanProfil():
    # Tampilkan halaman profil user
    for f in [frameLogin, frameForm, frameEdit, frameTabel, frameBuatAkun, framePilihTiket]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    frameProfil.place(rely=0.5, relx=0.5, anchor="center", width=470, height=900)
    try:
        avatar_img = PhotoImage(file="avatar.png")
        avatar = ttk.Label(frameProfil, image=avatar_img)
        avatar.image = avatar_img
    except Exception:
        avatar = ttk.Label(frameProfil, text="👤", font=("Segoe UI Emoji", 70))
    LabelJudulProfil.grid(row=0, column=0, sticky="w", pady=(10, 50))
    buttonLogoutProfil.grid(row=0, column=1, pady=(10, 50), sticky="e")
    avatar.grid(row=1, column=0, columnspan=2, pady=(10, 30))
    separatorProfil.grid(row=2, columnspan=2, pady=15, sticky="ew")
    LabelNikProfil.grid(row=3, column=0, sticky="w", pady=20)
    OutputNikProfil.grid(row=3, column=1, sticky="w", pady=20)
    LabelNamaProfil.grid(row=4, column=0, sticky="w", pady=20)
    OutputNamaProfil.grid(row=4, column=1, sticky="w", pady=20)
    LabelEmailProfil.grid(row=5, column=0, sticky="w", pady=20)
    OutputEmailProfil.grid(row=5, column=1, sticky="w", pady=20)
    LabelTelpProfil.grid(row=6, column=0, sticky="w", pady=20)
    OutputTelpProfil.grid(row=6, column=1, sticky="w", pady=20)
    LabelTanggalLahirProfil.grid(row=7, column=0, sticky="w", pady=20)
    OutputTanggaLahirProfil.grid(row=7, column=1, sticky="w", pady=20)
    buttonkembali.grid(row=8, column=0, pady=(40, 0), sticky="ew", padx=(0, 10))


def halamanPilihTiket():
    # Tampilkan halaman pilih tiket (main_frame)
    for f in [frameLogin, frameProfil, frameEdit, frameTabel, frameForm, frameMetodePembayaran]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    framePilihTiket.place(width=470, height=900, relx=0.5, rely=0.5, anchor="center")
    kembali.pack(pady=15)

def halamanMetodePembayaran():
    # Tampilkan halaman metode pembayaran
    for f in [frameForm, frameProfil, frameEdit, frameTabel, frameBuatAkun, frameLogin, frameBayarTiket, framePilihTiket]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    labelHargaMetodePembayaran.config(text=f"Total Harga: {data_pesanan['harga']}")
    frameMetodePembayaran.place(width=470, height=900, relx=0.5, rely=0.5, anchor="center")
    labelJudulMetodePembayaran.pack(pady=(30, 60))
    labelKaiPayMetodePembayaran.pack()
    buttonKaiPayMetodePembayaran.pack(pady=(10, 40))
    labelQrisMetodePembayaran.pack()
    buttonQrisMetodePembayaran.pack(pady=(10, 40))
    labelEWalletMetodePembayaran.pack()
    buttonMotionPayMetodePembayaran.pack(pady=(15, 20))
    buttonOvoMetodePembayaran.pack()
    labelHargaMetodePembayaran.pack(pady=(100, 0))
    buttonkembaliMetodePembayaran.pack(pady=(20, 0))

def halamanBayarTiket():
    # Tampilkan halaman pembayaran tiket
    for f in [frameForm, frameProfil, frameEdit, frameTabel, frameBuatAkun, frameLogin, frameMetodePembayaran, framePilihTiket]:
        try: f.place_forget()
        except: pass
        try: f.pack_forget()
        except: pass
    frameBayarTiket.place(rely=0.5, relx=0.5, anchor="center", width=470, height=900)
    # Update label sesuai metode pembayaran yang dipilih
    if selected_metode_pembayaran == "QRIS":
        labelJudulBayarTiket.config(text="QRIS")
        labelBayarTiket.config(text="QRIS")
    elif selected_metode_pembayaran == "KAIPay":
        labelJudulBayarTiket.config(text="KAIPay")
        labelBayarTiket.config(text="KAIPay")
    elif selected_metode_pembayaran == "MOTIONPAY":
        labelJudulBayarTiket.config(text="MotionPay")
        labelBayarTiket.config(text="MotionPay")
    elif selected_metode_pembayaran == "OVO":
        labelJudulBayarTiket.config(text="OVO")
        labelBayarTiket.config(text="OVO")
    else:
        labelJudulBayarTiket.config(text="Bayar Tiket")
        labelBayarTiket.config(text="")
        
    labelNikOutputBayarTiket.config(text=f": {data_pesanan['nik']}")
    labelStasiunAwalOutputBayarTiket.config(text=f": {data_pesanan['stasiun_awal']}")
    labelStasiunTujuanOutputBayarTiket.config(text=f": {data_pesanan['stasiun_tujuan']}")
    labelWaktuOutputBayarTiket.config(text=f": {data_pesanan['waktu']} WIB")
    labelTanggalOutputBayarTiket.config(text=f": {data_pesanan['tanggal']}")
    labelJumlahPenumpangOutputBayarTiket.config(text=f": {data_pesanan.get('jumlah_penumpang', '1')}")
    labelTotalPembayaranOutputBayarTiket.config(text=f": {data_pesanan['harga']}")
    
    labelBayarTiket.grid(row=1, column=0, sticky="w", pady=40)
    labelJudulBayarTiket.grid(row=0, column=0, sticky="w", pady=40)
    buttonUbahBayarTiket.grid(row=1, column=1, sticky="w", pady=40)
    labelNikBayarTiket.grid(row=2, column=0, sticky="w")
    labelNikOutputBayarTiket.grid(row=2, column=1, sticky="w")
    labelStasiunAwalBayarTiket.grid(row=3, column=0, sticky="w", pady=40)
    labelStasiunAwalOutputBayarTiket.grid(row=3, column=1, sticky="w", pady=40)
    labelStasiunTujuanBayarTiket.grid(row=4, column=0, sticky="w")
    labelStasiunTujuanOutputBayarTiket.grid(row=4, column=1, sticky="w")
    labelWaktuBayarTiket.grid(row=5, column=0, sticky="w", pady=40)
    labelWaktuOutputBayarTiket.grid(row=5, column=1, sticky="w", pady=40)
    labelTanggalBayarTiket.grid(row=6, column=0, sticky="w")
    labelTanggalOutputBayarTiket.grid(row=6, column=1, sticky="w")
    labelJumlahPenumpangBayarTiket.grid(row=7, column=0, sticky="w")
    labelJumlahPenumpangOutputBayarTiket.grid(row=7, column=1, sticky="w")
    labelTotalPembayaranBayarTiket.grid(row=7, column=0, sticky="w", pady=80)
    labelTotalPembayaranOutputBayarTiket.grid(row=7, column=1, sticky="w", pady=80)
    buttonBayarTiket.grid(row=8, column=0, sticky="w")


# === GUI WIDGETS ===
app = ttk.Window(title="Aplikasi Sederhana TTK Bootstrap", themename="superhero")
app.attributes('-fullscreen', True)

# Halaman Login
frameLogin = ttk.Frame(app, relief="solid", bootstyle="dark", padding=40)
labelEmailLogin = ttk.Label(frameLogin, text="EMAIL", font=("Verdana", 10))
entryEmailLogin = ttk.Entry(frameLogin, width=25)
labelPassLogin = ttk.Label(frameLogin, text="PASSWORD", font=("Verdana", 10))
entryPassLogin = ttk.Entry(frameLogin, show="*", width=25)
buttonLogin = ttk.Button(frameLogin, text="LOGIN", padding=(20, 5), command=kirim)
labelBuatAkun = ttk.Label(frameLogin, text="belum punya akun?")
buttonBuatAkun = ttk.Button(frameLogin, text="Daftar Sekarang", bootstyle="dark", command=halamanBuatAkun)

# Halaman Admin
frameEdit = ttk.Frame(app, bootstyle="dark", padding=90)
buttonLogoutAdmin = ttk.Button(frameEdit, text="⬅️Logout", command=Logout, bootstyle="dark")
labelJudulEdit = ttk.Label(frameEdit, text="Data Manipulation", font=("Verdana", 15))
labelcari = ttk.Label(frameEdit, text="Pencarian Data", font=("Verdana", 10))
entrycari = ttk.Entry(frameEdit)
buttoncari = ttk.Button(frameEdit, text="Cari", bootstyle="primary-outline", command=cari_data_sequential)
labelurut = ttk.Label(frameEdit, text="Urutkan Data", font=("Verdana", 10))
comboboxurut = ttk.Combobox(frameEdit, values=["1 - 31" , "31 - 1"])
buttonurut = ttk.Button(frameEdit, text="Urutkan", bootstyle="primary-outline", command=urutkan_data_tanggal_manual)
labelFilter = ttk.Label(frameEdit, text="Filter Data", font=("Verdana", 10))
entryFilterJumlahPenumpang = ttk.Entry(frameEdit)
buttonfilter = ttk.Button(frameEdit, text="Filter", bootstyle="primary-outline", command=filter_jumlah_penumpang)
labelEditAdmin = ttk.Label(frameEdit, text="Edit Data", font=("Verdana", 10))
entryEditAdmin = ttk.Entry(frameEdit)
buttonEditAdmin = ttk.Button(frameEdit, text="Edit", bootstyle="warning-outline", command=edit_data)
labelHapusAdmin = ttk.Label(frameEdit, text="Hapus Data", font=("Verdana", 10))
entryHapusAdmin = ttk.Entry(frameEdit)
buttonHapusAdmin = ttk.Button(frameEdit, text="Hapus", bootstyle="danger-outline", command=hapus_data)

# Matplotlib Figure (halaman admin)
fig = Figure(figsize=(8, 3), dpi=100, facecolor="#21374c")
ax = fig.add_subplot(111)
# Inisialisasi data kosong agar tidak error
x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
y = [0]*12
ax.plot(
    x, y,
    marker='o',
    color="#eeeeee",
    linestyle='-',
    linewidth=3,
    markersize=10,
    markerfacecolor='#EEEEEE',
    markeredgecolor='#00ADB5',
    label='Data Penumpang'
)

ax.set_title("Data Penumpang", fontsize=13, color="#EEEEEE", fontweight='bold', pad=20)
ax.set_xlabel("Bulan", fontsize=10, color="#FFFFFF", fontweight='bold')
ax.set_ylabel("Jumlah", fontsize=10, color='#FFFFFF', fontweight='bold')
ax.grid(True, linestyle='--', color='#00ADB5', alpha=0.3)
ax.legend(facecolor="#06334F", edgecolor='#00ADB5', fontsize=11, labelcolor='#EEEEEE')
ax.set_facecolor("#222831")
ax.tick_params(axis='x', colors='#EEEEEE', labelsize=11)
ax.tick_params(axis='y', colors='#EEEEEE', labelsize=11)
fig.tight_layout()
canvas = FigureCanvasTkAgg(fig, master=app)

# tabel (halaman admin)
frameTabel = ttk.Frame(app)
tree = ttk.Treeview(
    frameTabel,
    columns=("NIK", "STASIUN ASAL", "STASIUN TUJUAN", "WAKTU", "TANGGAL KEBERANGKATAN", "JUMLAH PENUMPANG"),
    show="headings", bootstyle="dark"
)
frameTabel = ttk.Frame(app)
tree = ttk.Treeview(
    frameTabel,
    columns=("NIK", "STASIUN ASAL", "STASIUN TUJUAN", "WAKTU", "TANGGAL KEBERANGKATAN", "JUMLAH PENUMPANG"),
    show="headings", bootstyle="dark"
)
tree.heading("NIK", text="NIK")
tree.column("NIK", anchor="center")
tree.heading("STASIUN ASAL", text="ASAL")
tree.column("STASIUN ASAL", anchor="center")
tree.heading("STASIUN TUJUAN", text="TUJUAN")
tree.column("STASIUN TUJUAN", anchor="center")
tree.heading("WAKTU", text="WAKTU")
tree.column("WAKTU", anchor="center")
tree.heading("TANGGAL KEBERANGKATAN", text="TANGGAL")
tree.column("TANGGAL KEBERANGKATAN", anchor="center")
tree.heading("JUMLAH PENUMPANG", text="JUMLAH")
tree.column("JUMLAH PENUMPANG", anchor="center")
tree.column("NIK", anchor="center")
tree.heading("STASIUN ASAL", text="ASAL")
tree.column("STASIUN ASAL", anchor="center")
tree.heading("STASIUN TUJUAN", text="TUJUAN")
tree.column("STASIUN TUJUAN", anchor="center")
tree.heading("WAKTU", text="WAKTU")
tree.column("WAKTU", anchor="center")
tree.heading("TANGGAL KEBERANGKATAN", text="TANGGAL")
tree.column("TANGGAL KEBERANGKATAN", anchor="center")
tree.heading("JUMLAH PENUMPANG", text="JUMLAH")
tree.column("JUMLAH PENUMPANG", anchor="center")

# Halaman Buat Akun
frameBuatAkun = ttk.Frame(app, bootstyle="dark", padding=40, relief="solid")
buttonLogoutBuatAkun = ttk.Button(frameBuatAkun, text="Kembali", command=halamanLogin, bootstyle="dark")
labelJudulBuatAkun = ttk.Label(frameBuatAkun, text="Daftar Akun", font=("Verdana", 10, "bold"))
labelNikBuatAkun = ttk.Label(frameBuatAkun, text="NIK :", font=("Verdana", 8))
entryNikBuatAkun = ttk.Entry(frameBuatAkun)
labelNamaLengkap = ttk.Label(frameBuatAkun, text="NAMA LENGKAP :", font=("Verdana", 8))
entryNamaLengkap = ttk.Entry(frameBuatAkun)
labelEmailpengguna = ttk.Label(frameBuatAkun, text="EMAIL :", font=("Verdana", 8))
entryEmailpengguna = ttk.Entry(frameBuatAkun)
labelNoTelp = ttk.Label(frameBuatAkun, text="NO TELEPON :", font=("Verdana", 8))
entryNoTelp = ttk.Entry(frameBuatAkun)
labeltanggalLahir = ttk.Label(frameBuatAkun, text="TANGGAL LAHIR:", font=("Verdana", 8))
dateentrytanggalLahir = ttk.DateEntry(frameBuatAkun, width=15)
buttonKirimBuatAkun = ttk.Button(
    frameBuatAkun, text="Daftar", bootstyle="primary-outline", padding=(20, 5),
    command=lambda: [buatAkun(), halamanForm(), messagebox.showinfo("Berhasil", "Akun Telah Berhasil Dibuat!")]
)

# Halaman Form
frameForm = ttk.Frame(app, bootstyle="dark", padding=30, relief="solid")
buttonProfil = ttk.Button(frameForm, text="👤Account", command=halamanProfil, bootstyle="dark")
labelJudulForm = ttk.Label(frameForm, text="Pemesanan Tiket", font=("Verdana", 10))
labelNikForm = ttk.Label(frameForm, text="NIK :", font=("Verdana", 8))
entryNikForm = ttk.Entry(frameForm)
labelStasiunAwalForm = ttk.Label(frameForm, text="STASIUN AWAL :", font=("Verdana", 8))
entryStasiunAwalForm = ttk.Entry(frameForm)
labelStasiunTujuanForm = ttk.Label(frameForm, text="STASIUN TUJUAN :", font=("Verdana", 8))
entryStasiunTujuanForm = ttk.Entry(frameForm)
labelTanggalForm = ttk.Label(frameForm, text="TANGGAL :", font=("Verdana", 8))
dateentryTanggalForm = ttk.DateEntry(frameForm, width=15)
labelJumlahPenumpangForm = ttk.Label(frameForm, text="JUMLAH PENUMPANG :", font=("Verdana", 8))
entryJumlahPenumpangForm = ttk.Spinbox(frameForm, from_=1, to=10, width=5)
entryJumlahPenumpangForm.set(1)
buttonKirimForm = ttk.Button(
    frameForm, text="CARI TIKET", padding=(15, 7),
    command=lambda: [halamanPilihTiket(), CariTiket()], width=25
)

# Halaman Profil
frameProfil = ttk.Frame(app, bootstyle="dark", padding=40, relief="solid")
buttonLogoutProfil = ttk.Button(frameProfil, text="⬅️Logout", command=Logout, bootstyle="dark")
LabelJudulProfil = ttk.Label(frameProfil, text="PROFILE", font=("Verdana", 11, "bold"))
separatorProfil = ttk.Separator(frameProfil, orient="horizontal")
LabelNikProfil = ttk.Label(frameProfil, text="NIK", font=("Verdana", 8))
OutputNikProfil = ttk.Label(frameProfil, text="", font=("Verdana", 8))
LabelNamaProfil = ttk.Label(frameProfil, text="NAMA LENGKAP", font=("Verdana", 8))
OutputNamaProfil = ttk.Label(frameProfil, text="", font=("Verdana", 8))
LabelEmailProfil = ttk.Label(frameProfil, text="EMAIL", font=("Verdana", 8))
OutputEmailProfil = ttk.Label(frameProfil, text="", font=("Verdana", 8))
LabelTelpProfil = ttk.Label(frameProfil, text="NO.TELEPON", font=("Verdana", 8))
OutputTelpProfil = ttk.Label(frameProfil, text="", font=("Verdana", 8))
LabelTanggalLahirProfil = ttk.Label(frameProfil, text="TANGGAL LAHIR", font=("Verdana", 8))
OutputTanggaLahirProfil = ttk.Label(frameProfil, text="", font=("Verdana", 8))
buttonkembali = ttk.Button(frameProfil, text="Kembali", command=halamanForm, bootstyle="danger-outline")

# Halaman Pilih Tiket
framePilihTiket = ttk.Frame(app, padding=50, relief="solid", bootstyle="dark")
judulRute = ttk.Label(framePilihTiket, text="", font=("Helvetica", 11, "bold"))
judulTanggal = ttk.Label(framePilihTiket, text="", font=("Helvetica", 10, "bold"))
judulRute.pack(pady=(0, 5), anchor="w")
judulTanggal.pack(pady=(0, 15), anchor="w")
for detail in data_tiket:
    dataTiket(framePilihTiket, detail)
kembali = ttk.Button(framePilihTiket, text="Kembali", bootstyle="danger-outline", padding=(90, 10), command=halamanForm)

# Halaman Metode Pembayaran
frameMetodePembayaran = ttk.Frame(app, bootstyle="dark", padding=40, relief="solid")
labelJudulMetodePembayaran = ttk.Label(frameMetodePembayaran, text="Pilih Metode Pembayaran", font=("Verdana", 10, "bold"))
labelKaiPayMetodePembayaran = ttk.Label(frameMetodePembayaran, text="💳 KAIPay", font=("Verdana", 10, "bold"))
buttonKaiPayMetodePembayaran = ttk.Button(frameMetodePembayaran, text="KAIPay", width=30, command=lambda: pilih_metode_pembayaran("KAIPay"))
labelQrisMetodePembayaran = ttk.Label(frameMetodePembayaran, text="📱QRIS", font=("Verdana", 10, "bold"))
buttonQrisMetodePembayaran = ttk.Button(frameMetodePembayaran, text="QRIS", width=30, command=lambda: pilih_metode_pembayaran("QRIS"))
labelEWalletMetodePembayaran = ttk.Label(frameMetodePembayaran, text="💸 E-Wallet", font=("Verdana", 10, "bold"))
buttonMotionPayMetodePembayaran = ttk.Button(frameMetodePembayaran, text="MOTIONPAY", width=30, command=lambda: pilih_metode_pembayaran("MOTIONPAY"))
buttonOvoMetodePembayaran = ttk.Button(frameMetodePembayaran, text="OVO", width=30, command=lambda: pilih_metode_pembayaran("OVO"))
labelHargaMetodePembayaran = ttk.Label(frameMetodePembayaran, text="Total Harga: Rp xx.xxx", font=("Verdana", 10, "bold"))
buttonkembaliMetodePembayaran = ttk.Button(frameMetodePembayaran, text="Kembali", command=halamanPilihTiket, bootstyle="danger-outline", width=20)

# Halaman Bayar Tiket
frameBayarTiket = ttk.Frame(app, bootstyle="dark", padding=(60, 30), relief="solid")
labelJudulBayarTiket = ttk.Label(frameBayarTiket, text="Bayar dengan QRIS", font=("Verdana", 15))
labelBayarTiket = ttk.Label(frameBayarTiket, text="", font=("Verdana", 10, "bold"))
buttonUbahBayarTiket = ttk.Button(frameBayarTiket, text="Ubah", command=halamanMetodePembayaran, bootstyle="danger-outline", width=8)
labelNikBayarTiket = ttk.Label(frameBayarTiket, text="NIK")
labelNikOutputBayarTiket = ttk.Label(frameBayarTiket, text="")
labelStasiunAwalBayarTiket = ttk.Label(frameBayarTiket, text="STASIUN AWAL")
labelStasiunAwalOutputBayarTiket = ttk.Label(frameBayarTiket, text="")
labelStasiunTujuanBayarTiket = ttk.Label(frameBayarTiket, text="STASIUN TUJUAN")
labelStasiunTujuanOutputBayarTiket = ttk.Label(frameBayarTiket, text="")
labelWaktuBayarTiket = ttk.Label(frameBayarTiket, text="WAKTU")
labelWaktuOutputBayarTiket = ttk.Label(frameBayarTiket, text="")
labelTanggalBayarTiket = ttk.Label(frameBayarTiket, text="TANGGAL")
labelJumlahPenumpangBayarTiket = ttk.Label(frameBayarTiket, text="JUMLAH PENUMPANG")
labelJumlahPenumpangOutputBayarTiket = ttk.Label(frameBayarTiket, text="")
labelTanggalOutputBayarTiket = ttk.Label(frameBayarTiket, text="")
labelTotalPembayaranBayarTiket = ttk.Label(frameBayarTiket, text="TOTAL PEMBAYARAN", font=("Verdana", 9, "bold"))
labelTotalPembayaranOutputBayarTiket = ttk.Label(frameBayarTiket, text="Rp xx.xxx", font=("Verdana", 9, "bold"))
buttonBayarTiket = ttk.Button(frameBayarTiket, text="CETAK TIKET", bootstyle="primary", command=booking)

# Tampilkan halaman login saat aplikasi dijalankan
halamanLogin()
app.mainloop()

