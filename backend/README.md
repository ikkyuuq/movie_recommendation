# Movie API

เอกสารประกอบการใช้งานของ Movie API นี้ API นี้สามารถให้ข้อมูลเกี่ยวกับภาพยนตร์ นักแสดง ทีมทำงาน และอื่นๆ นอกจากนี้ยังมีคุณสมบัติที่ช่วยในการดึงข้อมูลจาก API ภายนอกและจัดเก็บลงในฐานข้อมูล

## Endpoints

### API Endpoints

- เข้าถึง API ได้ที่ [https://mlynx-server-845b26ee5ca0.herokuapp.com](https://mlynx-server-845b26ee5ca0.herokuapp.com).

1. **/movie**

   - ดึงข้อมูลเกี่ยวกับภาพยนตร์

2. **/movie?tmdb_id=xxxx**
   
   - ดึงข้อมูลฉพาะหนังเรื่องๆนึงจาก Database โดยใช้ TMDB ID

3. **/comment?movie_id=xxxx**

   - ดึงข้อมูลคอมเม้นในแต่ละหนัง

4. **/like?movie_id=xxxx&user_id=xxxx**
   
   - ดึงข้อมูลจำนวนของ comment id ที่ user id กดไลก์
  
5. **/favour?uesr_id=xxxx**
   
   - ดึงข้อมูลข้อมูลหนังที่ผู้ใช้เพิ่มไว้ใน My list

6. **/updb?start_p=1&stop_p=500**
   
   - ดึงข้อมูลจาก API ภายนอกและจัดเก็บในฐานข้อมูล
