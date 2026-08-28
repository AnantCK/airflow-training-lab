# airflow-training-lab
สำหรับการฝึกอบรมหรือทดลองใช้งาน Apache Airflow แบบ Online โดยไม่ต้องติดตั้งลงเครื่องคอมพิวเตอร์ของผู้เรียน

สำหรับผู้เรียน (วิธีเข้าใช้งานผ่าน Browser)**

1. **Fork Repository ไปยังบัญชีของตนเอง:**
1. ผู้เรียนเปิดลิงก์ Repository ของผู้สอน https://github.com/anantchok/airflow-training-lab
2. กดปุ่ม **Fork** ด้านขวาบน เพื่อคัดลอกโปรเจกต์ไปยังบัญชี GitHub ของตนเอง


2. **เปิดใช้งาน GitHub Codespaces:**
1. ในหน้า Repo ที่ Fork มา ให้กดปุ่มสีเขียว **`<> Code`**
2. เลือกแท็บ **Codespaces**
3. กดปุ่ม **Create codespace on main** (ระบบจะเปิดหน้าจอ VS Code บนเบราว์เซอร์ ใช้เวลาเตรียมเครื่องประมาณ 1–2 นาที)


3. **รันคำสั่งเริ่มต้นระบบ Airflow:**
เมื่อหน้าต่าง Terminal ด้านล่างปรากฏขึ้น ให้พิมพ์คำสั่งตามลำดับ:

```bash
# 1. Initial ฐานข้อมูลและสร้าง User เริ่มต้น
docker compose up airflow-init

# 2. เมื่อขึ้นสถานะ airflow-init completed แล้ว ให้สั่งรันทั้งระบบแบบ Background
docker compose up -d

```


4. **เปิด Airflow Web UI:**
1. รอประมาณ 30–60 วินาที จะมี Popup แจ้งเตือนพอร์ต **8080** เด้งขึ้นมามุมขวาล่าง ให้คลิก **Open in Browser** (หรือไปที่แท็บ **PORTS** ด้านล่าง แล้วคลิกไอคอนลูกโลกที่ Port `8080`)
2. หากขึ้น error ให้รอระบบสำหรับการเปิดใช้งานประมาณ 1-2 นาทีเนื่องจากต้องใช้เวลาในช่วงเริ่มใช้งานครั้งแรก
3. ระบบจะเปิดแท็บใหม่เข้าสู่หน้า Airflow Login
4. กรอก Username: `airflow` และ Password: `airflow` เพื่อเริ่มใช้งานและแก้ไขโค้ดในโฟลเดอร์ `dags/` ได้ทันที
5. ระบบจะไปที่หน้า home หาก url เป็น: localhost/home ให้ click back url ที่ใช้งานจริง 
