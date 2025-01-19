import psutil
import win32evtlog
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import ctypes


def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not check_admin():
    messagebox.showwarning("Yetki Hatası", "Bu uygulama yönetici izni olmadan doğru çalışmaz!")


# Olayları okuma işlemi
def read_event_log():
    # Yükleme göstergesi
    loading_label_logs.config(text="Yükleniyor...")
    loading_label_logs.update()

    # Listeyi GUI'de göster
    for item in treeview_logs.get_children():
        treeview_logs.delete(item)  # Eski verileri temizle

    # Başlık etiketini güncelliyoruz
    header_label_logs.config(text="")

    server = 'localhost'
    logtype = log_type_combobox.get()

    try:
        handle = win32evtlog.OpenEventLog(server, logtype)
        events = win32evtlog.ReadEventLog(handle,
                                          win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)

        for event in events:
            event_source = event.SourceName
            event_message = event.StringInserts if event.StringInserts else ['No message available']
            treeview_logs.insert('', 'end', values=(event_source, event_message[0]))

        loading_label_logs.config(text="")
        header_label_logs.config(text=f"Olay Günlükleri ({len(events)})")
    except Exception as e:
        messagebox.showerror("Hata", f"Olay günlüğü okunamadı: {e}")


# Olay günlüğü sekmesindeki fonksiyon
def threaded_event_log():
    threading.Thread(target=read_event_log, daemon=True).start()


## GÜVENİLİR İŞLEM LİSTESİ
trusted_process_list = [
    "csrss.exe",
    "WidgetService.exe",
    "amdfendrsr.exe",
    "CPUMetricsServer.exe",
    "ApplicationFrameHost.exe",
    "vmmemCmZygote",
    "NVDisplay.Container.exe",
    "UserOOBEBroker.exe",
    "wininit.exe",
    "System Idle Process",
    "cncmd.exe",
    "HTTPDebuggerSvc.exe",
    "Riot Client.exe",
    "pycharm64.exe",
    "ACCSvc.exe",
    "MsMpEng.exe",
    "Spotify.exe",
    "SecurityHealthSystray.exe",
    "System",
    "RuntimeBroker.exe",
    "dasHost.exe",
    "fsnotifier.exe",
    "PSSvc.exe",
    "unsecapp.exe",
    "MemCompression",
    "RazerCentralService.exe",
    "MpDefenderCoreService.exe",
    "PSAgent.exe",
    "NgcIso.exe",
    "FoxitPDFReaderUpdateService.exe",
    "conhost.exe",
    "chrome.exe",
    "SDXHelper.exe",
    "RadeonSoftware.exe",
    "Video.UI.exe",
    "audiodg.exe",
    "LockApp.exe",
    "winlogon.exe",
    "Widgets.exe",
    "lsass.exe",
    "sqlceip.exe",
    "atiesrxx.exe",
    "sqlservr.exe",
    "python.exe",
    "SecurityHealthService.exe",
    "AMDRSServ.exe",
    "CefSharp.BrowserSubprocess.exe",
    "vmms.exe",
    "ShellHost.exe",
    "OfficeClickToRun.exe",
    "TeamViewer_Service.exe",
    "wlanext.exe",
    "WhatsApp.exe",
    "atieclxx.exe",
    "wslservice.exe",
    "gamingservicesnet.exe",
    "XboxPcAppFT.exe",
    "LsaIso.exe",
    "TextInputHost.exe",
    "Microsoft.SharePoint.exe",
    "DtsApo4Service.exe",
    "SearchIndexer.exe",
    "SearchHost.exe",
    "NisSrv.exe",
    "WmiPrvSE.exe",
    "QtWebEngineProcess.exe",
    "gamingservices.exe",
    "RiotClientServices.exe",
    "NVIDIA Web Helper.exe",
    "ACCStd.exe",
    "Razer Central.exe",
    "msedge.exe",
    "RtkAudUService64.exe",
    "GameManagerService.exe",
    "smss.exe",
    "nvcontainer.exe",
    "StartMenuExperienceHost.exe",
    "ctfmon.exe",
    "SystemSettings.exe",
    "sqlwriter.exe",
    "ShellExperienceHost.exe",
    "jcef_helper.exe",
    "spoolsv.exe",
    "explorer.exe",
    "Registry",
    "PSAdminAgent.exe",
    "AggregatorHost.exe",
    "vmcompute.exe",
    "RiotClientCrashHandler.exe",
    "vgtray.exe",
    "Razer Synapse Service.exe",
    "services.exe",
    "Razer Synapse 3.exe",
    "AMDRSSrcExt.exe",
    "sihost.exe",
    "taskhostw.exe",
    "LiveUpdateChecker.exe",
    "fontdrvhost.exe",
    "Razer Synapse Service Process.exe",
    "svchost.exe",
    "dllhost.exe",
    "armsvc.exe",
    "dwm.exe",
    "Taskmgr.exe",
    "backgroundTaskHost.exe",
    "Discord.exe"
]


def list_processes():
    # listeler
    process_list = []
    untrusted_process_list = []

    # Yükleme göstergesi
    loading_label_process.config(text="Yükleniyor...")
    loading_label_process.update()

    # Listeyi GUI'de göster
    for item in treeview.get_children():
        treeview.delete(item)  # Eski verileri temizle

    # Başlık etiketini güncelliyoruz
    header_label_process.config(text="")

    # Çalışan işlemleri listele
    for process in psutil.process_iter(
            ['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status', 'exe', 'cwd', 'open_files',
             'create_time']):
        try:
            # my_set.add(process.name())
            process_list.append(process)
        except psutil.AccessDenied:
            print(f"Erişim engellendi: {process.pid}")

    # İşlemleri kontrol et
    for running_process in process_list:
        try:
            if running_process.name() not in trusted_process_list:
                untrusted_process_list.append(running_process)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("Hatalı veya erişime engelli bir işlem")
            # İşlem yoksa, erişim engellenmişse veya ölü bir işlemse atla
            pass

    for untrusted_process in untrusted_process_list:
        print(untrusted_process.info)

        treeview.insert('', 'end', values=(
            untrusted_process.pid or None,
            untrusted_process.name() or None,
            untrusted_process.cpu_percent() or None,
            untrusted_process.memory_percent() or None,
            untrusted_process.exe() or None,
            untrusted_process.status() or None,
        ))

    # Yükleme durumu bitirme
    loading_label_process.config(text="")

    # Başlık etiketini güncelliyoruz
    header_label_process.config(text=f"Çalışan İşlemler ({len(untrusted_process_list)})")


# İşlemleri sonlandıran fonksiyon
def terminate_processes(pids):
    try:
        for pid in pids:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=3)  # İşlemin gerçekten sonlandığından emin ol
        messagebox.showinfo("Başarılı", f"Seçilen işlemler başarıyla sonlandırıldı.")
        threaded_process_list()  # İşlem sonlandıktan sonra listeyi yenile
    except psutil.NoSuchProcess:
        messagebox.showerror("Hata", "Bazı işlemler zaten sonlandırılmış.")
        threaded_process_list()  # İşlem bulunamıyorsa yine de listeyi yenile
    except psutil.AccessDenied:
        messagebox.showerror("Hata", "Bazı işlemleri sonlandırmak için gerekli izinlere sahip değilsiniz.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")


# İşlemi sonlandırmadan önce onay isteyen fonksiyon
def confirm_termination(pids):
    result = messagebox.askyesno("Onay", f"Seçili işlemleri sonlandırmak istediğinize emin misiniz?")
    if result:
        terminate_processes(pids)


# Sağ tıklama menüsünü açan fonksiyon
def show_context_menu(event):
    selected_items = treeview.selection()
    if selected_items:  # Seçili öğeler varsa
        # Menüdeki işlemleri etkinleştir
        context_menu.entryconfig("Seçili İşlemleri Sonlandır", state="normal")
    else:  # Hiçbir şey seçilmemişse menüdeki işlemleri devre dışı bırak
        context_menu.entryconfig("Seçili İşlemleri Sonlandır", state="disabled")
    context_menu.post(event.x_root, event.y_root)


# İşlemleri arka planda almak için threading
def threaded_process_list():
    # Bu fonksiyon, list_processes fonksiyonunu ayrı bir thread'de çalıştıracak
    threading.Thread(target=list_processes).start()


# Tkinter penceresi oluşturma
root = tk.Tk()
root.title("Modern Process Viewer")
root.geometry("1200x600")

# Notebook (sekme sistemi) oluşturma
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# İşlem sekmesi
process_tab = ttk.Frame(notebook)
notebook.add(process_tab, text="İşlem Listesi", padding=5)

# Olay günlüğü sekmesi
log_tab = ttk.Frame(notebook)
notebook.add(log_tab, text="Olay Günlükleri", padding=5)

# İşlem Listesi sekmesi

# Frame oluşturuyoruz ve Treeview'u içine yerleştiriyoruz
frame_processes = tk.Frame(process_tab)
frame_processes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Treeview widget'ı oluşturma (Tablo görünümü)
treeview = ttk.Treeview(frame_processes, columns=("PID", "Name", "CPU Usage", "Memory Usage", "Exe", "Status"),
                        show="headings")

# Sütun başlıklarını düzenleme
treeview.heading("PID", text="PID")
treeview.heading("Name", text="Name")
treeview.heading("CPU Usage", text="CPU Usage (%)")
treeview.heading("Memory Usage", text="Memory Usage (%)")
treeview.heading("Exe", text="Exe")
treeview.heading("Status", text="Status")

# Her sütunun veri kısmının ortalanmasını sağlayalım
treeview.column("PID", anchor="center", width=80)
treeview.column("Name", anchor="center", width=100)
treeview.column("CPU Usage", anchor="center", width=200)
treeview.column("Memory Usage", anchor="center", width=200)
treeview.column("Exe", anchor="center", width=200)
treeview.column("Status", anchor="center", width=100)

# Kaydırıcıları ekliyoruz (dikey ve yatay)
scrollbar_y = tk.Scrollbar(frame_processes, orient="vertical", command=treeview.yview)
scrollbar_x = tk.Scrollbar(frame_processes, orient="horizontal", command=treeview.xview)

treeview.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# Treeview ve scrollbar'ı yerleştiriyoruz
treeview.grid(row=0, column=0, sticky="nsew")
scrollbar_y.grid(row=0, column=1, sticky="ns")
scrollbar_x.grid(row=1, column=0, sticky="ew")

# Frame'deki satır ve sütunların genişlemesini sağlıyoruz
frame_processes.grid_rowconfigure(0, weight=1, uniform="equal")  # Dikeydeki genişlemeyi sağlıyoruz
frame_processes.grid_columnconfigure(0, weight=1, uniform="equal")  # Yatayda genişlemeyi sağlıyoruz

# Sağ tıklama menüsü (context menu)
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Seçili İşlemleri Sonlandır", state="disabled",
                         command=lambda: confirm_termination(
                             [int(treeview.item(item, "values")[0]) for item in treeview.selection()]))

# Treeview'da sağ tıklama için olay ekliyoruz
treeview.bind("<Button-3>", show_context_menu)

# Yükleme etiketi (loading label)
loading_label_process = tk.Label(process_tab, text="", font=("Arial", 12), fg="blue")
loading_label_process.pack(pady=5)

# Başlık etiketi
header_label_process = tk.Label(process_tab, text="", font=("Arial", 13))
header_label_process.pack(pady=5)

# Listeyi güncellemek için buton
button = tk.Button(process_tab, text="List Processes", command=threaded_process_list, bg="#4CAF50", fg="white",
                   font=("Arial", 12))
button.pack(pady=20)

# Olay Günlükleri sekmesi

# Olay günlükleri sekmesindeki Frame ve Treeview oluşturma
frame_logs = tk.Frame(log_tab)
frame_logs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Log türünü seçmek için bir ComboBox ekleyelim
log_types = ['System', 'Application', 'Security', 'Setup', 'ForwardedEvents', 'Internet Explorer', 'Windows PowerShell']
log_type_combobox = ttk.Combobox(log_tab, values=log_types, state="readonly", width=20)
log_type_combobox.set('System')  # Varsayılan olarak 'System' seçili
log_type_combobox.pack(pady=10)

# Treeview widget'ı oluşturma (Olaylar için)
treeview_logs = ttk.Treeview(frame_logs, columns=("Source", "Message"), show="headings")

# Sütun başlıklarını düzenleme
treeview_logs.heading("Source", text="Kaynak")
treeview_logs.heading("Message", text="Mesaj")

# Her sütunun veri kısmının ortalanmasını sağlıyoruz
treeview_logs.column("Source", anchor="center", width=200)
treeview_logs.column("Message", anchor="center", width=600)

# Treeview widget'ını doğru bir şekilde ekleyelim
treeview_logs.pack(fill=tk.BOTH, expand=True)

# Frame'deki satır ve sütunların genişlemesini sağlıyoruz
frame_logs.grid_rowconfigure(0, weight=1, uniform="equal")  # Dikeydeki genişlemeyi sağlıyoruz
frame_logs.grid_columnconfigure(0, weight=1, uniform="equal")  # Yatayda genişlemeyi sağlıyoruz

# Yükleme etiketi (loading label) - Olay Günlükleri sekmesi
loading_label_logs = tk.Label(log_tab, text="", font=("Arial", 12), fg="blue")
loading_label_logs.pack(pady=5)

# Başlık etiketi - Olay Günlükleri sekmesi
header_label_logs = tk.Label(log_tab, text="Olay Günlükleri", font=("Arial", 13))
header_label_logs.pack(pady=5)

# Kaydırıcıları ekliyoruz (dikey ve yatay)
scrollbar_y_logs = tk.Scrollbar(frame_logs, orient="vertical", command=treeview_logs.yview)
scrollbar_x_logs = tk.Scrollbar(frame_logs, orient="horizontal", command=treeview_logs.xview)

treeview_logs.configure(yscrollcommand=scrollbar_y_logs.set, xscrollcommand=scrollbar_x_logs.set)

# Treeview ve scrollbar'ı yerleştiriyoruz
treeview_logs.grid(row=0, column=0, sticky="nsew")
scrollbar_y_logs.grid(row=0, column=1, sticky="ns")
scrollbar_x_logs.grid(row=1, column=0, sticky="ew")

# Olayları yüklemek için buton
button_logs = tk.Button(log_tab, text="Olay Günlüklerini Yükle", command=threaded_event_log, bg="#4CAF50", fg="white",
                        font=("Arial", 12))
button_logs.pack(pady=20)

# Sağ alt köşeye sabit bir label ekliyoruz
status_label = tk.Label(root, text="Özer Technologies © 2025", font=("Arial", 10), fg="grey")
status_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")  # Sağ alt köşeye sabitler

# Pencereyi çalıştırma
root.mainloop()
