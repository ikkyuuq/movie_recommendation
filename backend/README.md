# Movie API

เอกสารประกอบการใช้งานของ Movie API นี้ API นี้สามารถให้ข้อมูลเกี่ยวกับภาพยนตร์ นักแสดง ทีมทำงาน และอื่นๆ นอกจากนี้ยังมีคุณสมบัติที่ช่วยในการดึงข้อมูลจาก API ภายนอกและจัดเก็บลงในฐานข้อมูล

## Endpoints

### PHPMyAdmin

- เข้าถึง PHPMyAdmin เพื่อจัดการฐานข้อมูลของคุณ:
  - URL: [http://localhost:8888](http://localhost:8888)
  - ใช้เพื่อสร้างตารางใหม่หรือดูภาพรวมของข้อมูลในฐานข้อมูล

### API Endpoints

- เข้าถึง API ได้ที่ [http://localhost:5000](http://localhost:5000).

1. **/getmovies**

   - ดึงข้อมูลเกี่ยวกับภาพยนตร์

2. **/getactors**

   - ดึงข้อมูลเกี่ยวกับนักแสดง

3. **/getcrews**

   - ดึงข้อมูลเกี่ยวกับทีมทำงาน

4. **/fetchapitodb**
   - ดึงข้อมูลจาก API ภายนอกและจัดเก็บในฐานข้อมูล

## Docker Usage

ทำตามขั้นตอนนี้เพื่อติดตั้ง API โดยใช้ Docker:

1. โคลนที่เก็บ repository นี้ลงในเครื่องของคุณ

   ```bash
   git clone <repository_url>
   ```

2. เข้าไปที่ไดเร็กทอรีที่มีไฟล์ `docker-compose.yml`

   ```bash
   cd <path_to_workdir>
   ```

3. สร้างและเริ่มต้นคอนเทนเนอร์

   ```bash
   docker-compose up -d --build
   ```

4. นำเข้าโครงสร้างฐานข้อมูล

   - เข้าถึง Docker mysql container
     ```bash
     docker exec -it database bash
     ```
   - เข้าถึง MySQL ใน Docker container
     ```bash
     mysql -u root -p
     ```
   - ป้อนรหัสผ่าน (รหัสผ่าน: moviedb@password)
   - นำเข้าโครงสร้าง
     ```bash
     mysql -u root -p  < schema.sql
     ```
   - ป้อนรหัสผ่าน (รหัสผ่าน: moviedb@password)

5. ดึงข้อมูลจาก API ภายนอกเพื่อเติมฐานข้อมูล

   - กระทำคำสั่งต่อไปนี้ แทน `{page_to_start}` และ `{page_to_stop}` ด้วยช่วงหน้าที่ต้องการ
     ```bash
     localhost:5000/fetchapitodb?start_p={page_to_start}&stop_p={page_to_stop}
     ```

6. ทดสอบ Endpoint ของ API
   - เข้า [http://localhost:5000/getmovies](http://localhost:5000/getmovies) หรือ endpoint อื่นๆ

## ไฟล์

### app.py

ไฟล์นี้มีรหัสสำหรับสร้าง endpoint ใหม่ที่ดึงข้อมูลจากฐานข้อมูล ใช้เมทอดที่ตรงกับการเรียกใช้ฟังก์ชันใน `models.py`

### models.py

ไฟล์นี้มีฟังก์ชันสำหรับการดึงข้อมูลจากฐานข้อมูลโดยใช้วิธี HTTP ต่างๆ (GET, POST, PUT, DELETE)

สามารถสำรวจและปรับแต่งไฟล์เหล่านี้ตามความต้องการของทีมได้โดยอิสระ หากมีคำถามหรือปัญหาใด ๆ โปรดอ่านเอกสารหรือติดต่อผู้ดูแลโปรเจค
