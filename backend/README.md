# Movie API

เอกสารประกอบการใช้งานของ Movie API นี้ API นี้สามารถให้ข้อมูลเกี่ยวกับภาพยนตร์ นักแสดง ทีมทำงาน และอื่นๆ นอกจากนี้ยังมีคุณสมบัติที่ช่วยในการดึงข้อมูลจาก API ภายนอกและจัดเก็บลงในฐานข้อมูล

## Endpoints

### PHPMyAdmin

- เข้าถึง PHPMyAdmin เพื่อจัดการฐานข้อมูลของคุณ:
  - URL: [http://localhost:8888](http://localhost:8888)
  - ใช้เพื่อสร้างตารางใหม่หรือดูภาพรวมของข้อมูลในฐานข้อมูล

### API Endpoints

- เข้าถึง API ได้ที่ [http://localhost:5000](http://localhost:5000).

1. **/movies**

   - ดึงข้อมูลเกี่ยวกับภาพยนตร์

2. **/actors**

   - ดึงข้อมูลเกี่ยวกับนักแสดง

3. **/crews**

   - ดึงข้อมูลเกี่ยวกับทีมทำงาน

4. **/update-database**
   - ดึงข้อมูลจาก API ภายนอกและจัดเก็บในฐานข้อมูล

## Docker Usage

ทำตามขั้นตอนนี้เพื่อใช้งาน API โดยใช้ Docker:

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
   - เข้า [http://localhost:5000/movies](http://localhost:5000/movies) หรือ endpoint อื่นๆ
   - ตัวอย่างผลลัพธ์ของ Endpoint [http://localhost:5000/movies](http://localhost:5000/movies)
   - ![image](https://github.com/ikkyuuq/movie_recommendation/assets/67925388/ac20a428-27f8-4a0f-9ad7-5357574d22e8)
   - ตัวอย่างผลลัพธ์ของ Endpoint [http://localhost:5000/actors](http://localhost:5000/actors)
   - ![image](https://github.com/ikkyuuq/movie_recommendation/assets/67925388/f1fe1c12-0b15-4811-b7b9-944516fd27a2)

## ไฟล์

### app.py

สำหรับสร้าง endpoint ใหม่ที่ดึงข้อมูลจากฐานข้อมูล ใช้เมทอดที่ตรงกับการเรียกใช้ฟังก์ชันใน `models.py`

### models.py

สำหรับสร้างฟังก์ชันการดึงข้อมูลจากฐานข้อมูลโดยใช้วิธีต่างๆ (GET, POST, PUT, DELETE)
