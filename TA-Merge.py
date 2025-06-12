import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
import threading

# Function อ่านไฟล์แบบ fix-width (ไม่ skip record, log warning ถ้า Date/Time ผิด)
def read_fix_width_file(filepath):
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[1:]:
        if line.strip() == "":
            continue
        no = line[0:22].strip()
        datetime_field = line[22:43].strip()
        status = line[43:63].strip()
        location_id = line[63:].strip()

        try:
            dt_obj = datetime.strptime(datetime_field, "%d/%m/%Y %H:%M")
        except ValueError:
            print(f"[Warning] Date/Time format invalid → No={no}, Date/Time='{datetime_field}', Status={status}, Location={location_id}")
            dt_obj = None  # ยังเก็บ record เข้า list

        records.append((no, datetime_field, status, location_id, dt_obj))

    return records

# Function merge และ export (run ใน thread)
def merge_and_export_thread():
    try:
        progress_bar['value'] = 0
        progress_bar.update()

        records1 = read_fix_width_file(file1_path)
        progress_bar['value'] = 20
        progress_bar.update()

        records2 = read_fix_width_file(file2_path)
        progress_bar['value'] = 40
        progress_bar.update()

        all_records = records1 + records2

        # sort → ถ้า dt_obj=None ให้ใช้ datetime.min
        all_records.sort(key=lambda x: x[4] if x[4] is not None else datetime.min)
        progress_bar['value'] = 60
        progress_bar.update()

        now = datetime.now()
        filename = now.strftime("Site_%d%m%Y_%H%M%S.txt")
        export_path = os.path.join(output_folder, filename)

        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(f"{'No.':<22}{'Date/Time':<21}{'Status':<20}{'Location ID':<10}\n")
            for i, record in enumerate(all_records):
                f.write(f"{record[0]:<22}{record[1]:<21}{record[2]:<20}{record[3]:<10}\n")
                if i % 100 == 0:
                    progress_bar['value'] = 60 + int((i / len(all_records)) * 40)
                    progress_bar.update()

        progress_bar['value'] = 100
        progress_bar.update()

        messagebox.showinfo("Success", f"Merge สำเร็จ!\nไฟล์ถูกบันทึกที่:\n{export_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        btn_merge.config(state=tk.NORMAL)

# Function preview จำนวน record
def preview_counts():
    try:
        records1 = read_fix_width_file(file1_path)
        records2 = read_fix_width_file(file2_path)
        all_records = records1 + records2

        label_preview_fm.config(text=f"จำนวน record FM: {len(records1)}")
        label_preview_cl.config(text=f"จำนวน record CL: {len(records2)}")
        label_preview_total.config(text=f"จำนวน record รวม: {len(all_records)}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function merge แบบเรียกผ่านปุ่ม
def merge_and_export():
    if not file1_path or not file2_path:
        messagebox.showerror("Error", "กรุณาเลือกไฟล์ให้ครบทั้ง 2 ไฟล์ก่อน")
        return
    if not output_folder:
        messagebox.showerror("Error", "กรุณาเลือกโฟลเดอร์สำหรับบันทึกไฟล์ก่อน")
        return

    btn_merge.config(state=tk.DISABLED)
    progress_bar['value'] = 0
    threading.Thread(target=merge_and_export_thread).start()

# Function เลือกไฟล์ที่ 1
def select_file1():
    global file1_path
    path = filedialog.askopenfilename(title="เลือกไฟล์ที่ 1 (FM)")
    if path:
        file1_path = path
        label_file1.config(text=f"FM: {os.path.basename(path)}")
        preview_counts()

# Function เลือกไฟล์ที่ 2
def select_file2():
    global file2_path
    path = filedialog.askopenfilename(title="เลือกไฟล์ที่ 2 (CL)")
    if path:
        file2_path = path
        label_file2.config(text=f"CL: {os.path.basename(path)}")
        preview_counts()

# Function เลือกโฟลเดอร์ปลายทาง
def select_output_folder():
    global output_folder
    folder = filedialog.askdirectory(title="เลือกโฟลเดอร์สำหรับบันทึกไฟล์")
    if folder:
        output_folder = folder
        label_output_folder.config(text=f"โฟลเดอร์ปลายทาง: {folder}")

# --- Main GUI ---
root = tk.Tk()
root.title("โปรแกรม Merge ไฟล์ Fix-Width (Robust + No Skip + Log Warning)")
root.geometry("600x500")

file1_path = ""
file2_path = ""
output_folder = ""

label_title = tk.Label(root, text="โปรแกรม Merge ไฟล์ Fix-Width", font=("Arial", 16), fg="blue")
label_title.pack(pady=10)

btn_file1 = tk.Button(root, text="เลือกไฟล์ที่ 1 (FM)", command=select_file1, width=30)
btn_file1.pack(pady=5)

label_file1 = tk.Label(root, text="ยังไม่ได้เลือกไฟล์ที่ 1 (FM)")
label_file1.pack()

btn_file2 = tk.Button(root, text="เลือกไฟล์ที่ 2 (CL)", command=select_file2, width=30)
btn_file2.pack(pady=5)

label_file2 = tk.Label(root, text="ยังไม่ได้เลือกไฟล์ที่ 2 (CL)")
label_file2.pack()

btn_output_folder = tk.Button(root, text="เลือกโฟลเดอร์ปลายทาง", command=select_output_folder, width=30)
btn_output_folder.pack(pady=5)

label_output_folder = tk.Label(root, text="ยังไม่ได้เลือกโฟลเดอร์ปลายทาง")
label_output_folder.pack()

# Section preview counts
label_preview_title = tk.Label(root, text="Preview จำนวน Record", font=("Arial", 14), fg="green")
label_preview_title.pack(pady=10)

label_preview_fm = tk.Label(root, text="จำนวน record FM: -")
label_preview_fm.pack()

label_preview_cl = tk.Label(root, text="จำนวน record CL: -")
label_preview_cl.pack()

label_preview_total = tk.Label(root, text="จำนวน record รวม: -")
label_preview_total.pack()

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

btn_merge = tk.Button(root, text="Merge และ Export", command=merge_and_export, bg="green", fg="white", width=30, height=2)
btn_merge.pack(pady=10)

label_footer = tk.Label(root, text="Developed by ChatGPT + คุณ", font=("Arial", 10), fg="gray")
label_footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
