# AI FOR THAI LINE BOT WORKSHOP

## GitHub Codespace

### Fork this repository

1. ไปยัง [AIFORTHAI LINEBOT WORKSHOP For GitHub Codespace](https://github.com/AIforThai/aiforthai-linebot-workshop-codespace) 
2. กดปุ่ม `Fork` ที่มุมขวาบนของหน้าเว็บ
3. เลือกบัญชี GitHub ของคุณเพื่อสร้าง Fork
4. รอให้ GitHub สร้าง Fork ให้เสร็จสิ้น
5. เมื่อเสร็จสิ้น คุณจะถูกนำไปยังหน้า Fork ของคุณ

### Start GitHub Codespace

1. ไปยังหน้า Fork ของคุณ
2. กดปุ่ม `Code` ที่มุมขวาบนของหน้าเว็บ
3. กดปุ่ม `Create Codespace on main`
4. รอให้ GitHub Codespace สร้าง Codespace ให้เสร็จสิ้น
5. เมื่อเสร็จสิ้น คุณจะถูกนำไปยังหน้า Codespace ของคุณ
6. รอให้ Dev Container สร้าง และติดตั้ง dependencies ให้เสร็จสิ้น

### Open Terminal
1. กรณีที่ Terminal ไม่เปิดขึ้นมา ให้กดปุ่ม Terminal ที่มุมซ้ายบนของหน้า Codespace
2. หาก Terminal เปิดอยู่แล้ว กดปุ่ม New Terminal (`+`) เพื่อเปิด Terminal ใหม่

### Setup Environment
1. ใน Terminal เพิ่มสร้างไฟล์ `.env` โดยใช้คำสั่ง

```bash
cp env-example .env
```
2. เปิดไฟล์ `.env`
3. กรอกข้อมูลในไฟล์ `.env` ตามที่กำหนด
4. บันทึกไฟล์ `.env`

### Start Service
1. ใน Terminal รันคำสั่ง

```base
fastapi dev
```
2. หาก port 8000 ไม่ว่างให้เปลี่ยน port โดยการเพิ่ม `--port` ตามด้วย port ที่ต้องการ เช่น

```bash
fastapi dev --port 8080
```

### Forwarding Port
1. กด Tab ที่ชื่อ `Ports`
2. Click ขวาบน port ที่ต้องการ Forward
3. เลือกเมนู Port Visibility
4. เลือก Public เพื่อให้สามารถเข้าถึงได้จากภายนอก
5. Copy URL ที่แสดงในช่อง Public URL
6. นำ URL ที่ได้ไปใช้ใน LINE Developer Console
7. กรอก URL ที่ได้ในช่อง Webhook URL
8. กดปุ่ม Verify เพื่อทดสอบการเชื่อมต่อ
9. หากการเชื่อมต่อสำเร็จ จะมีข้อความ Success แสดงขึ้นมา

## Devcontainer on local

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Visual Studio Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Git](https://git-scm.com/downloads)

### Clone this repository
1. เปิด Terminal
2. ไปยังโฟลเดอร์ที่ต้องการเก็บโปรเจค
3. รันคำสั่ง

```bash
git clone https://github.com/AIforThai/aiforthai-linebot-workshop-codespace
```
4. รอให้ Git Clone โปรเจคเสร็จสิ้น
5. เมื่อเสร็จสิ้น ให้เปิดโฟลเดอร์โปรเจคใน Visual Studio Code

### Open Devcontainer
1. กดปุ่ม `Reopen in Container` ที่มุมขวาล่างของหน้า Visual Studio Code
2. รอให้ Dev Container สร้าง และติดตั้ง dependencies ให้เสร็จสิ้น
3. เมื่อเสร็จสิ้น คุณจะถูกนำไปยังหน้า Dev Container ของคุณ

### Open Terminal
1. กรณีที่ Terminal ไม่เปิดขึ้นมา ให้กดปุ่ม Terminal ที่มุมซ้ายบนของหน้า Dev Container
2. หาก Terminal เปิดอยู่แล้ว กดปุ่ม New Terminal (`+`) เพื่อเปิด Terminal ใหม่


### Setup Environment
1. ใน Terminal เพิ่มสร้างไฟล์ `.env` โดยใช้คำสั่ง

```bash
cp env-example .env
```
2. เปิดไฟล์ `.env`
3. กรอกข้อมูลในไฟล์ `.env` ตามที่กำหนด
4. บันทึกไฟล์ `.env`

### Start Service
1. ใน Terminal รันคำสั่ง

```base
fastapi dev
```
2. หาก port 8000 ไม่ว่างให้เปลี่ยน port โดยการเพิ่ม `--port` ตามด้วย port ที่ต้องการ เช่น

```bash
fastapi dev --port 8080
```
3. รอให้ FastAPI start service เสร็จสิ้น

### Forwarding Port
1. เปิด Tab ที่ชื่อ `Ports`
2. Click`Forward a port`
3. กรอก port ที่ต้องการ Forward
4. ดำเนินการขอ Forward port กับ GitHub
5. Click ขวาบน port ที่ต้องการ Forward
6. เลือกเมนู Port Visibility
7. เลือก Public เพื่อให้สามารถเข้าถึงได้จากภายนอก
8. Copy URL ที่แสดงในช่อง Public URL
9. นำ URL ที่ได้ไปใช้ใน LINE Developer Console
10. กรอก URL ที่ได้ในช่อง Webhook URL
11. กดปุ่ม Verify เพื่อทดสอบการเชื่อมต่อ
12. หากการเชื่อมต่อสำเร็จ จะมีข้อความ Success แสดงขึ้นมา

